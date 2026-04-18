from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Literal, Optional, Any

PriceStatus = Literal[
    "fresh_close",
    "fresh_fallback_source",
    "carried_forward",
    "unresolved",
]

SymbolKind = Literal[
    "holding",
    "radar_primary",
    "radar_alternative",
    "challenger",
    "fx",
]

Confidence = Literal["high", "medium", "low"]


@dataclass(slots=True)
class HoldingSnapshot:
    ticker: str
    shares: float
    previous_price_local: Optional[float]
    currency: str
    previous_market_value_local: Optional[float]
    previous_market_value_eur: Optional[float]
    previous_weight_pct: Optional[float]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ShortlistItem:
    symbol: str
    kind: SymbolKind
    priority: int
    note: str = ""


@dataclass(slots=True)
class PriceRequest:
    symbol: str
    requested_close_date: str
    kind: SymbolKind
    currency_hint: str = "USD"


@dataclass(slots=True)
class PriceResult:
    symbol: str
    requested_close_date: str
    returned_close_date: Optional[str]
    price: Optional[float]
    currency: Optional[str]
    source: Optional[str]
    source_detail: Optional[str]
    field_used: Optional[str]
    status: PriceStatus
    confidence: Confidence
    carried_forward: bool = False
    error: Optional[str] = None
    metadata: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class FXResult:
    pair: str
    requested_date: str
    returned_date: Optional[str]
    rate: Optional[float]
    source: Optional[str]
    status: PriceStatus
    error: Optional[str] = None
    metadata: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class QuotaStatus:
    source: str
    daily_limit: int
    reserve_daily: int
    spent_today: int
    remaining_today: int
    can_spend: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PricingPassResult:
    run_date: str
    requested_close_date: str
    holdings_count: int
    fresh_holdings_count: int
    coverage_count_pct: float
    invested_weight_coverage_pct: float
    decision: str
    unresolved_tickers: list[str]
    fx_basis: Optional[FXResult]
    prices: list[PriceResult]
    holdings: list[HoldingSnapshot] = field(default_factory=list)
    price_results: list[PriceResult] = field(default_factory=list)
    carried_forward_holdings_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        effective_price_results = self.price_results or self.prices
        return {
            "run_date": self.run_date,
            "requested_close_date": self.requested_close_date,
            "holdings_count": self.holdings_count,
            "fresh_holdings_count": self.fresh_holdings_count,
            "carried_forward_holdings_count": self.carried_forward_holdings_count,
            "coverage_count_pct": self.coverage_count_pct,
            "invested_weight_coverage_pct": self.invested_weight_coverage_pct,
            "decision": self.decision,
            "unresolved_tickers": self.unresolved_tickers,
            "fx_basis": None if self.fx_basis is None else self.fx_basis.to_dict(),
            "holdings": [h.to_dict() for h in self.holdings],
            "prices": [p.to_dict() for p in self.prices],
            "price_results": [p.to_dict() for p in effective_price_results],
        }
