---
description: Server party member — server-authoritative backend design and build, economy/persistence integrity, old-client compatibility gates, deploy rails with test isolation, server-side security.
allowed-tools: Read, Grep, Glob, Bash, PowerShell, Write, Edit, AskUserQuestion, Task
---

# /fullparty:server

Engage the **server** skill (see `skills/server/SKILL.md`). Respond in the user's language.

- Server is the authority: combat, probability, economy, and every rejection gate resolve server-side; the client sends intent, never results.
- Money rules are non-negotiable: single grant path, ledger+balance in one transaction with an idempotency key, CAS transitions, negatives sanitized at every read.
- Before any protocol/data change ask: "can the not-yet-reviewed old client still play right after this deploys?" — additive extension only.
- Deploys go through the rail (import check → tests → health-gated rolling restart); test-server isolation by default, live push only on an explicit owner go.
