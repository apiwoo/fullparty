---
name: harness
description: Delegation harness — run cheap implementer agents under the expensive main model's direction. Use when a change batch is fully spec-able (mechanical implementation, pattern application, parallel file batches) and worth offloading from the main model's tokens. Covers the spec-handoff contract, worker sandbox traps, degenerate-run detection, the two-stage bug pipeline, and the fallback protocol. Works with any worker CLI agent (Codex, a cheaper Claude, subagents) — the contract is model-agnostic.
---

# Harness — delegation party member

Respond to the user in their own language.

## The economics (why this member exists)

The main model (you) carries the judgment that can't be delegated: design, decomposition, review, real-runtime verification, owner communication. Implementation *volume* — once the design is decided — is token-expensive but judgment-cheap, which is exactly what a cheaper worker agent is for. The shape is always: **expensive model as architect/reviewer, cheap models as implementers**, regardless of vendor pairing (main↔Codex, main↔cheaper Claude tier, main↔subagents).

**Delegate when** the task is self-contained enough to write as one spec: mechanical implementation against a decided design, pattern application across many files, parallel independent batches, boilerplate-heavy subsystems.
**Never delegate**: taste/identity work (charter surface), cross-cutting design decisions, deterministic kernels (below), the *first* item of a new kind (doctrine: one through the pipeline before many), anything whose verification needs tools only you hold (engine runtime, screenshots, deploys).
**No worker available?** The same contract runs on your own subagents with a cheaper model — the harness is the structure, not a specific binary.

## Pairing presets (owner picks once, at harness setup — Tier 2)

The pipeline is main↔worker; the owner chooses which models fill the two seats. Present these presets **in this recommended order**, propose #1 as the default, and fall back down the list based on what's actually installed/available on the machine. Record the chosen pairing in `harness/RULES.md` (header line) and `.fullparty/progress.md`.

1. **Claude Fable (main) ↔ Codex 5.6 sol (worker)** — recommended default. Strongest design/review seat + a cross-vendor worker: different vendor = different blind spots, which makes the two-stage bug pipeline's independent investigation genuinely independent. Runs over the CLI invocation runbook below.
2. **Claude Fable (main) ↔ Claude Opus (worker)** — same-vendor pairing when Codex isn't installed (or its quota is exhausted). The worker runs as an in-harness subagent with a model override — no CLI wiring, no sandbox/ACL traps, shared tooling. The spec contract still applies verbatim (specs + SELF_CHECK, not chat): the discipline is what makes delegation reviewable, regardless of transport.
3. **Claude Opus (main) ↔ Claude Opus (worker)** — when the top tier isn't available or the budget calls for it. All-Claude, subagent transport, same contract.
4. **Codex 5.6 sol (main) ↔ Codex 5.6 sol (worker)** — for all-OpenAI setups (the user's main agent *is* Codex). The same contract documents drive it; the invocation runbook applies to the worker side.

Availability check before proposing: is the Codex CLI installed and current? which model tiers does the user's agent host expose? If the picked preset's worker turns out unavailable mid-campaign, offer the next preset down rather than silently degrading. Model names shift with generations — keep the *structure* (strongest-reasoning tier in the main seat, cheap/fast tier in the worker seat) and map current equivalents into these four shapes.

## Contract layout (per project)

```
harness/                   # or codex/ etc. — any name; keep one per project
  START.md                 # worker-facing: project one-pager + how to work here
  RULES.md                 # worker-facing: boundaries + project absolute rules
  templates/               # IMPL_SPEC / FIX_SPEC / INVESTIGATE_SPEC / SELF_CHECK
  sessions/{SID}/          # SID = {YYYYMMDD}_{short-slug}; exactly ONE spec per session
```

All main↔worker communication goes through `sessions/{SID}/` documents — never through chat, memory, or shared context. The worker reads START/RULES + its one spec; it writes `SELF_CHECK.md` and stops.

## Spec handoff (you write the spec)

- **Exactly one spec per session folder**: feature → `IMPL_SPEC.md`, agreed bug fix → `FIX_SPEC.md`, independent investigation → `INVESTIGATE_SPEC.md`.
- **Self-contained**: the worker must be able to do the job with zero access to your session notes, memories, or planning docs. If the spec needs context, the context goes *in the spec*.
- **Encoding armor (Windows-proven)**: write worker-facing docs in **English**, first line ASCII, via a UTF-8-writing tool. BOM-less UTF-8 Korean gets misread as CP949 by naive readers on the worker side — mojibake in, garbage out. Non-ASCII UI strings live in a **string table you pre-populate**, with the spec constraint "non-ASCII literals only from the string table".
- **Deterministic kernels are yours, not the worker's**: game-judgment logic that must agree across implementations (rule engines, scoring, economy math) you write yourself on every side, prove with **cross-fixtures** (identical input → identical output, fixture files in the repo), and hand off marked "DO NOT MODIFY — wiring only". The worker builds renderers/API plumbing around it; Done Criteria include re-running the fixtures.
- **Explicit file allowlist**: default = source files only. Engine assets (scenes, prefabs, metas) are editable only when the spec names the exact files.
- **No-network assumption**: worker sandboxes block network. Pre-install dependencies yourself before handoff; never put `pip install`/`npm install` in a spec.

## Invocation runbook (CLI workers)

Traps below are measured incidents, not theory:

- **Pin the working directory twice**: `cd` to the repo root before launching **and** pass the CLI's `--cd <repo-root>` (or equivalent) **and** state the absolute repo root in the prompt. Background shells lose cwd mid-run → "workspace unavailable" no-op exits.
- **Close stdin** on non-interactive calls (`$null |` pipe / `< /dev/null`) — exec modes otherwise hang waiting for EOF ("Reading additional input from stdin...").
- **Write-permission preflight (before the FIRST handoff, and after any folder was moved into the repo)**: a same-volume move breaks ACL inheritance on Windows, and the worker's sandbox identity silently loses write access — this exact trap ate three consecutive worker runs in a real sprint. Probe: create+delete a file in each target dir *as the worker would*; on denial, `icacls <dir> /reset /t /q`. (The engine skill's scaffold runbook has the same rule from the other side.)
- **Know your binary**: PATH often holds a stale copy that can't parse current config (instant death on unknown keys like `service_tier`). Resolve the real binary from the tool's own config/app install; re-resolve after app updates.
- **Sandbox mode flags drift**: prefer the current sandbox flag (e.g. `--sandbox workspace-write`) over deprecated aliases (`--full-auto`). If the sandbox refuses its own patch tool ("refusing to run unsandboxed"), workers usually self-detour via direct file writes — fine; if it recurs, single-root config overrides are the next lever.
- **A worker mid-run may ask a question into the void** ("reply 'continue'") — exec mode can't answer. Anything interactive-shaped in the spec (missing dirs, ambiguous choices) must be resolved *before* launch: pre-create directories, pre-decide choices.
- Long runs go to the background; you keep working other tracks and pick up the completion notification.

## Worker boundaries (put these in the project RULES.md)

- Worker edits source + docs and runs **static checks only** (compile checks, linters that work offline). Forbidden, no exceptions: engine/editor launch, servers, DB, browsers, network, deploys, git operations, E2E.
- Runtime verification belongs to the main model — SELF_CHECK ends with "runtime verification required" where applicable, and the worker stops there.
- Out-of-repo folders: read-only pattern reference at most; never modify.
- If a worker's investigation contradicts your analysis: it collects evidence and stops for arbitration — it never silently implements a different fix.

## Degenerate-run detection (exit 0 is not success)

Treat a run as **failed regardless of exit code** when any of: (a) it explored nonexistent file names, (b) the final message shows sentence collapse / incoherence, (c) zero artifacts were produced, (d) `SELF_CHECK.md` is missing. Protocol: **retry once with the spec tightened** (usually: exact paths nailed down — vague paths are the top degenerate-run cause). **Two failures on the same task → stop delegating and implement it yourself.** Announce the fallback ("worker blocked twice on X, taking it in-house"), log the cause in lessons, and don't sunk-cost a third run. Delegation is a cost optimization; it must never cost more than doing the work.

## Two-stage bug pipeline (keeps the worker's eyes independent)

1. **INVESTIGATE_SPEC**: symptoms + reproduction only — **your hypothesis deliberately withheld** (an anchored worker just confirms you). Worker writes findings with confidence levels (strong/medium/weak) + file:line evidence.
2. Compare its findings with yours. Agreement → **FIX_SPEC** with the agreed cause ("no re-litigating the diagnosis"). Contradiction → arbitrate with evidence before any fix.

## Review gate (yours, always)

- Cross-check `SELF_CHECK.md` against the actual `git diff` — spec coverage, boundary compliance, contract tables when both sides of an API changed.
- **Out-of-spec diff ≠ revert on sight**: check sibling `sessions/` first — it may be another session's legitimate work (a real incident: reverting a parallel session's work by assumption).
- Then run the real verification yourself: cross-fixtures, compile/build gates, runtime checks, screenshots. The worker's static pass is a claim, not proof (doctrine 1).
- Commit in the project's language/convention, update progress docs — the worker never touches git.

## Templates (drop into `harness/templates/`, adapt per project)

**IMPL_SPEC skeleton**: Read First (RULES.md) / Goal / Non-goals / Exact files to create-or-edit (allowlist) / Design decided (data shapes, endpoints, naming — no open choices) / String-table keys pre-added / Done Criteria (static checks + fixture re-runs) / Out of scope (git, deploy, network, runtime).
**SELF_CHECK skeleton**: per-spec-item status / spec-vs-code mismatches found & handled / contract table (server↔client keys·types·paths) when both sides touched / rule compliance checklist / risks / "runtime verification required" list.
