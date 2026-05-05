from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

RECOMMENDATION_SCORECARD_REQUIRED_COLUMNS = [
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


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise RuntimeError(f"Missing required ETF state artifact: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not path.exists():
        raise RuntimeError(f"Missing required ETF state artifact: {path}")
    with path.open("r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader), list(reader.fieldnames or [])


def _num(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except Exception:
        return None


def _validate_recommendation_scorecard_schema(rows: list[dict[str, str]], columns: list[str]) -> None:
    missing = [col for col in RECOMMENDATION_SCORECARD_REQUIRED_COLUMNS if col not in columns]
    if missing:
        raise RuntimeError("ETF recommendation scorecard missing required discipline columns: " + ", ".join(missing))
    if not rows:
        raise RuntimeError("ETF recommendation scorecard contains no rows.")
    allowed_fresh = {"Yes", "Smaller", "No"}
    allowed_replaceable = {"None", "Under review", "Replace candidate"}
    allowed_next = {"Hold", "Reduce", "Close", "Duel", "Reprice"}
    allowed_yes_no = {"Yes", "No"}
    for row in rows:
        ticker = str(row.get("ticker") or "UNKNOWN").upper()
        if row.get("fresh_cash_test") not in allowed_fresh:
            raise RuntimeError(f"ETF recommendation scorecard invalid fresh_cash_test for {ticker}: {row.get('fresh_cash_test')}")
        if row.get("replaceable_status") not in allowed_replaceable:
            raise RuntimeError(f"ETF recommendation scorecard invalid replaceable_status for {ticker}: {row.get('replaceable_status')}")
        if row.get("factor_overlap_flag") not in allowed_yes_no:
            raise RuntimeError(f"ETF recommendation scorecard invalid factor_overlap_flag for {ticker}: {row.get('factor_overlap_flag')}")
        if row.get("required_next_action") not in allowed_next:
            raise RuntimeError(f"ETF recommendation scorecard invalid required_next_action for {ticker}: {row.get('required_next_action')}")


def validate_state(output_dir: Path = Path("output"), tolerance: float = 0.05) -> None:
    state_path = output_dir / "etf_portfolio_state.json"
    valuation_path = output_dir / "etf_valuation_history.csv"
    scorecard_path = output_dir / "etf_recommendation_scorecard.csv"
    trade_ledger_path = output_dir / "etf_trade_ledger.csv"

    state = _read_json(state_path)
    valuation_rows, _ = _read_csv(valuation_path)
    scorecard_rows, scorecard_columns = _read_csv(scorecard_path)
    _read_csv(trade_ledger_path)

    if not state.get("report_filename"):
        raise RuntimeError("ETF state artifact missing report_filename.")
    if not state.get("positions"):
        raise RuntimeError("ETF state artifact contains no positions.")

    summary = state.get("summary") or {}
    total = _num(summary.get("total_portfolio_value_eur"))
    cash = _num(summary.get("cash_eur"))
    invested = _num(summary.get("invested_market_value_eur"))
    if total is None or cash is None or invested is None:
        raise RuntimeError("ETF state summary is missing total/cash/invested numeric values.")

    summed_positions = 0.0
    for pos in state.get("positions") or []:
        mv = _num(pos.get("market_value_eur"))
        ticker = str(pos.get("ticker") or "UNKNOWN")
        if mv is None:
            raise RuntimeError(f"ETF state position has non-numeric market_value_eur: {ticker}")
        summed_positions += mv

    if abs(summed_positions - total) > tolerance:
        raise RuntimeError(
            f"ETF state position sum does not reconcile with total NAV: positions={summed_positions:.2f} total={total:.2f}"
        )
    if abs((invested + cash) - total) > tolerance:
        raise RuntimeError(
            f"ETF state invested+cash does not reconcile: invested={invested:.2f} cash={cash:.2f} total={total:.2f}"
        )

    if not valuation_rows:
        raise RuntimeError("ETF valuation history is empty.")
    latest_valuation = valuation_rows[-1]
    valuation_total = _num(latest_valuation.get("total_portfolio_value_eur"))
    if valuation_total is None or abs(valuation_total - total) > tolerance:
        raise RuntimeError("ETF valuation history latest row does not reconcile with ETF state total NAV.")

    _validate_recommendation_scorecard_schema(scorecard_rows, scorecard_columns)

    state_tickers = {str(pos.get("ticker") or "").upper() for pos in state.get("positions") or [] if str(pos.get("ticker") or "").upper() != "CASH"}
    scorecard_tickers = {str(row.get("ticker") or "").upper() for row in scorecard_rows if str(row.get("ticker") or "").upper() != "CASH"}
    if state_tickers and not state_tickers.issubset(scorecard_tickers):
        missing = state_tickers - scorecard_tickers
        raise RuntimeError("ETF scorecard/state ticker set could not be reconciled. Missing: " + ", ".join(sorted(missing)))

    print(
        "ETF_STATE_ARTIFACTS_VALIDATION_OK | "
        f"state={state_path.name} | valuation={valuation_path.name} | "
        f"scorecard={scorecard_path.name} | trade_ledger={trade_ledger_path.name} | "
        f"total_portfolio_value_eur={total:.2f} | recommendation_schema=ok"
    )


if __name__ == "__main__":
    validate_state()
