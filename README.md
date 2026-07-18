# Fullparty — your full party for solo game development

You're making a game alone. **Fullparty gives you the party**: AI party members that build with you, and a guard that protects what you've built.

**Your role is deliberately small**: produce assets (generate images on the platform you like, grab things from asset stores) and **playtest your own game**. Everything else — code, UI construction, engine operations, imports, placement, verification — the party does. It drives Unity/Godot **headlessly (batch mode)**; it never asks you to click around the editor.

## The party (free, local)

- **`/fullparty:director`** — Party leader. Runs a whole production campaign (new game / major content batch / live expansion): phases the work, dispatches the other party members, enforces production doctrine distilled from real shipped-game campaigns (reality-only verification, enumerate-before-build, one-through-the-pipeline-before-many, back-up-before-you-break...), and interrupts you only for the calls that are yours — fun, tone, cuts, live pushes. Everything derived from your concept (names, styles, layouts) arrives as a filled-in recommendation you approve or strike — never an open question.
- **`/fullparty:art`** — Art party member. Crafts style-locked, consistency-controlled prompts for you to run on any image platform → you drop the results in a folder → it post-processes locally (chroma-key cutout, sheet slicing), QA-gates every asset (alpha/residual-key checks, auto-flag rejects), and places them into the game.
- **`/fullparty:ui`** — UI party member. Builds your game UI entirely in code (programmatic UI: safe-area, fonts, panels, toasts — no scene fiddling), then self-reviews with screenshot checks.
- **`/fullparty:engine`** — Engine party member. Drives Unity/Godot directly: headless compile gates, batch imports, scene placement via editor scripts, build + freshness verification. Web games run the same doctrine through a deploy → headless-browser-screenshot loop.
- **`/fullparty:server`** — Server party member. Builds your game's backend server-authoritative from day one: economy integrity (single grant path, idempotent ledgers), old-client compatibility gates, deploy rails with test-server isolation — rules paid for in live MMO operation.
- **`/fullparty:sound`** — Sound party member. Sweeps the game for every sound it needs → hands you precise sourcing sheets (asset-store specs or sound-AI prompts) → intakes what you bring back, wires it, tracks licenses, verifies coverage.
- **`/fullparty:bm`** — BM party member. Monetization structures designed with you against your economy, then the payment rails: IAP, server receipt validation, idempotent grants, money ledger, refunds.
- **`/fullparty:launch`** — Launch party member. Release builds, store listing, age rating, submission checklists, rejection response, launch-day rollout/rollback plan.
- **`/fullparty:legal`** — Legal party member. Privacy policy, terms, gacha-odds disclosures, licenses/credits — drafted from your game's reality, for your review.
- **`/fullparty:liveops`** — LiveOps party member. Monitoring, log triage, incident/hotfix runbooks, maintenance flow, CS-signal triage — live pushes always wait for your go.

Your game's identity stays yours: player-visible choices (art style, proportions, UI frame, fonts, audio tone) are locked per game with you in each project's charter — the party ships methods, never a house style.

## The guard (server, API key)

- **`/fullparty:init`** — register the project (opens your server-side judgment ledger). Once per project.
- **`/fullparty:scan`** — QA scan against a living failure catalog distilled from shipped live games: sends a diff/manifest **summary** (never raw source) → server returns the checks relevant to *your* change → runs locally → report.
- **`/fullparty:triage`** — judge findings in plain language; judgments are remembered server-side. **A question answered once is never asked again** — the guard knows your game better every scan.

**No signup.** Your agent gets an API key automatically (`POST https://fullparty.dev/signup`) during setup — free during open beta, unlimited.

## Install

**Just tell your AI coding agent** (Claude Code, Codex, or any other) — that's the whole install:

```
Set up Fullparty from https://github.com/apiwoo/fullparty and be my party for this game.
```

The agent reads [`AGENTS.md`](AGENTS.md), clones the repo, wires the party into your project, and gets to work. You never type a slash command unless you want to.

## What ships here (and what doesn't)

- **Ships:** the party skills (director + 9 specialists — local, yours), thin command wrappers, `.mcp.json` server connector.
- **Server-side:** the failure catalog, matching engine, and your per-project bug memory (the guard's brain).
- The AI speaks **your language**; your code never leaves your machine.
