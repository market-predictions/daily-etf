# ETF Review OS — Next Actions

## Status legend
- `[USER]` = must be done manually by you in UI or external systems
- `[ASSISTANT]` = I can do directly in chat/repo
- `[JOINT]` = I prepare, you apply/approve

---

## Phase 1 — keep the working environment disciplined

### 1. Keep using the lean bootstrap upload model
- Owner: `[USER]`
- Primary upload:
  - `control/PROJECT_BOOTSTRAP.md`
- Action:
  - keep the project context lean
  - continue reading changing repo files live from GitHub
- Done when:
  - future sessions do not depend on stale uploaded repo files

### 2. Keep using the control-layer start sequence
- Owner: `[JOINT]`
- Action: every meaningful ETF architecture, debugging, prompt, state, workflow, or delivery session starts with:
  1. `control/SYSTEM_INDEX.md`
  2. `control/CURRENT_STATE.md`
  3. `control/NEXT_ACTIONS.md`
  4. only then the minimum relevant execution file(s)
- Done when: sessions no longer need to rediscover how the system is organized.

---

## Phase 2 — recommendation discipline rollout

### 3. Merge and validate PR #13
- Owner: `[JOINT]`
- Source PR:
  - `Add recommendation discipline layer`
- Action:
  - review PR #13
  - merge if acceptable
  - confirm no runtime validation regressions
- Done when:
  - PR #13 is merged to `main`

### 4. Run a fresh production report with strict recommendation discipline
- Owner: `[ASSISTANT]`
- Action:
  - create a new English canonical report and Dutch companion
  - include the required `Portfolio discipline check`
  - include Section 10 buy-today / current-weight / best-alternative / required-next-action fields
  - include Section 13 Fresh Cash Test / Best Alternative / Required Next Review Action columns
  - ensure matching lane artifact exists
  - allow the production workflow to run
- Done when:
  - `validate_recommendation_discipline.py --strict-report-contract` passes before send
  - email delivery has real manifest/receipt evidence

### 5. Confirm expanded recommendation scorecard persistence
- Owner: `[ASSISTANT]`
- Action:
  - confirm companion state workflow runs after successful production send
  - confirm `output/etf_recommendation_scorecard.csv` is committed with the expanded schema
  - confirm `RECOMMENDATION_DISCIPLINE_OK` appears in logs
- Done when:
  - state artifacts persist to `main` after delivery

---

## Phase 3 — preserve executive look & feel and bilingual delivery

### 6. Do not alter presentation/rendering unless explicitly requested
- Owner: `[ASSISTANT]`
- Source files:
  - `send_report.py`
  - `delivery_base.py`
  - `send_report_OLD.py`
  - `etf-pro.txt`
  - `etf-pro-nl.txt`
- Action:
  - preserve the existing HTML/PDF styling
  - preserve equity-curve embedding
  - preserve English canonical + Dutch companion flow
  - preserve bilingual numeric parity validation
- Done when: architecture changes can be made without visual or bilingual regressions.

### 7. Validate any production workflow change against bilingual delivery
- Owner: `[ASSISTANT]`
- Action:
  - do not remove or rename existing bilingual env vars
  - do not change `MRKT_RPRTS_SUBJECT_PREFIX_NL`
  - do not change `MRKT_RPRTS_MAIL_TO_NL`
  - keep EN/NL pair validation before render/send
- Done when: workflow improvements do not silently break Dutch companion delivery.

---

## Phase 4 — validate breadth and state enforcement in live ETF runs

### 8. Confirm compact publication discipline
- Owner: `[ASSISTANT]`
- Action:
  - confirm the Structural Opportunity Radar remains compact
  - confirm the report still publishes only the best-ranked 5-8 lanes
  - confirm omitted-lane proof does not bloat the report
  - confirm strong-but-not-yet-actionable ideas remain selective rather than padded
- Done when: broader discovery does not degrade executive selectivity.

### 9. Check lane continuity and omitted-lane behavior in real output
- Owner: `[ASSISTANT]`
- Action:
  - confirm retained lanes, new entrants, dropped lanes, and near-miss challengers are handled cleanly
  - confirm omitted but relevant lanes are surfaced naturally in premium language
  - confirm the report explains changes without exposing internal process machinery
- Done when: the report feels fresher and broader without feeling unstable.

### 10. Confirm state artifacts after production
- Owner: `[ASSISTANT]`
- Action:
  - confirm `output/etf_portfolio_state.json`
  - confirm `output/etf_trade_ledger.csv`
  - confirm `output/etf_valuation_history.csv`
  - confirm `output/etf_recommendation_scorecard.csv`
- Done when:
  - all state files exist and validate after a live production cycle

---

## Phase 5 — cleanup only after successful production proof

### 11. Keep `send_report_OLD.py` protected until one more successful production cycle
- Owner: `[ASSISTANT]`
- Action:
  - do not delete `send_report_OLD.py` yet
  - confirm one successful production cycle after `delivery_base` import transition and strict recommendation discipline gate
- Done when:
  - production delivery succeeds and no fallback import is needed

### 12. Then convert or delete `send_report_OLD.py`
- Owner: `[ASSISTANT]`
- Action:
  - convert to tiny compatibility shim or delete after verification
  - update `control/REPO_FILE_CLASSIFICATION.md`
  - update `control/CLEANUP_PROGRESS.md`
- Done when:
  - repo no longer has misleading active `OLD` filename

### 13. Prune generated delivery derivatives
- Owner: `[ASSISTANT]`
- Action:
  - prune only after classification review
  - candidate patterns:
    - `output/*_clean.md`
    - `output/*_delivery.html`
    - `output/*.pdf`
    - `output/*_equity_curve.png`
    - old `output/pricing/price_cache_*.json`
- Done when:
  - canonical reports, lane artifacts, pricing audits, and state artifacts remain intact

---

## Phase 6 — reduce monolith risk later without weakening production

### 14. Fold recommendation addendum safely into `etf.txt`
- Owner: `[ASSISTANT]`
- Action:
  - only do this when a safe full-file patch path is available
  - avoid partial overwrite of the large production masterprompt
  - keep `control/ETF_MASTERPROMPT_RECOMMENDATION_DISCIPLINE_ADDENDUM.md` active until then
- Done when:
  - `etf.txt` contains the full discipline section and addendum can be retired

### 15. Keep the four-layer model explicit in future changes
- Owner: `[ASSISTANT]`
- Action: preserve the distinction between:
  1. decision framework
  2. input/state contract
  3. output contract
  4. operational runbook
- Done when: future changes do not collapse everything back into a single opaque blob.

---

## Suggested immediate next move

1. merge PR #13 after review
2. generate a fresh bilingual production report that includes the new discipline fields
3. let production workflow run
4. confirm strict recommendation discipline passes before send
5. confirm state artifacts persist back to `main`

---

## Current checkpoint

**The recommendation discipline layer is now implemented on PR #13. The next required step is merge + one fresh production run that proves strict recommendation discipline, bilingual delivery, and expanded state persistence all work together.**
