# ETF Review OS — Current State

## Snapshot date
2026-03-28

## What this repository currently is
This repository is already a working production-style report system for a weekly ETF review. It has:

- a strong masterprompt in `etf.txt`
- a delivery/rendering script in `send_report.py`
- a GitHub Actions workflow in `.github/workflows/send-weekly-report.yml`
- archived outputs in `output/`
- supporting latest-output folders

## Current strengths
- Strong determinism and anti-drift intent in the prompt.
- Explicit premium HTML/PDF delivery contract.
- Mandatory pricing pass before analysis.
- Strong fail-loud language around GitHub write, PDF generation, and email delivery.
- Good client-layer versus analyst-layer structure.
- Good discipline around carry-forward continuity and model-portfolio tracking.

## Current weaknesses
### 1. Prompt monolith
The current ETF system still mixes too many responsibilities in one file:
- decision framework
- input resolution
- pricing logic
- output formatting rules
- workflow orchestration
- delivery completion criteria

This makes the system powerful, but also harder to debug, extend, and keep stable.

### 2. Too much operational truth still lives inside prior reports
The current fallback chain leans heavily on the latest stored report. That is workable for continuity, but it is not the cleanest long-term state model.

### 3. ETF state is less explicit than FX state
Compared with `daily-fx`, the ETF flow currently has less explicit separation between:
- historical artifact
- implementation state
- valuation history
- recommendation history

### 4. Project/GitHub operating split has not yet been formalized
The intended future architecture is clear, but before this control layer there was no single starting point telling a future session what to read first and what is authoritative.

## Target architecture
### ChatGPT side
- One dedicated ChatGPT Project called **ETF Review OS**.
- Project instructions focused on operating discipline, not giant embedded repo logic.
- Minimal high-value files uploaded to the project for recurring work.

### GitHub side
- GitHub remains the source of truth for prompts, scripts, workflows, outputs, and control files.
- Control files guide sessions and reduce re-discovery costs.
- Over time, ETF should externalize more explicit state files similar to the FX system.

### Delivery side
- Delivery should remain in scripts + GitHub Actions.
- The prompt should define reporting and decision quality, but not be the only operational brain.

## Immediate priorities
### Priority A — stabilize the operating layer
Completed in this step:
- create a control layer in GitHub
- create a single entry point file
- create a current-state file
- create a next-actions file
- create a decision log

### Priority B — create the ChatGPT Project manually
Still required:
- create the actual ChatGPT Project in the UI
- paste project instructions
- upload the small set of canonical files you want always available inside the project

### Priority C — refactor the ETF prompt into layers
Planned next:
- split `etf.txt` conceptually into:
  - decision framework
  - state/input contract
  - output contract
  - runbook

### Priority D — externalize ETF state more explicitly
Planned after prompt-layering:
- add ETF state files for portfolio state, valuation history, trade ledger, and recommendation history
- reduce dependence on parsing old reports as operational truth

## Recommended session start sequence
For any future ETF architecture session:

1. read `control/SYSTEM_INDEX.md`
2. read this file
3. read `control/NEXT_ACTIONS.md`
4. only then open the specific execution file relevant to the task

## Current role split
### Manual by user
- create the ChatGPT Project
- paste project instructions
- upload selected project files
- optionally create the helper Custom GPT in the GPT builder

### Can be done by assistant
- design the project instructions
- design the GPT spec
- create and update GitHub control files
- propose and write new repo files
- refactor prompts
- propose script and workflow changes
- create non-destructive scaffolding directly in the repository

## Current status label
**Architecture transition in progress — GitHub control layer initialized, ChatGPT Project layer still manual/pending.**