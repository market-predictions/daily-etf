from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from .run_pricing_pass import latest_report_file

REPORT_RE = re.compile(r"^weekly_analysis_pro_(\d{6})(?:_(\d{2}))?\.md$")
PRICE_AUDIT_RE = re.compile(r"^price_audit_(\d{8})(?:_(\d{2}))?\.json$")
SECTION_RE = re.compile(r"^##\s+(\d+)\.")

SUMMARY_ALIASES = {
    "starting_capital_eur": ["starting capital (eur)", "startkapitaal (eur)"],
    "invested_market_value_eur": ["invested market value (eur)", "belegde marktwaarde (eur)"],
    "cash_eur": ["cash (eur)"],
    "total_portfolio_value_eur": ["total portfolio value (eur)", "totale portefeuillewaarde (eur)"],
    "since_inception_return_pct": ["since inception return (%)", "rendement sinds start (%)"],
    "eur_usd_used": ["eur/usd used", "eur/usd gebruikt"],
}


def _clean(value: str) -> str:
    value = re.sub(r"\*\*|__|`", "", value or "")
    value = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", value)
    return value.strip()


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None
    raw = _clean(value).replace(",", "").replace("%", "").strip()
    if not raw or raw in {"-", "—", "None"}:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", _clean(value).lower()).strip()


def _section_lines(md_text: str, section_number: int) -> list[str]:
    lines = md_text.splitlines()
    out: list[str] = []
    in_section = False
    for line in lines:
        match = SECTION_RE.match(line.strip())
        if match:
            current = int(match.group(1))
            if current == section_number:
                in_section = True
                out.append(line)
                continue
            if in_section:
                break
        elif in_section:
            out.append(line)
    return out


def _is_table_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2


def _is_separator_line(line: str) -> bool:
    stripped = line.strip().strip("|").replace("-", "").replace(":", "").replace(" ", "")
    return stripped == ""


def _first_table(lines: list[str]) -> list[list[str]]:
    i = 0
    while i + 1 < len(lines):
        if _is_table_line(lines[i]) and _is_separator_line(lines[i + 1]):
            block = [lines[i], lines[i + 1]]
            j = i + 2
            while j < len(lines) and _is_table_line(lines[j]):
                block.append(lines[j])
                j += 1
            rows: list[list[str]] = []
            for line in block:
                if _is_separator_line(line):
                    continue
                rows.append([_clean(cell) for cell in line.strip().strip("|").split("|")])
            return rows
        i += 1
    return []


def _rows_from_first_table(lines: list[str]) -> list[dict[str, str]]:
    rows = _first_table(lines)
    if len(rows) < 2:
        return []
    headers = [_norm(h) for h in rows[0]]
    parsed: list[dict[str, str]] = []
    for row in rows[1:]:
        padded = row + [""] * (len(headers) - len(row))
        parsed.append({headers[idx]: padded[idx] for idx in range(len(headers))})
    return parsed


def _parse_summary(lines: list[str]) -> dict[str, float]:
    pairs: dict[str, str] = {}
    for line in lines:
        stripped = _clean(line.strip())
        if stripped.startswith("-"):
            stripped = stripped.lstrip("- ").strip()
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        pairs[_norm(key)] = value.strip()

    result: dict[str, float] = {}
    for canonical, aliases in SUMMARY_ALIASES.items():
        for alias in aliases:
            if alias in pairs:
                value = _to_float(pairs[alias])
                if value is not None:
                    result[canonical] = value
                break
    return result


def _latest_price_audit(pricing_dir: Path) -> tuple[Path | None, dict[str, Any] | None]:
    hits: list[tuple[str, int, Path]] = []
    for path in pricing_dir.glob("price_audit_*.json"):
        match = PRICE_AUDIT_RE.match(path.name)
        if match:
            hits.append((match.group(1), int(match.group(2) or "1"), path))
    if not hits:
        return None, None
    hits.sort(key=lambda item: (item[0], item[1]))
    latest = hits[-1][2]
    return latest, json.loads(latest.read_text(encoding="utf-8"))


def _report_identity(report_path: Path) -> tuple[str, int]:
    match = REPORT_RE.match(report_path.name)
    if not match:
        raise RuntimeError(f"Unsupported report filename for state artifact builder: {report_path.name}")
    return match.group(1), int(match.group(2) or "1")


def parse_portfolio_state(report_path: Path, audit_path: Path | None, audit: dict[str, Any] | None) -> dict[str, Any]:
    md_text = report_path.read_text(encoding="utf-8")
    token, version = _report_identity(report_path)
    section15 = _section_lines(md_text, 15)
    section16 = _section_lines(md_text, 16)
    summary = _parse_summary(section15)
    rows15 = _rows_from_first_table(section15)
    rows16 = _rows_from_first_table(section16)

    positions: list[dict[str, Any]] = []
    continuity_by_ticker = {(_clean(row.get("ticker", "")).upper()): row for row in rows16 if row.get("ticker")}
    audit_prices = {str(row.get("symbol", "")).upper(): row for row in (audit or {}).get("price_results", [])}

    for row in rows15:
        ticker = _clean(row.get("ticker", "")).upper()
        if not ticker:
            continue
        continuity = continuity_by_ticker.get(ticker, {})
        price_audit = audit_prices.get(ticker, {})
        positions.append(
            {
                "ticker": ticker,
                "shares": _to_float(row.get("shares")),
                "price_local": _to_float(row.get("price (local)")),
                "currency": _clean(row.get("currency", "")) or None,
                "market_value_local": _to_float(row.get("market value (local)")),
                "market_value_eur": _to_float(row.get("market value (eur)")),
                "weight_pct": _to_float(row.get("weight %")),
                "direction": _clean(continuity.get("direction", "")) or ("Cash" if ticker == "CASH" else "Long"),
                "avg_entry": _to_float(continuity.get("avg entry")),
                "current_price": _to_float(continuity.get("current price")),
                "pl_pct": _to_float(continuity.get("p/l %")),
                "original_thesis": _clean(continuity.get("original thesis", "")) or None,
                "role": _clean(continuity.get("role", "")) or None,
                "pricing_status": price_audit.get("status"),
                "pricing_source": price_audit.get("source"),
                "pricing_returned_close_date": price_audit.get("returned_close_date"),
            }
        )

    state = {
        "schema_version": "1.0",
        "generated_at": date.today().isoformat(),
        "report_filename": report_path.name,
        "report_token": token,
        "report_version": version,
        "base_currency": "EUR",
        "source_authority": "report_section_15_with_pricing_audit_overlay",
        "pricing_basis": {
            "audit_file": None if audit_path is None else str(audit_path),
            "run_date": None if audit is None else audit.get("run_date"),
            "requested_close_date": None if audit is None else audit.get("requested_close_date"),
            "decision": None if audit is None else audit.get("decision"),
            "publication_allowed": None if audit is None else audit.get("publication_allowed"),
            "coverage_count_pct": None if audit is None else audit.get("coverage_count_pct"),
            "invested_weight_coverage_pct": None if audit is None else audit.get("invested_weight_coverage_pct"),
            "fx_basis": None if audit is None else audit.get("fx_basis"),
        },
        "summary": summary,
        "positions": positions,
        "constraints": _parse_constraints(section16),
    }
    return state


def _parse_constraints(section16: list[str]) -> dict[str, str]:
    constraints: dict[str, str] = {}
    in_constraints = False
    for line in section16:
        stripped = _clean(line.strip())
        if stripped.startswith("### Constraints"):
            in_constraints = True
            continue
        if in_constraints and stripped.startswith("### "):
            break
        if in_constraints and stripped.startswith("-") and ":" in stripped:
            key, value = stripped.lstrip("- ").split(":", 1)
            constraints[_norm(key).replace(" ", "_").replace("/", "_")] = value.strip()
    return constraints


def parse_scorecard(report_path: Path) -> list[dict[str, Any]]:
    rows = _rows_from_first_table(_section_lines(report_path.read_text(encoding="utf-8"), 13))
    out: list[dict[str, Any]] = []
    for row in rows:
        ticker = _clean(row.get("ticker", "")).upper()
        if not ticker:
            continue
        out.append(
            {
                "ticker": ticker,
                "etf": _clean(row.get("etf", "")) or None,
                "existing_new": _clean(row.get("existing/new", "")) or None,
                "weight_inherited_pct": _to_float(row.get("weight inherited")),
                "target_weight_pct": _to_float(row.get("target weight")),
                "suggested_action": _clean(row.get("suggested action", "")) or None,
                "conviction_tier": _clean(row.get("conviction tier", "")) or None,
                "total_score": _to_float(row.get("total score")),
                "portfolio_role": _clean(row.get("portfolio role", "")) or None,
                "better_alternative_exists": _clean(row.get("better alternative exists?", "")) or None,
                "short_reason": _clean(row.get("short reason", "")) or None,
            }
        )
    return out


def parse_trade_ledger(report_path: Path) -> list[dict[str, Any]]:
    rows = _rows_from_first_table(_section_lines(report_path.read_text(encoding="utf-8"), 14))
    out: list[dict[str, Any]] = []
    for row in rows:
        ticker = _clean(row.get("ticker", "")).upper()
        if not ticker:
            continue
        out.append(
            {
                "ticker": ticker,
                "previous_weight_pct": _to_float(row.get("previous weight %")),
                "new_weight_pct": _to_float(row.get("new weight %")),
                "weight_change_pct": _to_float(row.get("weight change %")),
                "shares_delta": _to_float(row.get("shares delta")),
                "action_executed": _clean(row.get("action executed", "")) or None,
                "funding_source_note": _clean(row.get("funding source / note", "")) or None,
            }
        )
    return out


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in fieldnames})


def write_artifacts(output_dir: Path, state: dict[str, Any], scorecard: list[dict[str, Any]], trade_rows: list[dict[str, Any]]) -> dict[str, Path]:
    state_path = output_dir / "etf_portfolio_state.json"
    scorecard_path = output_dir / "etf_recommendation_scorecard.csv"
    trade_ledger_path = output_dir / "etf_trade_ledger.csv"
    valuation_history_path = output_dir / "etf_valuation_history.csv"

    _write_json(state_path, state)

    _write_csv(
        scorecard_path,
        scorecard,
        [
            "ticker",
            "etf",
            "existing_new",
            "weight_inherited_pct",
            "target_weight_pct",
            "suggested_action",
            "conviction_tier",
            "total_score",
            "portfolio_role",
            "better_alternative_exists",
            "short_reason",
        ],
    )

    _write_csv(
        trade_ledger_path,
        trade_rows,
        [
            "ticker",
            "previous_weight_pct",
            "new_weight_pct",
            "weight_change_pct",
            "shares_delta",
            "action_executed",
            "funding_source_note",
        ],
    )

    valuation_row = {
        "report_filename": state.get("report_filename"),
        "report_token": state.get("report_token"),
        "requested_close_date": (state.get("pricing_basis") or {}).get("requested_close_date"),
        "total_portfolio_value_eur": (state.get("summary") or {}).get("total_portfolio_value_eur"),
        "cash_eur": (state.get("summary") or {}).get("cash_eur"),
        "since_inception_return_pct": (state.get("summary") or {}).get("since_inception_return_pct"),
        "pricing_audit_file": (state.get("pricing_basis") or {}).get("audit_file"),
    }
    _write_csv(
        valuation_history_path,
        [valuation_row],
        [
            "report_filename",
            "report_token",
            "requested_close_date",
            "total_portfolio_value_eur",
            "cash_eur",
            "since_inception_return_pct",
            "pricing_audit_file",
        ],
    )

    return {
        "state": state_path,
        "scorecard": scorecard_path,
        "trade_ledger": trade_ledger_path,
        "valuation_history": valuation_history_path,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--pricing-dir", default="output/pricing")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    pricing_dir = Path(args.pricing_dir)
    report_path = latest_report_file(output_dir)
    audit_path, audit = _latest_price_audit(pricing_dir)

    state = parse_portfolio_state(report_path, audit_path, audit)
    scorecard = parse_scorecard(report_path)
    trade_rows = parse_trade_ledger(report_path)
    paths = write_artifacts(output_dir, state, scorecard, trade_rows)

    print(
        "ETF_STATE_ARTIFACTS_OK | "
        f"report={report_path.name} | "
        f"state={paths['state'].name} | scorecard={paths['scorecard'].name} | "
        f"trade_ledger={paths['trade_ledger'].name} | valuation_history={paths['valuation_history'].name} | "
        f"pricing_audit={audit_path.name if audit_path else 'none'}"
    )


if __name__ == "__main__":
    main()
