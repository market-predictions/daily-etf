# ETF Review OS — Decision Log

Use this file to capture stable architecture decisions so future sessions do not need to rediscover them.

---

## 2026-03-28 — Adopt Project + GitHub + Actions architecture
### Decision
The ETF flow will no longer be treated conceptually as one giant prompt-centered system.

### Chosen architecture
- **ChatGPT Project** = working memory and recurring workspace
- **GitHub repo** = explicit source of truth for prompts, scripts, outputs, and control docs
- **GitHub Actions + scripts** = real execution and delivery layer
- **Optional Custom GPT** = architect/reviewer only, not the primary runtime container

### Reason
This separates:
- thinking/work context
- system state and audit trail
- production execution

That reduces brittleness and makes debugging easier.

---

## 2026-03-28 — Add a control layer to the ETF repo
### Decision
A new `control/` layer is introduced to guide future sessions.

### Initial files
- `control/SYSTEM_INDEX.md`
- `control/CURRENT_STATE.md`
- `control/NEXT_ACTIONS.md`
- `control/DECISION_LOG.md`
- `control/CHATGPT_PROJECT_INSTRUCTIONS.md`
- `control/OPTIONAL_CUSTOM_GPT_SPEC.md`

### Reason
The previous setup had strong execution files, but no single authoritative session-start path.

---

## 2026-03-28 — ETF should move toward explicit state files
### Decision
ETF should evolve toward explicit implementation files similar in spirit to the FX system.

### Planned direction
Potential future files:
- `output/etf_portfolio_state.json`
- `output/etf_trade_ledger.csv`
- `output/etf_valuation_history.csv`
- `output/etf_recommendation_scorecard.csv`

### Reason
Relying mainly on prior report parsing is functional but weaker than using explicit state files for implementation facts.

---

## 2026-03-28 — Do not use the optional GPT as the production runner
### Decision
If a helper GPT is created, it should be used for:
- architecture review
- prompt refactoring
- script/workflow review
- consistency checking

It should **not** be treated as the canonical production runtime.

### Reason
Projects and GitHub together are better suited for long-running context plus state and auditability. A GPT is better as a specialist tool than as the main container.
