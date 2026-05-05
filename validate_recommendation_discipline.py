from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Any

REPORT_RE = re.compile(r"^weekly_analysis_pro_(\d{6})(?:_(\d{2}))?\.md$")
SECTION_RE = re.compile(r"^##\s+(\d+)\.\s+(.*)$")
REQUIRED_SCORECARD_COLUMNS = [
    "report_date",
    "ticker",
    "weight_pct",
    "total_score",
    "thesis_score",
    "implementation_score",
    "fresh_cash_test",
    "replaceable_status",
    "weeks_replaceable",
    "best_alternative",
    "alternative_score",
    "contribution_pct",
    "factor_overlap_flag",
    "required_next_action",
    "override_reason",
]
FRESH_CASH_ALLOWED = {"Yes", "Smaller", "No"}
REPLACEABLE_ALLOWED = {"None", "Under review", "Replace candidate"}
NEXT_ACTION_ALLOWED = {"Hold", "Reduce", "Close", "Duel", "Reprice"}
YES_NO_ALLOWED = {"Yes", "No"}


def _clean(text: str | None) -> str:
    if text is None:
        return ""
    text = re.sub(r"\*\*|__|`", "", str(text))
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    return text.strip()


def _to_float(value: str | None) -> float | None:
    raw = _clean(value).replace(",", "").replace("%", "")
    if raw in {"", "-", "—", "None"}:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def latest_canonical_english_pro_report(output_dir: Path) -> Path:
    hits: list[tuple[str, int, Path]] = []
    for path in output_dir.glob("weekly_analysis_pro_*.md"):
        if path.name.startswith("weekly_analysis_pro_nl_"):
            continue
        match = REPORT_RE.match(path.name)
        if match:
            hits.append((match.group(1), int(match.group(2) or "1"), path))
    if not hits:
        raise RuntimeError("No canonical English ETF pro reports found in output/.")
    hits.sort(key=lambda item: (item[0], item[1]))
    return hits[-1][2]


def _section_lines(md_text: str, section_number: int) -> list[str]:
    out: list[str] = []
    in_section = False
    for line in md_text.splitlines():
        match = SECTION_RE.match(line.strip())
        if match:
            number = int(match.group(1))
            if number == section_number:
                in_section = True
                out.append(line)
                continue
            if in_section:
                break
        elif in_section:
            out.append(line)
    return out


def _section_text(md_text: str, section_number: int) -> str:
    return "\n".join(_section_lines(md_text, section_number))


def _parse_label_value_lines(lines: list[str]) -> dict[str, str]:
    pairs: dict[str, str] = {}
    for line in lines:
        s = _clean(line.strip())
        if s.startswith("-"):
            s = s.lstrip("- ").strip()
        if ":" in s:
            key, value = s.split(":", 1)
            pairs[_clean(key).lower()] = _clean(value)
    return pairs


def _parse_section15_summary(md_text: str) -> dict[str, float]:
    pairs = _parse_label_value_lines(_section_lines(md_text, 15))
    aliases = {
        "cash_eur": ["cash (eur)", "beschikbare cash (eur)"],
        "total_portfolio_value_eur": ["total portfolio value (eur)", "totale portefeuillewaarde (eur)"],
    }
    result: dict[str, float] = {}
    for key, names in aliases.items():
        for name in names:
            value = _to_float(pairs.get(name))
            if value is not None:
                result[key] = value
                break
    return result


def _parse_hold_but_replaceable(md_text: str) -> set[str]:
    section2 = _section_text(md_text, 2)
    lines = section2.splitlines()
    tickers: set[str] = set()
    in_block = False
    for line in lines:
        stripped = _clean(line)
        if stripped.lower().startswith("### hold but replaceable"):
            in_block = True
            continue
        if in_block and stripped.startswith("### "):
            break
        if in_block and stripped.startswith("-"):
            payload = stripped.lstrip("- ").strip()
            if payload.lower() == "none":
                continue
            for token in re.split(r"[,;\s]+", payload):
                token = token.strip().upper()
                if re.fullmatch(r"[A-Z][A-Z0-9.-]{0,14}", token):
                    tickers.add(token)
    return tickers


def _has_portfolio_discipline_check(md_text: str) -> bool:
    text = md_text.lower()
    required = [
        "portfolio discipline check",
        "fresh cash test failures",
        "replaceable for >1 run",
        "hedge validity concern",
        "factor concentration concern",
        "cash deployment question",
    ]
    return all(token in text for token in required)


def _has_cash_explanation(md_text: str) -> bool:
    text = md_text.lower()
    return "cash deployment question" in text or "reserve" in text or "deploy" in text or "cash" in _section_text(md_text, 6).lower()


def _has_factor_concentration_note(md_text: str) -> bool:
    text = md_text.lower()
    return "factor concentration concern" in text or "factor concentration" in text or "concentration" in text


def _ticker_review_block(md_text: str, ticker: str) -> str:
    section10 = _section_text(md_text, 10)
    pattern = re.compile(rf"^###\s+{re.escape(ticker)}\b.*$", re.MULTILINE)
    match = pattern.search(section10)
    if not match:
        return ""
    start = match.start()
    next_match = re.search(r"^###\s+", section10[match.end():], flags=re.MULTILINE)
    if next_match:
        end = match.end() + next_match.start()
        return section10[start:end]
    return section10[start:]


def validate_report_discipline(md_text: str, *, strict_report_contract: bool = False) -> list[str]:
    errors: list[str] = []
    hold_replaceable = _parse_hold_but_replaceable(md_text)
    summary = _parse_section15_summary(md_text)
    cash = summary.get("cash_eur")
    total = summary.get("total_portfolio_value_eur")
    cash_pct = (cash / total * 100.0) if cash is not None and total else None

    if strict_report_contract and not _has_portfolio_discipline_check(md_text):
        errors.append("Missing compact Portfolio discipline check block with required rows.")

    if cash_pct is not None and cash_pct > 3.0 and not _has_cash_explanation(md_text):
        errors.append(f"Cash balance is above 3% ({cash_pct:.2f}%) but no reserve/deploy explanation was found.")

    if strict_report_contract and not _has_factor_concentration_note(md_text):
        errors.append("Missing portfolio-level factor concentration note.")

    for ticker in sorted(hold_replaceable):
        block = _ticker_review_block(md_text, ticker)
        if not block:
            errors.append(f"Hold but replaceable ticker {ticker} has no Section 10 review block.")
            continue
        lower = block.lower()
        if strict_report_contract:
            for phrase in [
                "would buy today",
                "would buy at current weight",
                "best alternative",
                "required next action",
            ]:
                if phrase not in lower:
                    errors.append(f"{ticker} is Hold but replaceable but Section 10 lacks '{phrase}'.")

    return errors


def read_scorecard(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise RuntimeError(f"Missing recommendation scorecard: {path}")
    with path.open("r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames or []
        missing = [col for col in REQUIRED_SCORECARD_COLUMNS if col not in fieldnames]
        if missing:
            raise RuntimeError("Recommendation scorecard missing required columns: " + ", ".join(missing))
        return list(reader)


def validate_scorecard(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    if not rows:
        errors.append("Recommendation scorecard contains no rows.")
        return errors

    for idx, row in enumerate(rows, start=2):
        ticker = _clean(row.get("ticker")) or f"row_{idx}"
        fresh = _clean(row.get("fresh_cash_test"))
        replaceable = _clean(row.get("replaceable_status"))
        factor_overlap = _clean(row.get("factor_overlap_flag"))
        next_action = _clean(row.get("required_next_action"))
        override = _clean(row.get("override_reason"))
        best_alt = _clean(row.get("best_alternative"))
        weeks = _to_float(row.get("weeks_replaceable"))
        weight = _to_float(row.get("weight_pct"))

        if fresh not in FRESH_CASH_ALLOWED:
            errors.append(f"{ticker}: invalid fresh_cash_test '{fresh}'.")
        if replaceable not in REPLACEABLE_ALLOWED:
            errors.append(f"{ticker}: invalid replaceable_status '{replaceable}'.")
        if factor_overlap not in YES_NO_ALLOWED:
            errors.append(f"{ticker}: invalid factor_overlap_flag '{factor_overlap}'.")
        if next_action not in NEXT_ACTION_ALLOWED:
            errors.append(f"{ticker}: invalid required_next_action '{next_action}'.")
        if weight is None:
            errors.append(f"{ticker}: weight_pct must be numeric.")

        if replaceable in {"Under review", "Replace candidate"}:
            if next_action not in {"Duel", "Reduce", "Close", "Reprice"}:
                errors.append(f"{ticker}: replaceable holding requires Duel/Reduce/Close/Reprice next action.")
            if not best_alt or best_alt.lower() == "none":
                errors.append(f"{ticker}: replaceable holding requires a named best_alternative.")
            if weeks is None:
                errors.append(f"{ticker}: replaceable holding requires numeric weeks_replaceable.")

        if fresh in {"Smaller", "No"} and next_action == "Hold" and not override:
            errors.append(f"{ticker}: Hold despite failed fresh cash test requires override_reason.")

        contribution = _to_float(row.get("contribution_pct"))
        if contribution is not None and contribution < -10.0 and not override:
            errors.append(f"{ticker}: >10% drag requires re-underwriting override_reason.")

    return errors


def validate(output_dir: Path, *, strict_report_contract: bool = False) -> None:
    report = latest_canonical_english_pro_report(output_dir)
    md_text = report.read_text(encoding="utf-8")
    scorecard_path = output_dir / "etf_recommendation_scorecard.csv"
    rows = read_scorecard(scorecard_path)

    errors = []
    errors.extend(validate_report_discipline(md_text, strict_report_contract=strict_report_contract))
    errors.extend(validate_scorecard(rows))

    if errors:
        raise RuntimeError("RECOMMENDATION_DISCIPLINE_FAILED | " + " ; ".join(errors))

    print(f"RECOMMENDATION_DISCIPLINE_OK | report={report.name} | scorecard={scorecard_path.name} | rows={len(rows)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--strict-report-contract", action="store_true")
    args = parser.parse_args()
    validate(Path(args.output_dir), strict_report_contract=args.strict_report_contract)


if __name__ == "__main__":
    main()
