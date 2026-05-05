# ETF Masterprompt Addendum — Recommendation Discipline

## Authority

This addendum extends `etf.txt` and must be treated as part of the active internal masterprompt until its content is safely folded into the large prompt file.

Reason for separate file:

- `etf.txt` is large and should not be partially overwritten through unsafe tooling.
- This file preserves deterministic behavior while avoiding corruption of the current production masterprompt.

---

## Insert after current-position scoring and before final action table construction

# Capital Re-underwriting Layer

Every current holding must pass a capital re-underwriting layer after position scoring and before the final action table.

The question is:

> If the portfolio had fresh cash today, would this position still deserve this amount of capital versus the best available alternative?

For every current holding, evaluate and record:

1. **Fresh cash test**
   - `Yes` = would buy today at roughly current or target weight
   - `Smaller` = would still own, but not at current size
   - `No` = would not allocate fresh capital today

2. **Thesis vs implementation split**
   - thesis_score = structural thesis quality
   - implementation_score = ETF quality, price/trend, liquidity, timing, and implementation fit

3. **Relative alternative duel**
   - if the holding is `Hold but replaceable`, name the best alternative
   - compare the holding score and alternative score
   - assign a required next action

4. **Contribution / drag test**
   - identify whether the position has contributed or dragged since entry
   - every position with loss worse than 10% requires a re-underwriting note

5. **Factor-overlap test**
   - flag major duplicated factor exposure
   - especially broad beta + growth/AI overlap, rate sensitivity, commodity sensitivity, or hedge duplication

6. **Exit / reduce / hold override logic**
   - a failed fresh cash test may still result in Hold only with an explicit override reason
   - every `Hold but replaceable` must have a named next action

---

## Required internal recommendation scorecard fields

Every run must create or update machine-readable recommendation memory at:

```text
output/etf_recommendation_scorecard.csv
```

with this schema:

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

Allowed values:

- fresh_cash_test: `Yes`, `Smaller`, `No`
- replaceable_status: `None`, `Under review`, `Replace candidate`
- factor_overlap_flag: `Yes`, `No`
- required_next_action: `Hold`, `Reduce`, `Close`, `Duel`, `Reprice`

---

## Required client-facing report additions

### Section 5 or 6 — Portfolio discipline check

Add a compact table titled exactly:

**Portfolio discipline check**

| Check | Result |
|---|---|
| Fresh cash test failures | tickers or None |
| Replaceable for >1 run | tickers or None |
| Hedge validity concern | tickers or None |
| Factor concentration concern | concise note |
| Cash deployment question | reserve/deploy explanation |

### Section 10 — Current Position Review

For each current position, include:

- Would buy today?
- Would buy at current weight?
- Best alternative:
- Required next action if under review:

### Section 13 — Final Action Table

The final action table must include or clearly derive:

- Fresh Cash Test
- Best Alternative
- Required Next Review Action

Preferred table:

| Ticker | ETF | Existing/New | Weight Inherited | Target Weight | Suggested Action | Conviction Tier | Total Score | Fresh Cash Test | Best Alternative | Required Next Review Action | Portfolio Role | Better Alternative Exists? | Short Reason |
|---|---|---|---:|---:|---|---|---:|---|---|---|---|---|---|

---

## Operational discipline rule

A run is not recommendation-discipline complete unless:

- every `Hold but replaceable` has a named next action
- every weak hedge has a hedge-validity decision
- every >10% loser has a re-underwriting note
- every cash balance >3% has a reserve/deploy explanation
- every major factor concentration has an explicit portfolio-level note

The delivery workflow should run:

```bash
python validate_recommendation_discipline.py --strict-report-contract
```

before send once this addendum is active.
