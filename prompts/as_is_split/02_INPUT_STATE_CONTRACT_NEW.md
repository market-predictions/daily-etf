# ETF Input / State Contract — As-Is Split — NEW

This file extracts the **input-resolution, carry-forward, pricing-pass, portfolio-tracking, and pricing-operability** parts of `etf.txt` without intentionally changing the investment methodology.
Cross-references to other sections are preserved as written.

---

## 6. INPUT RESOLUTION + STANDARDIZED INPUT TEMPLATE

If the user does not explicitly provide a new portfolio in the current chat, you must automatically use the most recent stored report in:
- repository: `market-predictions/daily-etf`
- folder: `output/`

### Most recent report rule
Use the most recent available report, including same-day versioned reports, using this priority:
1. latest date
2. highest same-day version number

Recognize both naming patterns:
- `weekly_analysis_YYMMDD.md`
- `weekly_analysis_YYMMDD_NN.md`

### No-manual-input fallback rule
If a prior report exists, do not ask for manual portfolio input.

Use this fallback hierarchy:
1. explicit portfolio data in the current chat
2. Section `## 16. Carry-forward input for next run` from the most recent stored report
3. Section `## 15. Current portfolio holdings and cash`
4. Section `## 13. Final action table`
5. deterministic assumptions

### Critical pricing precedence rule
A prior report is a source for:
- share counts
- thesis context
- prior weights
- prior actions
- carry-forward structure

A prior report is **not** the preferred source for current prices if fresh same-day close retrieval is feasible.

### Inaugural build rule
If no prior report exists and I do not provide a portfolio, build a fresh inaugural model portfolio using:
- Starting capital: EUR 100,000
- no leverage unless explicitly allowed
- a reasonably diversified ETF implementation aligned with the framework

### Portfolio tracking rules
The tracked portfolio must follow these rules:
- Base capital: EUR 100,000
- Holdings are tracked in native ticker currency
- Total portfolio NAV is tracked in EUR
- Use the same-day market close EUR/USD snapshot where available
- If a same-day close snapshot is not cleanly verifiable, use the latest official reference EUR/USD rate from the Market Data + FX Valuation Protocol
- Assume whole shares only
- Residual unallocated capital remains as cash
- Assume all recommendations are implemented
- Do not let prior-report pricing become the default when fresh close retrieval is still possible

---

## 6A. MARKET DATA + FX VALUATION PROTOCOL

The purpose of this section is to make ETF closing-price retrieval and EUR valuation operationally deterministic **without creating lagging portfolio pricing**.

### Primary rule
After the U.S. regular session has ended, the default behavior is to attempt a fresh same-day valuation update.
Carry-forward is a fallback, not the baseline.

### Allowed pricing source hierarchy for ETF closes
For each ETF holding, use this source priority:
1. official exchange or primary market close
2. issuer or fund provider page if it clearly shows the latest market price or NAV-relevant trading price
3. major market data source with latest official close
4. reputable financial media market quote page
5. prior verified close from the latest stored report only if no fresh close can be verified

### Allowed FX source hierarchy for USD-to-EUR conversion
Use this priority for USD-to-EUR conversion:
1. same-day market close EUR/USD snapshot from a reputable FX, central-bank, or market-data source
2. latest official ECB or equivalent reference rate if same-day close is not yet reliably available
3. prior verified EUR/USD from the latest stored report only if no fresh FX reference can be verified

### Time-of-day rule
A same-day ETF close may be used once the U.S. regular session has ended.
Use regular-session close, not after-hours.
Do not wait for a single perfect source if regular-session close data is already available per ticker from reputable sources.

### Per-ticker valuation rule
You must attempt to retrieve a fresh close for every held ETF separately.
Do not require that all holdings come from one single source.
Per-ticker verified closes are allowed.

### Mandatory coverage table rule
For every run after the U.S. regular close, you must build an internal pricing coverage table before writing the report.

This table must contain, at minimum:
- Ticker
- Previous price
- Fresh price found? Yes/No
- Source tier used
- FX basis used
- Status = Fresh close / Fresh fallback source / Carried forward

### Incomplete-set rule
If at least 75% of holdings by count OR at least 85% of invested portfolio weight has a fresh verifiable close:
- update those holdings to the fresh close
- carry forward only the holdings that could not be freshly verified
- still update total NAV and equity curve

If less than that threshold is met:
- carry forward the full prior verified portfolio valuation
- explicitly say that the mark-to-market was not updated because the fresh close-set was too incomplete

### Currency-conversion rule
If all ETF closes are fresh but same-day EUR/USD is not cleanly available:
- use the latest official reference EUR/USD rate from the allowed FX hierarchy
- do not block ETF valuation solely because one exact market-close FX print is unavailable

### Staleness labeling rule
For every run, classify each holding price as one of:
- Fresh close
- Fresh source, non-primary fallback
- Carried forward

### Deterministic valuation rule
The valuation process must prefer a partial but explicitly labeled fresh mark-to-market over a full carry-forward, as long as the Incomplete-set rule is satisfied.

### Mandatory reporting note
If any holdings were carried forward because fresh closes were unavailable, state this briefly in:
- Executive Summary
- Equity Curve and Portfolio Development
- Position Changes Executed This Run or Current Portfolio Holdings and Cash

### Anti-freeze rule
Do not leave the equity curve unchanged merely because one or two holdings or the exact same-day FX close could not be perfectly verified.

### Anti-lag rule
After the U.S. regular close, the system must actively prefer a fresh same-day valuation update.
Carry-forward may happen only after the pricing pass has actually been attempted and evaluated.

---

## 6B. MANDATORY PRE-ANALYSIS PRICING PASS

Before any macro analysis, portfolio scoring, GitHub write, or email delivery, you must complete a fresh market-data valuation pass.

### Required sequence
1. Retrieve a fresh close for each held ETF individually.
2. Retrieve the USD/EUR conversion basis using the FX hierarchy.
3. Build the internal pricing coverage table for all holdings.
4. Label each holding as:
   - Fresh close
   - Fresh fallback source
   - Carried forward
5. Compute:
   - holdings coverage by count
   - invested-weight coverage
6. Apply the Incomplete-set rule immediately.
7. Recalculate:
   - total NAV
   - market values
   - weights
   - cash %
   - since-inception return
8. Only after this repricing step is complete may the report-writing step begin.

### Hard precedence rule
The pricing pass comes before:
- macro regime classification
- geopolitical regime classification
- position scoring
- new opportunity generation
- GitHub write
- email delivery

### Fail-soft rule
If at least 75% of holdings by count OR 85% of invested weight can be freshly valued, update the portfolio immediately using the fresh prices available and carry forward only unresolved holdings.

### Portfolio-wide carry-forward prohibition
Do not carry forward the whole portfolio merely because one or two holdings are unresolved if the Incomplete-set rule is otherwise satisfied.

### Freshness-first rule
For after-close runs, the portfolio must be treated as a live tracked book.

---

## 6C. MANDATORY VALUATION SANITY CHECKS

Before the report is written, the pricing pass output must pass the following arithmetic checks.

### Holdings-table arithmetic
The section later published as `Current portfolio holdings and cash` must satisfy all of these:
1. the sum of all non-cash `Market value (EUR)` rows must equal `Invested market value (EUR)`
2. the `CASH` row `Market value (EUR)` must equal `Cash (EUR)`
3. the sum of all `Market value (EUR)` rows including `CASH` must equal `Total portfolio value (EUR)`
4. `Since inception return (%)` must be derived from `Total portfolio value (EUR)` versus the original starting capital

### Equity-curve alignment
The section later published as `Equity curve and portfolio development` must satisfy all of these:
1. the latest row in the equity-curve table must equal `Total portfolio value (EUR)`
2. the chart rendered from that section must be based on the same table values, not a conflicting hidden source
3. if the portfolio value is carried forward, that status must be explicit in the equity-curve notes and latest table row comment

### Fail-loud rule
If any sanity check fails:
- do not publish the report in chat
- do not write the report to GitHub
- do not trigger email delivery
- instead report the valuation inconsistency explicitly

### Anti-placeholder rule
Do not silently reuse `100,000.00` or any other prior total solely because it was the last clean value.
A carried-forward valuation is allowed only if it is explicitly justified by the pricing-pass coverage result.

### Anti-hidden-drift rule
If the equity-curve chart would differ from the latest equity-curve table values, the run must fail rather than render inconsistent portfolio history.

---

## 6D. ETF INSTRUMENT REGISTRY

The pricing system must be able to handle portfolio changes and new tickers triggered by macro, geopolitical, or policy analysis.

### Canonical registry file
Use:
- `control/ETF_INSTRUMENT_REGISTRY.csv`

If a `_NEW` registry exists during transition work, treat it as a design draft until the live registry is renamed into place.

### Registry purpose
The registry stores operational pricing metadata per ETF instrument.
It is not the investment-decision engine. It is the pricing-operability layer.

### Minimum registry fields
- ticker
- fund_name
- issuer
- currency
- source_rule_class
- onboarding_state
- preferred_primary_source
- preferred_secondary_source
- active_flag
- notes

### Registry rule
Do not hardcode the entire pricing system around the current portfolio only.
Use the registry so new tickers can be onboarded without redesigning the whole pricing workflow.

---

## 6E. INSTRUMENT ONBOARDING + SOURCE RULE CLASSES

### Onboarding states
Every ETF must be in one of these operational states:
- `candidate`
- `provisional`
- `active_tracked`
- `rejected_operationally`

### Source rule classes
Every ETF must also have a `source_rule_class` such as:
- `issuer_first`
- `issuer_or_marketdata`
- `quorum_required`
- `manual_review`

### Operational consequence
A new ETF may be analytically valid before it is pricing-operationally ready.

Therefore:
- a `candidate` may appear in Structural Opportunity Radar or Best New Opportunities
- but it must not enter live tracked holdings until it passes pricing-operability checks strongly enough to become `provisional` or `active_tracked`

### New ticker onboarding sequence
When a new ETF appears because analysis suggests a portfolio change:
1. identify the instrument, issuer, and currency
2. assign a provisional source rule class
3. attempt source discovery using free public sources
4. determine onboarding state
5. append evidence to the pricing evidence log
6. only then allow the ETF into live tracked implementation if status is sufficient

---

## 6F. PRICING EVIDENCE LOG

### Canonical evidence log file
Use:
- `output/pricing_evidence_log.csv`

If a `_NEW` evidence log exists during transition work, treat it as a design draft until the live file is renamed into place.

### Logging rule
Every run should append one row per evaluated ticker, including carried-forward and rejected instruments.

### Minimum fields
- run_date
- target_price_date
- ticker
- issuer
- onboarding_state
- source_rule_class
- source_1_name
- source_1_url_or_label
- source_1_asof
- source_1_price
- source_2_name
- source_2_url_or_label
- source_2_asof
- source_2_price
- chosen_price
- chosen_fx_basis
- chosen_status
- acceptance_reason
- manual_review_flag
- notes

### Acceptance statuses
At minimum use:
- `accepted`
- `accepted_fallback`
- `carried_forward`
- `manual_review_required`

### Tolerance rule
As a default starting policy:
- issuer + confirmation source may be accepted within 0.50%
- fallback + fallback may be accepted within 0.25%
- larger gaps should trigger `manual_review_required` or ticker-level carry-forward

### Anti-freeze rule extension
If one new or weakly covered ticker fails validation, do not freeze the whole portfolio if the rest of the holdings pass the incomplete-set rule.
Use per-ticker fallback and log the decision.

---

## STEP 11 — IMPLEMENT THE MODEL PORTFOLIO

Translate the final actions into an implemented model portfolio using these rules:
- Starting capital: EUR 100,000 for inaugural build
- Carry forward the prior implemented model portfolio if one exists
- Assume all current recommendations are implemented
- Use whole shares only
- Track holdings in native currency
- Convert total portfolio value to EUR using the market close EUR/USD snapshot
- Keep residual as cash
- Apply the Market Data + FX Valuation Protocol for all ETF closes and FX conversion
- Treat Section 6B as authoritative for valuation before narrative analysis begins
- Treat Section 6C as mandatory before the report may be finalized
- Use Sections 6D–6F when portfolio changes introduce new tickers or when pricing trust needs explicit evidence
- Do not require a single-source all-holdings close set if per-ticker verified closes are available
- If the Incomplete-set rule is satisfied, update the portfolio using fresh closes where available and carry forward only the unresolved holdings
- Do not inherit prior report prices as current prices if the pricing pass has produced a fresh valuation decision

## STEP 12 — BUILD THE EQUITY-CURVE SUMMARY

Use the portfolio history from the stored reports to summarize:
- starting capital
- current portfolio value
- since-inception return
- whether the portfolio is at a new equity high, pullback, or drawdown

The report must include:
- a short textual equity-curve summary
- a compact equity-curve data table
- the literal marker line: `EQUITY_CURVE_CHART_PLACEHOLDER`

The latest equity-curve table row must match the current report’s `Total portfolio value (EUR)` exactly, subject only to trivial rounding tolerance.
