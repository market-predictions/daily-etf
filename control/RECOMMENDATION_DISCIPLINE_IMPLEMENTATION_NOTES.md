# Recommendation Discipline Layer — Implementation Notes

## Implemented in this PR

This PR introduces the first enforceable recommendation discipline layer without immediately risking subscriber delivery.

### Added

- `control/RECOMMENDATION_DISCIPLINE_LAYER.md`
- `validate_recommendation_discipline.py`

### Updated

- `pricing/build_state_artifacts.py`
- `validate_etf_state_artifacts.py`
- `.github/workflows/persist-etf-state-artifacts.yml`

## What is now enforced

### Machine-readable recommendation memory

`output/etf_recommendation_scorecard.csv` now uses the expanded recommendation discipline schema:

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

### Validator

`validate_recommendation_discipline.py` validates:

- required schema columns
- allowed values for `fresh_cash_test`, `replaceable_status`, `factor_overlap_flag`, and `required_next_action`
- replaceable positions requiring a non-passive next action
- replaceable positions requiring a named `best_alternative`
- failed fresh cash tests requiring override logic when still held
- large negative contribution requiring re-underwriting explanation
- cash above 3% requiring a reserve/deploy explanation

### Workflow gate

`persist-etf-state-artifacts.yml` now runs:

```bash
python validate_recommendation_discipline.py
```

before committing generated state artifacts back to `main`.

This means the state layer cannot silently persist a structurally incomplete recommendation scorecard.

## Deliberate transition choice

The production send workflow is not yet blocked by `--strict-report-contract`.

Reason:

- existing production reports do not yet contain the full compact `Portfolio discipline check` block
- the safe migration path is to first enforce the machine-readable state layer
- the next report-generation prompt update should make the client-facing discipline block mandatory
- after one passing production cycle with the new report block, the send workflow can be hardened to strict mode

## Still pending

### Prompt/output contract hardening

The following still needs to be promoted directly into `etf.txt` and `etf-pro.txt`:

- mandatory Capital Re-underwriting Layer
- Section 5 or 6 `Portfolio discipline check`
- Section 10 per-position fields:
  - Would buy today?
  - Would buy at current weight?
  - Best alternative:
  - Required next action if under review:
- Section 13 columns:
  - Fresh Cash Test
  - Best Alternative
  - Required Next Review Action

### Production send gate

After the next report includes the client-facing discipline block, add a strict pre-send validation step:

```bash
python validate_recommendation_discipline.py --strict-report-contract
```

## Safety boundary

Do not delete or weaken existing pricing, lane-breadth, bilingual, render, delivery, or state validations while rolling this out.
