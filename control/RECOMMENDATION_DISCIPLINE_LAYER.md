# ETF Review OS — Recommendation Discipline Layer

## Purpose

This file defines the recommendation-discipline model that hardens the Weekly ETF Review from a good narrative report into a capital-underwriting system.

It separates four layers:

1. **Decision framework** — how current holdings are re-underwritten.
2. **Input/state contract** — what machine-readable recommendation memory must persist.
3. **Output contract** — what compact client-facing blocks must appear in the report.
4. **Operational runbook** — what must validate before publication/state persistence.

---

## 1. Decision framework

### Capital Re-underwriting Layer

Every current holding must pass a capital re-underwriting check between:

- current position scoring, and
- final action table construction.

This layer answers one question:

> If the portfolio had cash today, would this position still deserve this amount of capital versus the best available alternative?

### Required tests per holding

| Test | Purpose | Allowed result |
|---|---|---|
| Fresh cash test | Would we put new capital into this holding today? | Yes / Smaller / No |
| Thesis vs implementation split | Separate structural thesis from ETF/price/trend implementation quality. | thesis_score + implementation_score |
| Relative alternative duel | If replaceable, name the best alternative and compare scores. | alternative ticker + score |
| Contribution / drag test | Identify whether position has helped or dragged portfolio performance. | contribution_pct |
| Factor-overlap test | Flag duplicated beta/factor exposure. | Yes / No |
| Exit / reduce / hold override logic | Force an override reason when holding a position that fails tests. | override_reason |

### Capital decision rules

- A position can remain **Hold** even if weak, but only with a named reason and next action.
- `Hold but replaceable` is not a final state; it must carry a next review action.
- A hedge can remain even with weak mark-to-market performance, but only if hedge validity is explicitly reaffirmed.
- Cash above 3% must have a reserve/deploy explanation.
- Major factor concentration must have an explicit portfolio-level note.

---

## 2. Input/state contract

The machine-readable recommendation memory file is:

```text
output/etf_recommendation_scorecard.csv
```

### Required schema

| Field | Purpose |
|---|---|
| report_date | Date of report |
| ticker | ETF ticker |
| weight_pct | Current weight |
| total_score | Current total score |
| thesis_score | Structural thesis score |
| implementation_score | ETF/price/trend score |
| fresh_cash_test | Yes / Smaller / No |
| replaceable_status | None / Under review / Replace candidate |
| weeks_replaceable | Inertia timer |
| best_alternative | Named alternative or None |
| alternative_score | Alternative score or blank |
| contribution_pct | Portfolio contribution estimate |
| factor_overlap_flag | Yes / No |
| required_next_action | Hold / Reduce / Close / Duel / Reprice |
| override_reason | Required if holding despite failed tests |

### Compatibility rule

Older reports may not contain all required fields. The builder may derive conservative defaults for the first transition cycle, but future reports should supply the fields explicitly.

---

## 3. Output contract

The premium report must remain compact. Add discipline without bloating the client experience.

### Section 5 or 6 — Portfolio discipline check

Add a compact table:

| Check | Result |
|---|---|
| Fresh cash test failures | tickers or None |
| Replaceable for >1 run | tickers or None |
| Hedge validity concern | tickers or None |
| Factor concentration concern | concise note |
| Cash deployment question | reserve/deploy explanation |

### Section 10 — Current position review

Each current position must include:

- Would buy today?
- Would buy at current weight?
- Best alternative:
- Required next action if under review:

### Section 13 — Final action table

Add or derive:

- Fresh Cash Test
- Best Alternative
- Required Next Review Action

---

## 4. Operational runbook

Before publishing or persisting state, require recommendation discipline validation.

### `RECOMMENDATION_DISCIPLINE_OK`

The discipline check passes only if:

- every `Hold but replaceable` has a named next action
- every weak hedge has a hedge-validity decision
- every position with a loss worse than 10% has a re-underwriting note
- every cash balance above 3% has a reserve/deploy explanation
- every major factor concentration has an explicit portfolio-level note

### Implementation sequence

1. Prompt/output contract first.
2. Scorecard schema second.
3. Validator third.
4. Workflow gate last.

### Current enforcement mode

- `validate_recommendation_discipline.py` validates the latest canonical English pro report and recommendation scorecard.
- The state-persistence workflow should run this validator before committing state artifacts.
- The production send workflow may run it in transition mode until all reports consistently include the new discipline block.

---

## Authority

This file is the durable design contract. The implementation lives in:

- `pricing/build_state_artifacts.py`
- `validate_recommendation_discipline.py`
- `.github/workflows/persist-etf-state-artifacts.yml`
- `.github/workflows/send-weekly-report.yml`
- `etf.txt`
- `etf-pro.txt`
