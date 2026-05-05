# ETF Review OS — Current State

## Snapshot date
2026-05-05

## What this repository currently is

This repository is a production-style Weekly ETF Review system with:

- production masterprompt in `etf.txt`
- recommendation-discipline addendum in `control/ETF_MASTERPROMPT_RECOMMENDATION_DISCIPLINE_ADDENDUM.md`
- premium English editorial layer in `etf-pro.txt`
- Dutch premium companion layer in `etf-pro-nl.txt`
- delivery/rendering script in `send_report.py`
- production GitHub Actions workflow for execution and bilingual email delivery
- companion GitHub Actions workflow for ETF state artifact persistence
- non-email validation workflow for runtime/pricing/render changes
- pricing subsystem in `pricing/`
- pricing audit output in `output/pricing/`
- lane-assessment artifact folder in `output/lane_reviews/`
- explicit ETF state artifact builder in `pricing/build_state_artifacts.py`
- state validator in `validate_etf_state_artifacts.py`
- lane breadth validator in `validate_lane_breadth.py`
- recommendation discipline validator in `validate_recommendation_discipline.py`
- control layer in `control/`
- split-test scaffold in `prompts/as_is_split/`

GitHub remains the source of truth for prompts, scripts, workflows, outputs, and control docs.

---

## Current production architecture

### Decision framework

The ETF review now has four active decision layers:

1. macro/geopolitical regime classification
2. broad lane discovery and compact live-radar publication
3. current position scoring
4. **Capital Re-underwriting Layer**

The Capital Re-underwriting Layer requires every current holding to be assessed through:

- fresh cash test
- thesis vs implementation split
- relative alternative duel when replaceable
- contribution / drag test
- factor-overlap test
- exit / reduce / hold override logic

This layer is documented in:

- `control/RECOMMENDATION_DISCIPLINE_LAYER.md`
- `control/ETF_MASTERPROMPT_RECOMMENDATION_DISCIPLINE_ADDENDUM.md`

### Input/state contract

The explicit state layer includes:

- `output/etf_portfolio_state.json`
- `output/etf_trade_ledger.csv`
- `output/etf_valuation_history.csv`
- `output/etf_recommendation_scorecard.csv`

The recommendation scorecard now targets the expanded recommendation discipline schema:

```text
report_date
ticker
weight_pct
total_score
thesis_score
implementation_score
fresh_cash_test
replaceable_status
weeks_replaceable
best_alternative
alternative_score
contribution_pct
factor_overlap_flag
required_next_action
override_reason
```

State artifacts are built by:

```bash
python -m pricing.build_state_artifacts
```

and validated by:

```bash
python validate_etf_state_artifacts.py
python validate_recommendation_discipline.py
```

### Output contract

The premium report must preserve the existing 17-section structure and now also include a compact recommendation-discipline output contract.

Required additions:

- Section 5 or 6: **Portfolio discipline check**
- Section 10 per position:
  - Would buy today?
  - Would buy at current weight?
  - Best alternative:
  - Required next action if under review:
- Section 13 final action table must include or derive:
  - Fresh Cash Test
  - Best Alternative
  - Required Next Review Action

The English pro editorial layer has been updated in `etf-pro.txt` to preserve these fields rather than smoothing them away.

### Operational runbook

The production send workflow now keeps the existing gates and adds the strict recommendation-discipline gate before email delivery.

Current pre-send gate sequence includes:

```bash
python -m pricing.run_pricing_pass
python validate_lane_breadth.py
# English/Dutch pair validation through send_report.py helpers
# HTML/PDF render validation through send_report.py helpers
python -m pricing.build_state_artifacts
python validate_etf_state_artifacts.py
python validate_recommendation_discipline.py --strict-report-contract
python send_report.py
```

The companion state workflow also validates recommendation discipline before committing state artifacts back to `main`.

---

## Current strengths

- Executive ETF report look & feel is still preserved.
- English canonical plus Dutch companion delivery remains the active bilingual pattern.
- Pricing audit is explicit and persisted.
- Lane breadth is explicit through a matching lane artifact.
- State artifacts are explicit and machine-readable.
- Recommendation discipline is now machine-readable and validator-backed.
- `send_report.py` now imports `delivery_base.py` first with `send_report_OLD.py` fallback.
- Cleanup classification exists in `control/REPO_FILE_CLASSIFICATION.md`.
- Cleanup progress is recorded in `control/CLEANUP_PROGRESS.md`.
- Production send is gated by pricing, breadth, bilingual parity, render, state, and recommendation discipline.

---

## Current risks / watchpoints

### 1. `etf.txt` monolith still exists

`etf.txt` remains a large production masterprompt. The recommendation discipline layer is currently added through:

```text
control/ETF_MASTERPROMPT_RECOMMENDATION_DISCIPLINE_ADDENDUM.md
```

This was deliberate to avoid unsafe partial overwrite of the large masterprompt file. The addendum must be treated as active prompt authority until safely folded into `etf.txt`.

### 2. Strict send gate can block reports that omit new discipline fields

The production workflow now runs:

```bash
python validate_recommendation_discipline.py --strict-report-contract
```

before email delivery.

This is desired, but it means the next report must include the new Portfolio discipline check and Section 10/13 discipline fields.

### 3. State artifacts still need a successful post-discipline production confirmation

After merging the recommendation discipline PR, the next production run must confirm:

- strict recommendation discipline passes
- generated `output/etf_recommendation_scorecard.csv` uses the expanded schema
- state artifacts persist back to `main`
- bilingual render and email delivery remain intact

### 4. `send_report_OLD.py` remains protected

Do not delete `send_report_OLD.py` until at least one successful production cycle has passed after the `delivery_base` transition and the recommendation-discipline send gate.

---

## Immediate priorities

### Priority A — merge and validate recommendation discipline PR

Required:

- merge PR #13 after review
- run validation workflow if available
- run a fresh production cycle that includes the new discipline report block

### Priority B — confirm strict report contract in real output

Confirm the next report contains:

- Portfolio discipline check
- buy-today / current-weight / best-alternative / next-action fields per position
- expanded Section 13 table with Fresh Cash Test, Best Alternative, Required Next Review Action

### Priority C — confirm state persistence

Confirm after successful delivery:

- `persist-etf-state-artifacts.yml` runs
- `output/etf_recommendation_scorecard.csv` is committed with expanded schema
- `validate_recommendation_discipline.py` prints `RECOMMENDATION_DISCIPLINE_OK`

### Priority D — cleanup after successful production cycle

Only after a successful production cycle:

- consider converting or deleting `send_report_OLD.py`
- prune generated delivery derivatives according to `control/REPO_FILE_CLASSIFICATION.md`

---

## Recommended session start sequence

For any future ETF architecture session:

1. read `control/SYSTEM_INDEX.md`
2. read this file
3. read `control/NEXT_ACTIONS.md`
4. only then open the specific execution file relevant to the task

---

## Current status label

**ETF now has explicit pricing, lane breadth, state artifacts, bilingual delivery, cleanup classification, and recommendation discipline. The next proof point is a successful production run that passes strict recommendation-discipline validation before subscriber delivery and persists the expanded recommendation scorecard back to `main`.**
