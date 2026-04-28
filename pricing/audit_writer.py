from __future__ import annotations

import json
from pathlib import Path

from .models import PricingPassResult


def _next_audit_path(output_dir: Path, requested_close_date: str) -> Path:
    compact_date = requested_close_date.replace("-", "")
    base = output_dir / f"price_audit_{compact_date}.json"
    if not base.exists():
        return base

    idx = 2
    while True:
        candidate = output_dir / f"price_audit_{compact_date}_{idx:02d}.json"
        if not candidate.exists():
            return candidate
        idx += 1


def write_price_audit(output_dir: str | Path, result: PricingPassResult) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = _next_audit_path(output_dir, result.requested_close_date)
    path.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return path
