# ETF Input / State Contract — As-Is Split

This file extracts the **input-resolution, valuation, and carry-forward** parts of `etf.txt` without intentionally changing logic.
Cross-references to other sections are preserved as written.

---

# 6. INPUT RESOLUTION + STANDARDIZED INPUT TEMPLATE

I may provide the portfolio using the structure below.

If I do not explicitly provide a new portfolio in the current chat, you must automatically use the most recent stored report in:
- repository: `market-predictions/daily-etf`
- folder: `output/`

## Most recent report rule
Use the most recent available report, including same-day versioned reports, using this priority:
1. latest date
2. highest same-day version number

Recognize both naming patterns:
- `weekly_analysis_YYMMDD.md`
- `weekly_analysis_YYMMDD_NN.md`

## No-manual-input fallback rule
If a prior report exists, do not ask me for manual portfolio input.

Use this fallback hierarchy:
1. explicit portfolio data in the current chat
2. Section `## 16. Carry-forward input for next run` from the most recent stored report
3. Section `## 15. Current portfolio holdings and cash`
4. Section `## 13. Final action table`
5. deterministic assumptions

## Critical pricing precedence rule
A prior report is a source for:
- share counts
- thesis context
- prior weights
- prior actions
- carry-forward structure

A prior report is **not** the preferred source for current prices if fresh same-day close retrieval is feasible.
After the U.S. regular close, fresh same-day ETF pricing must be attempted before current prices are inherited from a prior report.

## Inaugural build rule
If no prior report exists and I do not provide a portfolio, build a fresh inaugural model portfolio using:
- Starting capital: EUR 100,000
- no leverage unless explicitly allowed
- a reasonably diversified ETF implementation aligned with the framework

## Portfolio tracking rules
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

## Standardized input template

### Portfolio table
| Ticker | ETF Name | Direction | Weight % | Avg Entry | Current Price | P/L % | Original Thesis | Role |
|---|---|---:|---:|---:|---:|---:|---|---|

### Available cash
- Cash %:
- Margin usage %:
- Leverage allowed: Yes/No

### Watchlist / structural radar
| Theme | Primary ETF | Alternative ETF | Why I’m considering it | Current status |
|---|---|---|---|---|

### Constraints
- Max position size:
- Max number of positions:
- UCITS only: Yes/No
- Leverage ETFs allowed: Yes/No
- Regions to avoid:
- Sectors to avoid:
- Drawdown tolerance:
- Income vs growth preference:

### Changes since last review
- Added:
- Reduced:
- Closed:
- Thesis changes:
- Risk concerns:

---

# 6A. MARKET DATA + FX VALUATION PROTOCOL

This section is mandatory.

The purpose of this section is to make ETF closing-price retrieval and EUR valuation operationally deterministic **without creating lagging portfolio pricing**.

## Primary rule
After the U.S. regular session has ended, the default behavior is to attempt a fresh same-day valuation update.
Carry-forward is a fallback, not the baseline.

Do not block the full valuation update only because a single unified source for all holdings is unavailable.
A complete end-of-day valuation may use per-ticker verified closes from multiple reputable sources, as long as the source used for each ticker is explicitly deterministic and the pricing timestamp is close-compatible.

## Allowed pricing source hierarchy for ETF closes
For each ETF holding, use this source priority:

1. official exchange or primary market close
2. issuer or fund provider page if it clearly shows the latest market price or NAV-relevant trading price
3. major market data source with latest official close
4. reputable financial media market quote page
5. prior verified close from the latest stored report only if no fresh close can be verified

## Allowed FX source hierarchy for USD-to-EUR conversion
Use this priority for USD-to-EUR conversion:

1. same-day market close EUR/USD snapshot from a reputable FX, central-bank, or market-data source
2. latest official ECB or equivalent reference rate if same-day close is not yet reliably available
3. prior verified EUR/USD from the latest stored report only if no fresh FX reference can be verified

## Time-of-day rule
A same-day ETF close may be used once the U.S. regular session has ended.
Use regular-session close, not after-hours.
Do not wait for a single perfect source if regular-session close data is already available per ticker from reputable sources.

## Per-ticker valuation rule
You must attempt to retrieve a fresh close for every held ETF separately.
Do not require that all holdings come from one single source.
Per-ticker verified closes are allowed.

## Mandatory coverage table rule
For every run after the U.S. regular close, you must build an internal pricing coverage table before writing the report.
This table must contain, at minimum:
- Ticker
- Previous price
- Fresh price found? Yes/No
- Source tier used
- FX basis used
- Status = Fresh close / Fresh fallback source / Carried forward

You do not have to print this full table in the client report unless explicitly asked, but you must use it to drive the valuation decision.

## Incomplete-set rule
If at least 75% of holdings by count OR at least 85% of invested portfolio weight has a fresh verifiable close:
- update those holdings to the fresh close
- carry forward only the holdings that could not be freshly verified
- clearly state which tickers were carried forward if the user asks or if the report notes require it
- still update total NAV and equity curve

If less than that threshold is met:
- carry forward the full prior verified portfolio valuation
- explicitly say that the mark-to-market was not updated because the fresh close-set was too incomplete

## Currency-conversion rule
If all ETF closes are fresh but same-day EUR/USD is not cleanly available:
- use the latest official reference EUR/USD rate from the allowed FX hierarchy
- do not block ETF valuation solely because one exact market-close FX print is unavailable

## Staleness labeling rule
For every run, classify each holding price as one of:
- Fresh close
- Fresh source, non-primary fallback
- Carried forward

This labeling is internal unless explicitly requested, but it must control the valuation logic.

## Deterministic valuation rule
The valuation process must prefer a partial but explicitly labeled fresh mark-to-market over a full carry-forward, as long as the Incomplete-set rule is satisfied.

## Mandatory reporting note
If any holdings were carried forward because fresh closes were unavailable, state this briefly in:
- Executive Summary (`What changed this week`)
- Equity Curve and Portfolio Development (`Notes`)
- Position Changes Executed This Run or Current Portfolio Holdings and Cash

## Anti-freeze rule
Do not leave the equity curve unchanged merely because one or two holdings or the exact same-day FX close could not be perfectly verified.
Use the fallback hierarchy and incomplete-set rule to keep the tracked portfolio moving whenever enough of the portfolio can be marked reliably.

## Anti-lag rule
After the U.S. regular close, the system must actively prefer a fresh same-day valuation update.
It is prohibited to skip the pricing pass just because:
- a prior report already exists
- one or two holdings are unresolved
- all holdings are not available from one source
- the reporting workflow is long
- the delivery step has not happened yet

Carry-forward may happen only after the pricing pass has actually been attempted and evaluated.

---

# 6B. MANDATORY PRE-ANALYSIS PRICING PASS

This section is mandatory.

Before any macro analysis, portfolio scoring, GitHub write, or email delivery, you must complete a fresh market-data valuation pass.

## Required sequence
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

## Hard precedence rule
The pricing pass comes before:
- macro regime classification
- geopolitical regime classification
- position scoring
- new opportunity generation
- GitHub write
- email delivery

## Fail-soft rule
If at least 75% of holdings by count OR 85% of invested weight can be freshly valued, update the portfolio immediately using the fresh prices available and carry forward only unresolved holdings.

## Portfolio-wide carry-forward prohibition
Do not carry forward the whole portfolio merely because one or two holdings are unresolved if the Incomplete-set rule is otherwise satisfied.

## Freshness-first rule
For after-close runs, the portfolio must be treated as a live tracked book.
That means current same-day close prices have precedence over prior report prices whenever fresh retrieval is feasible.

---

# 12. PRIOR REPORT LOOKUP RULE

Before starting the current analysis, look in `output/` within `market-predictions/daily-etf` for the most recent available report matching:
- `weekly_analysis_YYMMDD.md`
- `weekly_analysis_YYMMDD_NN.md`

Use the most recent available report, including same-day versioned reports, unless I explicitly provide new portfolio inputs in the current chat.

Priority order:
1. explicit portfolio data in the current chat
2. Section 16 from the most recent stored report
3. Section 15 from the most recent stored report
4. the most recent final action table
5. deterministic assumptions

## Delivery enforcement note
Neither a successful GitHub write nor a successful chat publication is sufficient on its own.
The mandatory workflow is only complete when the full report has been:
- published in chat
- written to GitHub
- and sent by email via `send_report.py` as the full HTML report body plus PDF attachment to `mrkt.rprts@gmail.com`

A summary-only email body is not sufficient.
A statement that the email was sent is not sufficient.
A positive delivery receipt from the send step is required.
