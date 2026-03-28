# ETF Output Contract — As-Is Split

This file extracts the **presentation, readability, and required-report-structure** parts of `etf.txt` without intentionally changing logic.
Cross-references to other sections are preserved as written.

---

# 2. CLIENT-GRADE PRESENTATION STANDARD

The report must be structured in two layers.

## Layer A - Client layer
This comes first and must be highly scannable:
1. Executive Summary
2. Portfolio Action Snapshot
3. Regime Dashboard
4. Structural Opportunity Radar
5. Key Risks
6. Bottom Line
7. Equity Curve and Portfolio Development

## Layer B - Analyst layer
This comes second and contains full detail:
8. Asset Allocation Map
9. Second-Order Effects Map
10. Current Position Review
11. Best New Opportunities
12. Portfolio Rotation Plan
13. Final Action Table
14. Position Changes Executed This Run
15. Current Portfolio Holdings and Cash
16. Carry-forward Input for Next Run
17. Disclaimer

## Rule
The client layer must be understandable on its own.
The analyst layer must support and justify the client layer.

Do not begin with dense scorecards or long diagnostics.
Always start with what changed, what to do, and why.

---

# 2A. VISUAL DELIVERY CONTRACT FOR HTML + PDF

The HTML body and PDF are rendered by a downstream delivery script. Your job is to write content that fits that premium visual system cleanly.

## Visual intent
The delivered report must feel like a premium weekly private-bank style briefing, not a generic word-processor export, dashboard toy, or PowerPoint-like mock-up.

The HTML email is the lead client-facing product.
The PDF must follow the same design language, but it must not force the email into a PDF-like reading experience.

## Core visual principles
The delivery system assumes:
- a light warm paper background
- a darker slate-teal header band
- a serif masthead for the product name only
- sans-serif body typography
- restrained champagne accent rules
- minimal icon use
- strong spacing discipline
- no decorative repetition
- clear separation between executive layer and analyst appendix
- compact, clean tables where tables improve scanning
- PDF layout that follows the email design language but uses print-safe pagination

## Non-negotiable presentation rules
Write in a way that supports a clean executive email:
- no repeated section naming inside the same section
- no duplicate header text that says the same thing twice
- no decorative internal labels such as "institutional", "client edition", "HTML/PDF", or implementation notes inside the report body
- the executive header subtitle must show only the fully written report date, not the report title repeated again
- the executive header may use a discreet right-aligned label "Investor Report" if it is visually balanced and subordinate to the masthead
- no unnecessary placeholder language such as "Suggested visual treatment"
- no visual clutter caused by too many colored pills, soft badges, or app-like UI elements
- no cheap or playful icon use inside the body
- no repeated decorative section headers where the body already makes the section purpose obvious
- no large analyst blocks that rely only on paragraph flow to separate one ticker or idea from the next
- no long unbroken walls of bullets when a compact table would communicate better
- no excessive subheading variation that creates visual noise without adding hierarchy

## Writing rules by the visual system
Write in a way that supports premium HTML/PDF rendering:
- Keep section openings short and decisive.
- Keep the Executive Summary compact and highly scannable.
- Keep action lists tight; do not flood the action snapshot with long bullets.
- Use short label-value lines where the structure asks for them.
- Keep tables compact, complete, and cleanly formatted.
- Preserve true line breaks in Markdown tables and lists; do not collapse them into escaped newline text.
- Avoid unnecessary filler sentences before the main conclusion.
- Do not write comments about formatting, design, rendering, or file generation into the report content.
- Prefer concise paragraphs over long narrative blocks.
- Keep repetitive wording to a minimum, especially across the executive sections.
- When the same point already appears in Executive Summary or Bottom Line, do not restate it again unless the later section adds new information.
- Keep ETF tickers as plain ticker text in headings, action lists, and tables; the delivery layer may automatically decorate those tickers as clickable TradingView links in HTML/PDF output.
- Preserve the first column label exactly as `Ticker` in ticker-based tables so the delivery layer can auto-link those cells reliably.
- In headings for single-position sections, keep the format `### TICKER — ETF name` so the delivery layer can auto-link the ticker consistently.

## Email-first execution addendum
The HTML email must read as a premium executive briefing first, and only secondarily as a full archival report.
That means the analyst appendix must remain complete in substance, but it must be rendered in a compact, controlled format.

The delivery layer should therefore prefer:
- compact summary cards at the top
- table-first rendering where possible
- clear visual separation between one ticker and the next
- one consistent heading hierarchy
- reduced decorative variation in the analyst appendix
- minimal vertical waste

Do not design the email as a long scrolling analyst memo with lightly styled markdown pasted into a card shell.

## Section-specific formatting expectations
The delivery system expects the following:
- Executive Summary: compact summary lines plus a single decisive main takeaway.
- Portfolio Action Snapshot: present the action states in a compact, executive-friendly structure that can be rendered as a clean table or matrix.
- Section badges / numbered headers must remain visually centered and aligned with their heading text in the final email render.
- Regime Dashboard: no repeated heading inside the section body.
- Structural Opportunity Radar: no repeated heading inside the section body.
- Current Position Review: each ticker block must begin with a clearly identifiable ticker / ETF heading and remain visually distinct from the next ticker.
- Best New Opportunities: each ranked opportunity must have a clean title line; avoid raw bracket-style labels such as `[Rank #1]` in the rendered output.
- Section kickers: the numeric badge, blue circle, and section title must be optically centered and aligned in the rendered email.
- Best New Opportunities subgroup lines such as `A. Macro-derived opportunities` and `B. Structural opportunities` must render as subdued subgroup labels, clearly subordinate to the specific opportunity titles beneath them.
- Prospective score: the underlying content must stay factor-by-factor, but it must be renderable as a compact 2-column factor/score table.
- Portfolio Rotation Plan: content must be cleanly renderable as a compact table or matrix instead of a long vertical icon stack.
- Carry-forward Input for Next Run: preserve the canonical sentence exactly in the markdown source, but do not display that sentence in the delivered client-facing HTML/PDF.
- The analyst appendix must restart the displayed section numbering from 1 and may use its own full header band with the fully written report date and a discreet right-aligned label "Analyst Report".
- In Best New Opportunities, subgroup lines such as `A. Macro-derived opportunities` and `B. Structural opportunities` must be visually subordinate to the actual opportunity titles and should align to the right in the delivery layer.
- Key Risks: render as a compact invalidator list; do not let it visually dissolve into generic bullets.
- Best New Opportunities: render each opportunity as a clearly separated opportunity block; the opportunity title must look materially different from the subsection label above it.
- Current Position Review: assessment content should be renderable as a compact label/value table or equivalent disciplined structure, not as a long undifferentiated bullet slab.
- Analyst appendix: preserve full substance, but render dense sections in a table-first, compressed style suitable for email reading.
- Section numbering badges are optional but, if used, they must align cleanly with the section label and must not create visual clutter.

## Icon rule
Icons are optional, not mandatory.
If icons are used at all, use them sparingly and only where they clearly improve scanability.
Do not rely on icons to create hierarchy.
Do not create a different icon treatment for every subsection.
The email should still look complete and premium if almost all body icons are removed.

## Delivery-script expectations
The downstream HTML renderer should, where possible:
- normalize subsection labels by removing decorative emojis from internal headings
- convert portfolio action snapshot into a compact two-column decision table
- convert portfolio rotation plan into a compact matrix / table
- convert prospective score into a two-column factor / score table
- visually separate each current holding review from the next using a distinct heading treatment or card boundary
- remove raw bracketed labels such as `[Rank #1]` from rendered opportunity titles
- keep PDF generation aligned with the email system, but allow a print-safe fallback layout when pagination requires it

## Attachment rule
The client attachment format is PDF, not DOCX.
The PDF and HTML body must contain the same substantive report.
The PDF follows the email style system; it does not lead it.

---

# 3. READABILITY + ICON REGIME

Use a clean, consistent icon regime to improve scanability. Use icons to improve readability, not to add clutter.

## Preferred icons
- ✅ supportive / aligned / passed / keep
- ⚠️ caution / mixed / weaker fit / partial concern
- ❌ invalidation / close / broken thesis / avoid
- ➕ add / increase / upgrade
- ➖ reduce / trim / lower weight
- 🔁 replace / rotate
- 🧭 regime / context / confluence / portfolio map
- 📊 scoring / model / ranking / comparison
- 🌍 geopolitics / cross-border driver
- 🏦 central bank / policy / rates
- 🛢️ energy / oil / supply shock
- 🥇 gold / hard-asset hedge
- 🏭 cyclicals / industrial / manufacturing exposure
- 💻 growth / tech / duration-sensitive exposure
- 🛡️ hedge / defense / resilience / protection
- 💵 USD / dollar / FX spillover
- 📅 event risk / catalyst / release calendar
- 🔍 second-order effect / transmission channel
- 🚀 structural innovation / secular opportunity
- 📈 portfolio development / equity curve
- 🚫 do not use / unsupported / not allowed

## Formatting rules
- Use bold for section headers, regime labels, verdicts, and the most decision-relevant phrases.
- Use short paragraphs and compact bullets.
- Use tables where by the framework.
- Put the most important client actions near the top.
- Keep the report visually consistent across runs.
- Do not bury the action call in long narrative text.
- Do not create redundant headings that repeat the section title.
- Prefer one strong hierarchy system over many slightly different visual heading styles.
- When a section is table-friendly, keep it table-friendly instead of turning it into long decorative bullet lists.

## Disclaimer display rules
Use a subtle Markdown-safe callout directly below the report title.

Use this exact structure immediately below the title:

> *This report is for informational and educational purposes only; please see the disclaimer at the end.*

This must look visibly separate from the body but must not dominate the page.

---

# 10. REQUIRED OUTPUT STRUCTURE

- In sections 10, 13, 14, 15, and 16, preserve `Ticker` as the first column header wherever tickers are shown.
- In section 10, preserve position headers in the format `### [Ticker] — [ETF name]`.
- In sections 4, 16, and any other ETF table, preserve the headers `Primary ETF` and `Alternative ETF` exactly where ETF tickers are shown.
- Where a table column contains ETF tickers intended for navigation, prefer plain ticker text only in those cells.

Use exactly this structure.

# Weekly Report Review YYYY-MM-DD

> *This report is for informational and educational purposes only; please see the disclaimer at the end.*

## 1. ✅ Executive summary
Must contain only:
- **Primary regime:** [label]
- **Secondary cross-current:** [label]
- **Geopolitical regime:** [label]
- **What changed this week:** [1 short paragraph]
- **Overall portfolio judgment:** [1 short paragraph]
- **Main takeaway:** **[short decisive sentence]**

## 2. 📌 Portfolio action snapshot
This section is mandatory.

### ➕ Add
- [tickers]

### ✅ Hold
- [tickers]

### ⚠️ Hold but replaceable
- [tickers]

### ➖ Reduce
- [tickers]

### ❌ Close
- [tickers]

### 🔁 Best replacements to fund
- Replace [old] with [new]

### Top 3 actions this week
1. ...
2. ...
3. ...

### Top 3 risks this week
1. ...
2. ...
3. ...

## 3. 🧭 Regime dashboard
### Macro regime
- Growth:
- Inflation:
- Central banks:
- Real rates:
- Credit:
- USD:
- Commodities:
- Equity leadership:
- Bond market signal:
- **Primary regime:** [label]
- Secondary cross-current:

### Geopolitical regime
- **Regime classification:** [label]
- Driver 1:
- Driver 2:
- Driver 3:
- Overall portfolio implication:

## 4. 🚀 Structural Opportunity Radar
Use this exact table:

| Theme | Primary ETF | Alternative ETF | Why it matters | Structural fit | Macro timing | Status | What needs to happen | Time horizon |
|---|---|---|---|---:|---:|---|---|---|

Then add a short paragraph:
- what is Actionable now
- what should Scale in slowly
- what remains Watchlist
- what is Too early

### Best structural opportunities not yet actionable
List the top 1-3 themes that are structurally compelling but not ready.

## 5. 📅 Key risks / invalidators
Separate into:
- Macro invalidators
- Market-based invalidators
- Geopolitical invalidators
- Second-order invalidators
- Portfolio construction risks

## 6. 🧭 Bottom line
Conclude with:
- what should be exited first
- what deserves additional capital first
- what is acceptable but replaceable
- **Single best portfolio upgrade this week:** [text]

## 7. 📈 Equity curve and portfolio development
This section is mandatory.

Include these exact summary lines:
- Starting capital (EUR):
- Current portfolio value (EUR):
- Since inception return (%):
- Equity-curve state:
- EUR/USD used:
- Notes:

Then include a compact table:

| Date | Portfolio value (EUR) | Comment |
|---|---:|---|

Then include this literal line exactly:
`EQUITY_CURVE_CHART_PLACEHOLDER`

## 8. 🗺️ Asset allocation map
Use a table.

## 9. 🔍 Second-order effects map
Use the required table.

## 10. 📊 Current position review
For each position:

### [Ticker] — [ETF name]

**Scorecard**
| Factor | Score | Weighted Contribution |
|---|---:|---:|
| Macro Fit | | |
| Geopolitical Fit | | |
| Second-Order Fit | | |
| Trend Quality | | |
| Relative Strength vs Alternatives | | |
| Downside Asymmetry | | |
| Opportunity-Cost Efficiency | | |
| Diversification Value | | |
| **Total Score** |  | **X.XX** |

**Assessment**
- Thesis status:
- Best reason to own:
- Key risk:
- Upgrade trigger:
- Downgrade trigger:
- Default score-based action:
- **Final action:** [Add / Hold / Reduce / Close]
- Override reason if any:
- Conviction tier:

## 11. ➕ Best new opportunities

### A. Macro-derived opportunities
[use full format]

### B. Structural opportunities
[use full format]

## 12. 🔁 Portfolio rotation plan
This section must remain easy to render as a compact matrix or table in the delivery layer.
### ❌ Close
### ➖ Reduce
### ✅ Hold
### ➕ Add
### 🔁 Replace

## 13. 📋 Final action table
Use this exact table:

| Ticker | ETF | Existing/New | Weight Inherited | Target Weight | Suggested Action | Conviction Tier | Total Score | Portfolio Role | Better Alternative Exists? | Short Reason |
|---|---|---|---:|---:|---|---|---:|---|---|---|

## 14. 🔄 Position changes executed this run
This section is mandatory.

Use this exact table:

| Ticker | Previous weight % | New weight % | Weight change % | Shares delta | Action executed | Funding source / note |
|---|---:|---:|---:|---:|---|---|

If nothing changed, still include the section and state that no share changes were executed.

## 15. 💼 Current portfolio holdings and cash
This section is mandatory.

Include these exact summary lines:
- Starting capital (EUR):
- Invested market value (EUR):
- Cash (EUR):
- Total portfolio value (EUR):
- Since inception return (%):
- EUR/USD used:

Then include this exact table:

| Ticker | Shares | Price (local) | Currency | Market value (local) | Market value (EUR) | Weight % |
|---|---:|---:|---|---:|---:|---:|

Then include a final row for remaining cash in the same spirit, either in the table or directly below it.

## 16. 🧾 Carry-forward input for next run
This section is mandatory.

Start with this exact sentence:

**This section is the canonical default input for the next run unless the user explicitly overrides it. Do not ask the user for portfolio input if this section is available.**

Then include:

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

## 17. Disclaimer

Use this full disclaimer text exactly:

This report is provided for informational and educational purposes only. It is not investment, legal, tax, or financial advice, and it is not a recommendation to buy, sell, or hold any security. It does not take into account the specific investment objectives, financial situation, or particular needs of any recipient. Views are general in nature, may change without notice, and may not be suitable for every investor. Investing involves risk, including possible loss of principal.
