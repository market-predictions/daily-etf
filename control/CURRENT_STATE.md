# ETF Review OS — Current State

## Snapshot date
2026-04-21

## What this repository currently is

This repository is now a production-style weekly ETF review system with:
- a production masterprompt in `etf.txt`
- a premium editorial layer in `etf-pro.txt`
- a Dutch premium companion delivery layer in `etf-pro-nl.txt`
- a delivery/rendering script in `send_report.py`
- a production GitHub Actions workflow for execution and bilingual email delivery
- a companion GitHub Actions workflow for ETF state artifact persistence:
  - `.github/workflows/persist-etf-state-artifacts.yml`
- a non-email validation workflow for runtime and pricing changes
- archived outputs in `output/`
- a control layer in `control/`
- an as-is split scaffold in `prompts/as_is_split/`
- a split-test workflow in `.github/workflows/send-weekly-report-split-test.yml`
- a split-test output folder in `output_split_test/`
- a starter pricing subsystem in `pricing/` on `main` for quota-aware ETF close retrieval and audit output
- a lane-assessment artifact folder in `output/lane_reviews/`
- helper validation scripts:
  - `validate_lane_breadth.py`
  - `validate_etf_state_artifacts.py`
- an explicit ETF state artifact builder:
  - `pricing/build_state_artifacts.py`

## What changed in this step

The ETF architecture has started moving toward the more mature Weekly Index pattern without changing the existing report look & feel or bilingual delivery path.

Added:
- `pricing/build_state_artifacts.py`
- `validate_etf_state_artifacts.py`
- `.github/workflows/persist-etf-state-artifacts.yml`

The state artifact builder creates the explicit implementation-state files that were previously only planned:
- `output/etf_portfolio_state.json`
- `output/etf_trade_ledger.csv`
- `output/etf_valuation_history.csv`
- `output/etf_recommendation_scorecard.csv`

The validator checks that:
- the ETF state artifact exists
- state positions reconcile to total NAV
- invested value plus cash reconciles to total NAV
- valuation history reconciles to state NAV
- scorecard / state artifacts are at least structurally consistent

The companion workflow runs after the production send workflow completes successfully or by manual dispatch. It builds the ETF state artifacts, validates them, and commits them back to `main`.

This was deliberately implemented as a non-destructive artifact layer. It does not alter:
- `send_report.py` rendering behavior
- HTML/PDF styling
- equity-curve rendering
- Dutch companion generation
- bilingual parity validation
- email send logic
- `.github/workflows/send-weekly-report.yml` render/send steps

## Current strengths

- Strong executive look & feel in the ETF report family.
- Clear client-grade delivery standard.
- Production report, pro-editing layer, Dutch companion layer, and delivery script already exist.
- GitHub remains the live source of truth.
- The control layer exists and reflects the production architecture direction.
- The production prompt has a broader thematic discovery model with compact publication filtering.
- The production prompt requires a mandatory breadth universe and matching lane artifact.
- The premium editorial layer protects calm, selective subscriber-facing tone.
- The premium editorial layer preserves compact omitted-lane visibility instead of hiding it.
- A quota-aware pricing subsystem exists and can produce pricing audits.
- Validation and sending are separated more cleanly at the workflow layer.
- Bilingual delivery is protected by explicit English/Dutch pair validation and numeric parity checks in `send_report.py`.
- ETF now has an explicit implementation-state artifact builder and validator.
- ETF now has a companion state-artifact persistence workflow that avoids touching the secret-bearing bilingual send workflow.

## Current weaknesses

### 1. Production prompt monolith still exists
The production system still relies on `etf.txt` as a large combined prompt mixing:
- strategy logic
- state/input rules
- valuation protocol
- output rules
- delivery expectations
- workflow orchestration
- completion logic

### 2. State artifacts are wired as a companion workflow, not yet as an inline pre-render gate
The files now exist:
- `pricing/build_state_artifacts.py`
- `validate_etf_state_artifacts.py`
- `.github/workflows/persist-etf-state-artifacts.yml`

Current behavior:
- state artifacts are built after the production send workflow succeeds, through a companion `workflow_run` workflow
- the existing production send workflow remains untouched to protect bilingual delivery and secret-bearing env configuration

Still pending:
- decide whether to later move the state builder inline into `.github/workflows/send-weekly-report.yml`
- if moved inline, place it after `pricing.run_pricing_pass` and before render/send
- keep bilingual render/send behavior unchanged

### 3. Breadth enforcement is not yet fully wired into every state artifact
The breadth logic is now live in:
- `etf.txt`
- `etf-pro.txt`
- `validate_lane_breadth.py`
- `output/lane_reviews/`

The workflow already contains a lane breadth validation step, but continued live-run validation is still required to confirm that each production report has a matching lane artifact and omitted-lane proof.

### 4. Explicit ETF state files still need live-run confirmation
The builder and companion workflow now exist.
Still required:
- run a fresh production report
- confirm the companion workflow executes after successful send workflow completion
- confirm generated state artifacts are committed back to `main`

### 5. The pricing subsystem is still evolving
Still pending:
- hardening issuer-page handlers through runtime validation
- evaluating whether Yahoo fallback remains necessary after API coverage testing
- fuller prompt/report consumption of audit-derived state beyond pricing only
- deterministic state/report conflict resolution

### 6. Live production monitoring is still needed
The updated architecture should now be validated through normal live production runs to confirm:
- no radar bloat
- no drift in executive tone
- no rendering regressions
- bilingual parity remains intact
- better surfacing of omitted categories
- stable pricing-pass behavior under free-tier rate limits
- clean use of matching pricing audits without stale carry-over
- correct one-to-one report and lane-artifact pairing
- state artifacts reconcile when generated
- the companion state-artifact workflow runs successfully after delivery

## Target architecture

### ChatGPT side
- One dedicated ChatGPT Project called **ETF Review OS**.
- Project instructions that reinforce the operating model.
- A lean bootstrap model using `control/PROJECT_BOOTSTRAP.md` as the default standing upload.
- Live GitHub reads for changing repo files.

### GitHub side
- GitHub remains the source of truth for prompts, scripts, workflows, outputs, and control docs.
- The production prompt uses open discovery + dynamic lane ranking + compact publication.
- The production prompt requires a mandatory breadth universe and a matching lane artifact per report.
- The split scaffold remains available as reference and optional architecture workbench, not as a required gate for this change.
- ETF is moving toward an explicit pricing/state layer in `pricing/` plus machine-readable audit output in `output/pricing/`.
- ETF is also moving toward a machine-readable lane-assessment layer in `output/lane_reviews/`.
- ETF now has an explicit state artifact layer with a companion persistence workflow.

### Delivery side
- Delivery remains in `send_report.py` plus GitHub Actions.
- `etf-pro.txt` remains the premium English editorial compression layer.
- `etf-pro-nl.txt` remains the Dutch companion layer derived from the completed English report.
- The ETF executive look & feel remains the non-negotiable presentation reference for the report family.
- Production email send is gated to actual production report output pushes.
- Runtime and pricing code changes are validated separately without sending email.
- State artifact persistence is handled by companion workflow to avoid disturbing the delivery workflow.

## Immediate priorities

### Priority A — validate companion state artifact persistence in production
Required:
- run a fresh bilingual ETF production report
- confirm `.github/workflows/send-weekly-report.yml` succeeds
- confirm `.github/workflows/persist-etf-state-artifacts.yml` starts after the successful send workflow
- confirm state artifacts are committed back to `main`

### Priority B — validate live breadth behavior in production
Still required:
- confirm major omitted domains now appear as promoted lanes or compact challengers
- confirm the published radar remains compact and decision-useful
- confirm omitted-lane language reads naturally in the premium layer

### Priority C — finish send-path enforcement later if needed
Still optional:
- move state artifact build/validation inline into the production send workflow once safe
- keep `validate_lane_breadth.py` active before render/send
- ensure missing lane artifacts fail before subscriber delivery
- ensure lane artifacts and reports are paired by exact date/version

### Priority D — reduce monolith risk later without weakening production
Still required:
- keep the four-layer architecture explicit in future changes
- gradually move boundary logic out of the monolith where safe
- preserve production reliability, bilingual output, and executive presentation quality while doing so

## Recommended session start sequence

For any future ETF architecture session:
1. read `control/SYSTEM_INDEX.md`
2. read this file
3. read `control/NEXT_ACTIONS.md`
4. only then open the specific execution file relevant to the task

## Current role split

### Manual by user
- maintain the ChatGPT Project bootstrap model
- add and manage repository secrets in GitHub UI
- review live report quality as subscriber/end-user
- review and merge implementation PRs when appropriate

### Can be done by assistant
- refine the production prompt
- refine the premium editorial layer
- update GitHub control files
- review and improve scripts/workflows
- strengthen pricing/state authority rules
- harden continuity logic and executive presentation behavior
- extend the pricing subsystem
- extend lane breadth enforcement and validation
- extend explicit ETF state artifacts and validation

## Current status label

**The ETF production prompt and premium editorial layer require mandatory breadth assessment and compact omitted-lane proof; the delivery script protects executive look & feel and bilingual EN/NL parity; an explicit ETF state artifact builder, validator, and companion persistence workflow now exist; the next validation step is a fresh bilingual ETF production run followed by confirmation that state artifacts persist back to `main`.**
