from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise RuntimeError("PyYAML is required for pricing configs. Install with: pip install pyyaml") from exc

from .models import HoldingSnapshot, PriceRequest, PricingPassResult
from .shortlist_builder import (
    build_challenger_shortlist,
    build_holdings_shortlist,
    build_radar_alternative_shortlist,
    build_radar_primary_shortlist,
    merge_and_deduplicate,
)
from .close_resolver import CloseResolver
from .fx_resolver import resolve_fx
from .audit_writer import write_price_audit

REPORT_RE = re.compile(r"weekly_analysis(?:_pro)?_(\d{6})(?:_(\d{2}))?\.md$")
FRESH_PRICE_STATUSES = {"fresh_close", "fresh_fallback_source"}
PUBLICATION_DECISION = "update_covered_holdings_carry_unresolved"


def latest_report_file(output_dir: Path) -> Path:
    files = []
    for path in output_dir.glob("weekly_analysis_pro_*.md"):
        if path.name.startswith("weekly_analysis_pro_nl_"):
            continue
        m = REPORT_RE.match(path.name)
        if m:
            day = m.group(1)
            version = int(m.group(2) or "1")
            files.append((day, version, path))
    if not files:
        raise RuntimeError("No production ETF pro reports found in output/.")
    files.sort(key=lambda x: (x[0], x[1]))
    return files[-1][2]


def requested_close_from_today(today: date) -> str:
    d = today
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d.isoformat()


def _to_float(text: str) -> float | None:
    text = text.replace(",", "").replace("%", "").strip()
    if not text or text == "-":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _clean_symbol(text: str) -> str:
    text = text.strip().upper()
    return re.sub(r"[^A-Z0-9./_-]", "", text)


def parse_section15_holdings(md_text: str) -> tuple[list[HoldingSnapshot], dict[str, float]]:
    section_start = md_text.find("## 15.")
    if section_start == -1:
        return [], {}
    section = md_text[section_start:]
    holdings: list[HoldingSnapshot] = []
    weights: dict[str, float] = {}
    in_table = False
    for line in section.splitlines():
        if line.startswith("| Ticker |"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                break
            if "---" in line:
                continue
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) < 7:
                continue
            ticker = parts[0].upper()
            if ticker == "CASH" or not ticker:
                continue
            shares = _to_float(parts[1])
            previous_price_local = _to_float(parts[2])
            currency = parts[3] or "USD"
            previous_market_value_local = _to_float(parts[4])
            previous_market_value_eur = _to_float(parts[5])
            previous_weight_pct = _to_float(parts[6])
            snapshot = HoldingSnapshot(
                ticker=ticker,
                shares=0.0 if shares is None else shares,
                previous_price_local=previous_price_local,
                currency=currency,
                previous_market_value_local=previous_market_value_local,
                previous_market_value_eur=previous_market_value_eur,
                previous_weight_pct=previous_weight_pct,
            )
            holdings.append(snapshot)
            if previous_weight_pct is not None:
                weights[ticker] = previous_weight_pct
    return holdings, weights


def parse_section16_watchlist(md_text: str) -> tuple[list[str], list[str], list[str]]:
    section_start = md_text.find("### Watchlist / dynamic radar memory")
    if section_start == -1:
        return [], [], []
    section = md_text[section_start:]
    primaries: list[str] = []
    alternatives: list[str] = []
    challengers: list[str] = []
    in_table = False
    for line in section.splitlines():
        if line.startswith("| Theme | Primary ETF | Alternative ETF |"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                break
            if "---" in line:
                continue
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if len(parts) < 5:
                continue
            primary = _clean_symbol(parts[1])
            alternative = _clean_symbol(parts[2])
            status = parts[4].lower()
            if primary:
                primaries.append(primary)
                if "watchlist" in status:
                    challengers.append(primary)
            if alternative:
                alternatives.append(alternative)
    return primaries, alternatives, challengers


def parse_section2_replacements(md_text: str) -> list[str]:
    section_start = md_text.find("### Best replacements to fund")
    if section_start == -1:
        return []
    section = md_text[section_start:]
    replacements: list[str] = []
    for line in section.splitlines()[1:10]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("###"):
            break
        if stripped.startswith("-"):
            symbol = _clean_symbol(stripped.lstrip("- "))
            if symbol and symbol != "NONE":
                replacements.append(symbol)
    return replacements


def load_policy(rate_limit_file: str) -> dict:
    return yaml.safe_load(Path(rate_limit_file).read_text(encoding="utf-8")).get("policy", {})


def _build_blocking_reasons(
    *,
    holdings_count: int,
    fresh_count: int,
    coverage_count_pct: float,
    invested_weight_coverage_pct: float,
    unresolved: list[str],
    fx_status: str | None,
) -> list[str]:
    reasons: list[str] = []
    if holdings_count <= 0:
        reasons.append("No holdings were parsed from the latest production report.")
    if fresh_count <= 0:
        reasons.append("No held ETF received a fresh verified close or accepted fresh fallback source.")
    if coverage_count_pct < 75.0 and invested_weight_coverage_pct < 85.0:
        reasons.append(
            "Fresh coverage below publication threshold: "
            f"count={coverage_count_pct:.2f}% and invested_weight={invested_weight_coverage_pct:.2f}%."
        )
    if fx_status not in FRESH_PRICE_STATUSES:
        reasons.append(f"FX basis is not fresh enough for publication: status={fx_status or 'missing'}.")
    if unresolved:
        reasons.append(f"Unresolved held tickers: {', '.join(sorted(set(unresolved)))}.")
    return reasons


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--requested-close-date", default=None)
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--pricing-dir", default="output/pricing")
    parser.add_argument("--rate-limit-file", default="pricing/rate_limits.yaml")
    parser.add_argument("--allow-partial", action="store_true", help="Write the audit but do not fail when publication is blocked.")
    args = parser.parse_args()

    today = date.today()
    requested_close_date = args.requested_close_date or requested_close_from_today(today)
    run_date = today.isoformat()

    output_dir = Path(args.output_dir)
    latest = latest_report_file(output_dir)
    md_text = latest.read_text(encoding="utf-8")
    holding_snapshots, weights = parse_section15_holdings(md_text)
    if not holding_snapshots:
        raise RuntimeError("Could not parse current holdings from section 15.")

    holding_symbols = [h.ticker for h in holding_snapshots]
    radar_primaries, radar_alternatives, watchlist_challengers = parse_section16_watchlist(md_text)
    replacement_candidates = parse_section2_replacements(md_text)
    policy = load_policy(args.rate_limit_file)
    max_alternatives = int(policy.get("max_alternatives_to_price", 8))
    max_challengers = int(policy.get("max_challengers_to_price", 6))

    challenger_symbols = replacement_candidates + [s for s in watchlist_challengers if s not in replacement_candidates]

    shortlist = merge_and_deduplicate(
        build_holdings_shortlist(holding_symbols)
        + build_radar_primary_shortlist(radar_primaries)
        + build_radar_alternative_shortlist(radar_alternatives, max_alternatives)
        + build_challenger_shortlist(challenger_symbols, max_challengers)
    )

    resolver = CloseResolver("pricing/source_registry.yaml", args.rate_limit_file, run_date)

    results = []
    fresh_count = 0
    carried_forward_count = 0
    unresolved = []
    fresh_weight = 0.0

    for item in shortlist:
        result = resolver.resolve(PriceRequest(symbol=item.symbol, requested_close_date=requested_close_date, kind=item.kind))
        results.append(result)
        if item.kind == "holding":
            if result.status in FRESH_PRICE_STATUSES:
                fresh_count += 1
                fresh_weight += weights.get(item.symbol.upper(), 0.0)
            elif result.status == "carried_forward" or result.carried_forward:
                carried_forward_count += 1
            if result.status == "unresolved":
                unresolved.append(item.symbol)

    fx = resolve_fx(requested_close_date)

    holdings_count = len(holding_symbols)
    coverage_count_pct = round((fresh_count / holdings_count) * 100.0, 2) if holdings_count else 0.0
    invested_weight_coverage_pct = round(fresh_weight, 2)
    publication_allowed = coverage_count_pct >= 75.0 or invested_weight_coverage_pct >= 85.0
    decision = PUBLICATION_DECISION if publication_allowed else "blocked_pricing_coverage_too_weak"
    fx_status = None if fx is None else fx.status
    blocking_reasons = _build_blocking_reasons(
        holdings_count=holdings_count,
        fresh_count=fresh_count,
        coverage_count_pct=coverage_count_pct,
        invested_weight_coverage_pct=invested_weight_coverage_pct,
        unresolved=unresolved,
        fx_status=fx_status,
    )
    if blocking_reasons:
        publication_allowed = False
        decision = "blocked_pricing_gate_failed"

    pass_result = PricingPassResult(
        run_date=run_date,
        requested_close_date=requested_close_date,
        holdings_count=holdings_count,
        fresh_holdings_count=fresh_count,
        carried_forward_holdings_count=carried_forward_count,
        coverage_count_pct=coverage_count_pct,
        invested_weight_coverage_pct=invested_weight_coverage_pct,
        decision=decision,
        publication_allowed=publication_allowed,
        blocking_reasons=blocking_reasons,
        unresolved_tickers=unresolved,
        fx_basis=fx,
        prices=results,
        holdings=holding_snapshots,
        price_results=results,
    )

    audit_path = write_price_audit(args.pricing_dir, pass_result)

    if publication_allowed:
        print(
            f"PRICING_OK | requested_close={requested_close_date} | holdings={holdings_count} | "
            f"shortlist={len(shortlist)} | fresh={fresh_count} | carried={carried_forward_count} | "
            f"count_coverage={coverage_count_pct:.2f} | weight_coverage={invested_weight_coverage_pct:.2f} | "
            f"audit={audit_path}"
        )
        return

    message = (
        f"PRICING_BLOCKED | requested_close={requested_close_date} | holdings={holdings_count} | "
        f"shortlist={len(shortlist)} | fresh={fresh_count} | carried={carried_forward_count} | "
        f"count_coverage={coverage_count_pct:.2f} | weight_coverage={invested_weight_coverage_pct:.2f} | "
        f"audit={audit_path} | reasons={' ; '.join(blocking_reasons)}"
    )
    print(message)
    if not args.allow_partial:
        raise SystemExit(message)
    sys.exit(0)


if __name__ == "__main__":
    main()
