# ETF Review OS — Current State

## Snapshot date
2026-04-21

## What this repository currently is

This repository is now a production-style weekly ETF review system with:
- a production masterprompt in `etf.txt`
- a premium editorial layer in `etf-pro.txt`
- a delivery/rendering script in `send_report.py`
- a production GitHub Actions workflow for execution and email delivery
- a non-email validation workflow for runtime and pricing changes
- archived outputs in `output/`
- a control layer in `control/`
- an as-is split scaffold in `prompts/as_is_split/`
- a split-test workflow in `.github/workflows/send-weekly-report-split-test.yml`
- a split-test output folder in `output_split_test/`
- a starter pricing subsystem in `pricing/` on `main` for quota-aware ETF close retrieval and audit output
- a new lane-assessment artifact folder in `output/lane_reviews/`
- a new helper validator script in `validate_lane_breadth.py`

## What changed in this step

The production ETF prompt has now been updated again to turn breadth from a soft discovery preference into an explicit production requirement. The key changes are:
- a mandatory breadth assessment universe across major investable buckets
- a requirement to assess those buckets every run before final ranking
- a matching machine-readable lane artifact for each production report
- a requirement to surface compact proof of omitted-but-assessed lanes in the final report
- corrected pro production filename rules in `etf.txt`

The premium editorial layer has also been tightened so it no longer compresses away omitted but relevant challengers. It now explicitly preserves compact proof that important breadth buckets were assessed even when they were not promoted into the live radar.

The repository now also contains:
- `output/lane_reviews/.gitkeep`
- `output/lane_reviews/README.md`
- `validate_lane_breadth.py`

This means the breadth fix is now partially implemented as both:
- production prompt/output-contract logic
- explicit artifact scaffolding and helper validation code

## Current strengths

- Strong executive look & feel in the ETF report family.
- Clear client-grade delivery standard.
- Production report, pro-editing layer, and delivery script already exist.
- GitHub remains the live source of truth.
- The control layer exists and now reflects the direct-production architecture choice.
- The production prompt now has a broader thematic discovery model with a compact publication filter.
- The production prompt now also requires a mandatory breadth universe and matching lane artifact.
- The premium editorial layer still protects a calm, selective, subscriber-facing tone.
- The premium editorial layer now preserves compact omitted-lane visibility instead of hiding it.
- A quota-aware pricing subsystem starter now exists on `main` and can evolve into the explicit state/input layer.
- Validation and sending are now separated more cleanly at the workflow layer.
- The prompt can now consume a matching pricing audit as an operational input layer when available.

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

### 2. Breadth enforcement is not yet fully wired into the production send path
The breadth logic is now live in:
- `etf.txt`
- `etf-pro.txt`
- `validate_lane_breadth.py`
- `output/lane_reviews/`

But the final delivery enforcement still needs to be wired directly into:
- `send_report.py`
- `.github/workflows/send-weekly-report.yml`

That means the architecture is now substantially improved, but the final render/send gate is not yet fully hardened at the production script level.

### 3. Explicit ETF state files still do not yet exist in production
ETF still relies mainly on prior report parsing plus the pricing subsystem and pricing-audit logic.
Planned future state files remain:
- `output/etf_portfolio_state.json`
- `output/etf_trade_ledger.csv`
- `output/etf_valuation_history.csv`
- `output/etf_recommendation_scorecard.csv`
- `output/pricing/price_audit_YYYYMMDD.json`

### 4. The pricing subsystem is still evolving
Still pending:
- hardening issuer-page handlers through runtime validation
- evaluating whether Yahoo fallback remains necessary after API coverage testing
- explicit valuation-state outputs
- fuller prompt/report consumption of audit-derived state beyond pricing only

### 5. Live production monitoring is still needed
The updated architecture should now be validated through normal live production runs to confirm:
- no radar bloat
- no drift in executive tone
- no rendering regressions
- better surfacing of previously omitted categories
- stable pricing-pass behavior under free-tier rate limits
- clean use of matching pricing audits without stale carry-over
- correct one-to-one report and lane-artifact pairing

## Target architecture

### ChatGPT side
- One dedicated ChatGPT Project called **ETF Review OS**.
- Project instructions that reinforce the operating model.
- A lean bootstrap model using `control/PROJECT_BOOTSTRAP.md` as the default standing upload.
- Live GitHub reads for changing repo files.

### GitHub side
- GitHub remains the source of truth for prompts, scripts, workflows, outputs, and control docs.
- The production prompt now uses open discovery + dynamic lane ranking + compact publication.
- The production prompt now also requires a mandatory breadth universe and a matching lane artifact per report.
- The split scaffold remains available as a reference and optional architecture workbench, not as a required gate for this change.
- ETF is moving toward an explicit pricing/state layer in `pricing/` plus machine-readable audit output in `output/pricing/`.
- ETF is also moving toward a machine-readable lane-assessment layer in `output/lane_reviews/`.

### Delivery side
- Delivery remains in `send_report.py` plus GitHub Actions.
- `etf-pro.txt` remains the premium editorial compression layer.
- The ETF executive look & feel remains the non-negotiable presentation reference for the report family.
- Production email send is now gated to actual production report output pushes.
- Runtime and pricing code changes are now validated separately without sending email.
- The final step still required is to wire lane breadth validation directly into the render/send path.

## Immediate priorities

### Priority A — validate live breadth behavior in production
Still required:
- confirm major omitted domains now appear as promoted lanes or compact challengers
- confirm the published radar remains compact and decision-useful
- confirm omitted-lane language reads naturally in the premium layer

### Priority B — finish send-path enforcement
Still required:
- wire `validate_lane_breadth.py` logic directly into `send_report.py`
- wire breadth validation into `.github/workflows/send-weekly-report.yml`
- fail before send if the report lacks the matching lane artifact or omitted-lane proof block

### Priority C — move ETF toward explicit implementation state
Still required:
- validate the pricing subsystem in real runs
- add explicit ETF state files
- make valuation authority less dependent on report parsing
- tighten deterministic conflict resolution between report intent and implementation facts

### Priority D — reduce monolith risk later without weakening production
Still required:
- keep the four-layer architecture explicit in future changes
- gradually move boundary logic out of the monolith where safe
- preserve production reliability and executive presentation quality while doing so

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

## Current status label

**The ETF production prompt and premium editorial layer now require a mandatory breadth assessment universe, a matching machine-readable lane artifact, and compact visibility for omitted-but-assessed lanes; scaffold files and a helper validator now exist in GitHub; and the next step is to wire that breadth validation directly into `send_report.py` and the production send workflow so the delivery path can fail before send when breadth proof is missing.**
