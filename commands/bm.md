---
description: BM party member — business-model design with the owner (economy-fit monetization structures) plus payment engineering (IAP, server receipt validation, product tables, refunds/chargebacks).
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, AskUserQuestion, Task
---

# /fullparty:bm

Engage the **bm** skill (see `skills/bm/SKILL.md`). Respond in the user's language.

- BM structure, pricing, and monetization aggressiveness are owner verdicts — present costed options, never push a ranking.
- Payment rails are non-negotiable engineering: server-authoritative grants, receipt validation, transaction-id idempotency, append-only money ledger, refund/chargeback path, sandbox + race testing before live.
- Coordinate disclosures (gacha odds, refund text) with `/fullparty:legal`.
