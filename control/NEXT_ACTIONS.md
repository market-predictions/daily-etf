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

## Phase 2 — preserve executive look & feel and bilingual delivery

### 3. Do not alter presentation/rendering unless explicitly requested
- Owner: `[ASSISTANT]`
- Source files:
  - `send_report.py`
  - `send_report_OLD.py`
  - `etf-pro.txt`
  - `etf-pro-nl.txt`
- Action:
  - preserve the existing HTML/PDF styling
  - preserve equity-curve embedding
  - preserve English canonical + Dutch companion flow
  - preserve bilingual numeric parity validation
- Done when: architecture changes can be made without visual or bilingual regressions.

### 4. Validate any production workflow change against bilingual delivery
- Owner: `[ASSISTANT]`
- Action:
  - do not remove or rename existing bilingual env vars
  - do not change `MRKT_RPRTS_SUBJECT_PREFIX_NL`
  - do not change `MRKT_RPRTS_MAIL_TO_NL`
  - keep EN/NL pair validation before render/send
- Done when: workflow improvements do not silently break Dutch companion delivery.

---

## Phase 3 — validate the breadth-enforcement architecture in live ETF runs

### 5. Run the next live ETF review from the updated production prompt
- Owner: `[ASSISTANT]`
- Source files:
  - `etf.txt`
  - `etf-pro.txt`
  - `etf-pro-nl.txt`
- Action:
  - use the updated production files directly
  - confirm the report still feels compact, premium, and decision-useful
  - confirm omitted sectors now show up as promoted lanes or compact challengers
  - confirm a matching pricing audit is consumed correctly when available
  - confirm a matching lane artifact is written correctly
- Done when: a live production run shows the broader discovery model, omitted-lane visibility, and matching lane artifact working inside the existing executive format.

### 6. Confirm compact publication discipline
- Owner: `[ASSISTANT]`
- Action:
  - confirm the Structural Opportunity Radar remains compact
  - confirm the report still publishes only the best-ranked 5-8 lanes
  - confirm omitted-lane proof does not bloat the report
  - confirm “strong but not yet actionable” ideas remain selective rather than padded
- Done when: broader discovery does not degrade executive selectivity.

### 7. Check lane continuity and omitted-lane behavior in real output
- Owner: `[ASSISTANT]`
- Action:
  - confirm retained lanes, new entrants, dropped lanes, and near-miss challengers are handled cleanly
  - confirm omitted but relevant lanes are surfaced naturally in premium language
  - confirm the report explains changes without exposing internal process machinery
- Done when: the report feels fresher and broader without feeling unstable.

---

## Phase 4 — wire explicit ETF state artifacts into production

### 8. Build state artifacts after the pricing pass
- Owner: `[ASSISTANT]`
- New file:
  - `pricing/build_state_artifacts.py`
- Action:
  - add `python -m pricing.build_state_artifacts` after `python -m pricing.run_pricing_pass` in `.github/workflows/send-weekly-report.yml`
- Done when: every production run writes or refreshes:
  - `output/etf_portfolio_state.json`
  - `output/etf_trade_ledger.csv`
  - `output/etf_valuation_history.csv`
  - `output/etf_recommendation_scorecard.csv`

### 9. Persist pricing and state artifacts back to main
- Owner: `[ASSISTANT]`
- Action:
  - extend the existing pricing audit commit step so it also commits:
    - `output/etf_portfolio_state.json`
    - `output/etf_trade_ledger.csv`
    - `output/etf_valuation_history.csv`
    - `output/etf_recommendation_scorecard.csv`
- Done when: state artifacts are available in GitHub after successful production runs.

### 10. Validate state artifacts before render/send
- Owner: `[ASSISTANT]`
- New file:
  - `validate_etf_state_artifacts.py`
- Action:
  - add `python validate_etf_state_artifacts.py` before render validation
  - fail before send if state/NAV arithmetic does not reconcile
- Done when: ETF has a hard state-artifact validation gate similar in spirit to Weekly Index.

### 11. Keep the workflow patch minimal and bilingual-safe
- Owner: `[ASSISTANT]`
- Action:
  - patch only the pricing/state portion of `.github/workflows/send-weekly-report.yml`
  - do not alter render/send steps
  - do not alter bilingual pair validation
  - do not alter SMTP secret env vars
- Done when: state artifact production is wired in without damaging delivery.

---

## Phase 5 — finish breadth enforcement into the send path

### 12. Keep `validate_lane_breadth.py` active before render
- Owner: `[ASSISTANT]`
- Action:
  - preserve the distinct pre-render breadth validation step
  - make the workflow fail before render/send if breadth proof is missing
  - surface a clear `BREADTH_OK` or equivalent log line when successful
- Done when: breadth is enforced operationally before subscriber delivery.

### 13. Confirm report/lane artifact one-to-one pairing
- Owner: `[ASSISTANT]`
- Action:
  - confirm every pro report has a matching lane artifact by date/version
  - confirm mismatched artifacts fail before send
- Done when: lane breadth becomes auditable rather than impressionistic.

---

## Phase 6 — reduce monolith risk later without weakening production

### 14. Keep the four-layer model explicit in future changes
- Owner: `[ASSISTANT]`
- Action: preserve the distinction between:
  1. decision framework
  2. input/state contract
  3. output contract
  4. operational runbook
- Done when: future changes do not collapse everything back into a single opaque blob.

### 15. Reduce monolith risk only where it is safe
- Owner: `[JOINT]`
- Action:
  - tighten boundaries gradually
  - keep production reliability intact
  - preserve the ETF executive look & feel while doing so
- Done when: clarity improves without destabilizing the live workflow.

---

## Suggested immediate next move

The best next move after this update is:
1. patch `.github/workflows/send-weekly-report.yml` with the minimal state-artifact hook
2. run a fresh bilingual ETF production report
3. confirm pricing audit, lane artifact, and state artifacts all persist to GitHub
4. confirm HTML/PDF output and Dutch companion delivery remain unchanged
5. only after that, consider adding a research-only inverse ETF / short-opportunity layer

---

## Current checkpoint

**The ETF repo now has an explicit state artifact builder and validator. The next required step is to wire them into the production workflow after the pricing pass and before render/send, while preserving the existing executive look & feel and bilingual EN/NL delivery flow.**
