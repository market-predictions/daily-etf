# ETF Review OS — Cleanup Progress

## Purpose

This file records repo-cleanup milestones that have already been implemented and validated, so future sessions do not need to rediscover the cleanup state.

For the cleanup authority and file classifications, use:

- `control/REPO_FILE_CLASSIFICATION.md`

---

## 2026-05-05 — Repo cleanup foundation implemented

### Completed

- Added `control/REPO_FILE_CLASSIFICATION.md` as the cleanup authority.
- Added `delivery_base.py` as a clearer compatibility wrapper around the historical delivery base implementation.
- Updated `send_report.py` so it now prefers `delivery_base` and falls back to `send_report_OLD.py`.
- Updated `.github/workflows/validate-etf-runtime.yml` so changes to `delivery_base.py` and `send_report_OLD.py` trigger runtime validation.

### Validation evidence

Manual GitHub Actions validation was run through:

- `Validate ETF runtime changes #3`
- Trigger: `workflow_dispatch`
- Status: `Success`
- Duration shown in GitHub UI: `1m 58s`

This validates the delivery-base import transition at runtime without subscriber email delivery.

### Files still protected

Do not delete yet:

- `send_report_OLD.py`

Reason:

- It remains the fallback delivery base until at least one normal production Weekly ETF Review cycle has completed successfully after the `delivery_base` import transition.

### Next cleanup gate

Before deleting or converting `send_report_OLD.py`, complete one successful production cycle that confirms:

1. pricing pass succeeds
2. lane breadth validation succeeds
3. English/Dutch pair validation succeeds when a Dutch companion exists
4. HTML/PDF render succeeds
5. email delivery succeeds with real manifest/receipt evidence
6. no regression appears in the executive report look & feel

Only after that, create a separate cleanup PR to either:

- convert `send_report_OLD.py` into a tiny backward-compatibility shim, or
- delete it if no code path imports it anymore.

---

## Current cleanup state

```text
Phase 1 — repo file classification                  DONE
Phase 2 — delivery_base compatibility wrapper        DONE
Phase 3 — send_report imports delivery_base first    DONE
Phase 4 — validation-only runtime check              DONE
Phase 5 — one successful production cycle            PENDING
Phase 6 — remove/convert send_report_OLD.py          BLOCKED until Phase 5
Phase 7 — prune generated delivery derivatives       PENDING
```

---

## Cleanup candidates after Phase 5

Review these after the next successful production cycle:

```text
output/*_clean.md
output/*_delivery.html
output/*.pdf
output/*_equity_curve.png
output/pricing/price_cache_*.json
```

Do not prune canonical production/audit/state files unless the cleanup authority explicitly changes:

```text
output/weekly_analysis_pro_*.md
output/weekly_analysis_pro_nl_*.md
output/pricing/price_audit_*.json
output/lane_reviews/etf_lane_assessment_*.json
output/etf_portfolio_state.json
output/etf_trade_ledger.csv
output/etf_valuation_history.csv
output/etf_recommendation_scorecard.csv
```
