from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from pricing.models import PriceResult


class PricingCache:
    """Simple per-day JSON cache for pricing results.

    Cache keys are `{source}:{symbol}:{requested_close_date}` so the same
    symbol can be stored multiple times if it was resolved by different sources.
    """

    def __init__(self, run_date: str, base_dir: str = "output/pricing") -> None:
        self.run_date = run_date
        self.base_path = Path(base_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.cache_path = self.base_path / f"price_cache_{run_date}.json"
        self._data: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.cache_path.exists():
            return {"results": {}}
        try:
            return json.loads(self.cache_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"results": {}}

    def save(self) -> None:
        self.cache_path.write_text(
            json.dumps(self._data, indent=2, sort_keys=True),
            encoding="utf-8",
        )

    @staticmethod
    def make_key(source: str, symbol: str, requested_close_date: str) -> str:
        return f"{source}:{symbol.upper()}:{requested_close_date}"

    def get(self, source: str, symbol: str, requested_close_date: str) -> Optional[dict[str, Any]]:
        key = self.make_key(source, symbol, requested_close_date)
        return self._data.get("results", {}).get(key)

    def put(self, result: PriceResult) -> None:
        if not result.source:
            return
        key = self.make_key(result.source, result.symbol, result.requested_close_date)
        self._data.setdefault("results", {})[key] = {
            "symbol": result.symbol,
            "requested_close_date": result.requested_close_date,
            "returned_close_date": result.returned_close_date,
            "price": result.price,
            "currency": result.currency,
            "source": result.source,
            "source_detail": result.source_detail,
            "field_used": result.field_used,
            "status": result.status,
            "confidence": result.confidence,
            "carried_forward": result.carried_forward,
            "error": result.error,
            "metadata": result.metadata,
        }
        self.save()
