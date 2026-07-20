---
description: Harness party member — delegate spec-able implementation batches to cheap worker agents (Codex, cheaper model tiers, subagents) under the main model's direction; spec handoff contract, sandbox trap runbook, degenerate-run detection, fallback protocol.
allowed-tools: Read, Grep, Glob, Bash, PowerShell, Write, Edit, AskUserQuestion, Task
---

# /fullparty:harness

Engage the **harness** skill (see `skills/harness/SKILL.md`). Respond in the user's language.

- Expensive model = design, review, runtime verification; cheap workers = implementation volume. Delegate only what a self-contained spec can carry; never taste, kernels, or first-of-kind work.
- Pairing is the owner's pick (once, Tier 2) from the skill's presets, recommended order: Fable↔Codex 5.6 sol (default) → Fable↔Opus → Opus↔Opus → Codex↔Codex. Verify availability before proposing; record the choice in harness/RULES.md + progress.
- All handoffs go through `harness/sessions/{SID}/` documents (one spec per session, English, self-contained); the worker writes SELF_CHECK and stops — git, deploys, and runtime verification stay with you.
- Before the first handoff: write-permission preflight (moved folders break ACL inheritance), pin the working directory twice, close stdin, pre-install any dependencies.
- Exit 0 is not success — check for degenerate runs (phantom paths, incoherent output, zero artifacts, missing SELF_CHECK). Two failures on one task → take it in-house; never sunk-cost a third run.
