---
name: server
description: "Server party member — design, build, and deploy the game's backend: server-authoritative architecture, economy/persistence integrity, client-server contract compatibility (old clients keep playing), deploy rails with test isolation, schedulers/migrations, server-side security. Use whenever the game needs an online backend or any server-side change."
---

# Server party member

The server is the game's authority and the owner's money — every rule here was paid for in live operation. Unlike player-visible surfaces, the backend is invisible infrastructure: **reusing these exact patterns across games is correct**, not sameness. Respond to the user in their own language.

## Architecture defaults

- **Server-authoritative, thin client.** Combat, probability, balance, and economy resolve on the server; the client sends intent (target id, action), never results (no damage values from the client). Balance/config ship as server data so numbers tune without a client build.
- **Single source of truth.** Numbers and contracts live server-side; hunt down client hardcoded literals. Verify SSOT guards by fault injection — deliberately skew a server constant and confirm the guard catches it.
- **Rejection gates are server-enforced** (version, admission, cheat, maintenance, launch). A client-only gate is bypassed by old or modified clients. Force-update = server boot gate + kicking online old clients so reconnection re-enters the gate.
- **Boring stack first**: one process (single event loop is fine), reverse proxy in front, SQL DB bound to localhost, cache/bus only when needed. Scale later by sharding **behind an env flag whose absence = 100% old behavior** — big features must roll back with one line.
- **Live switches live in the DB**, read per-request (launch gate, exposure flags) — flipping them must not need a restart.

## Managed backends (BaaS) — same principles, mapped

Firebase / Supabase / PlayFab and kin count as "the server"; the principles are stack-agnostic, only where they live changes. Server-authoritative = outcomes resolve in Cloud/Edge Functions (CloudScript etc.), **never** client-SDK writes straight into authoritative state. Rejection gates = security rules **plus** function-side validation — rules alone are access control, not game logic. Ledger + idempotency = the same tables/collections with a unique key on the transaction id (use the platform's transaction/batched-write API). Live switches = Remote Config / DB flags. What needs a platform substitute: staged rollouts and health-gated restarts. Managed fits sessionless/turn-based games well; a realtime authoritative simulation still wants a real server process.

## Economy & persistence invariants (the money rules)

- **One grant path per reward.** Broadcast/display code never grants; the moment two paths can pay the same event, you have a duplication bug (live incident: kill-event broadcast and reward-distribution both paid → double currency, duplicated drops).
- **Ledger + balance in one transaction**, ledger append-only, with an idempotency key (account, reference, reason) — and a **composite index matching exactly that dedup query** (a single-column index full-scans a ledger with millions of rows; build big indexes `CONCURRENTLY` or you stop the live DB).
- **State transitions use CAS**: `UPDATE ... WHERE value = old_value` + RETURNING, queue exactly one delta per real transition. Blind overwrites + fire-and-forget deltas re-applied on retries destroyed player currency live.
- **Sanitize negatives at every read entry point** (`max(0, v)`) — one negative currency value poisons every calculation downstream.
- **`ON CONFLICT DO NOTHING` ordering trap**: if a zero-value row claims the idempotency key first, the real grant is blocked forever — guard empty-pool cases before insert.
- **Persistent keys are always real account ids.** Runtime/synthetic ids are fine in memory and broadcasts, never in DB/push/ledger writes (synthetic-id leaks silently drop rows).
- **Respect session ownership** (realtime/session-authoritative games). If an HTTP mutation touches an in-memory authoritative session owned by another process/shard, delegate to the owner — writing the DB underneath gets overwritten by its stale flush. On handoffs, persist the source's true state *before* redirecting the client.
- **One-shot backfills/migrations**: run only after the code fix is live (restarted, not just copied), grant+ledger+idempotency key in one transaction, target set explicitly bounded, marked never-re-runnable.

## Client↔server contract & backward compatibility

The standing question before any protocol or data change (owner's own gate): **"right after this deploys, can the not-yet-reviewed old client still play?"** If the answer isn't a confident yes — stop.

- Store review freezes old clients for days. **Never ship a change that requires client+server deploying together**: opcode/integer-key maps, field renames or type changes, endpoint paths. Extend **additively only** (new keys, new message types) + capability negotiation per connection.
- **Hardcoded count couplings crash boots in both directions.** Where client constants mirror server data lengths, serve truncated data per client version (`?count=N` style) and make clients tolerant of extra entries.
- **Gate new content at every emission point** (gacha, craft, exchange, quests, boxes) by client version — otherwise old clients receive entities they can't render and items silently "disappear".
- Rate-limit throttles must **exempt control messages the client applies optimistically** (enter/leave etc.) — silently dropping them causes permanent desync; throttle real combat actions only.

## Deploy rails (build these before you need them)

- **Deploy script = import check → full test suite (fail = abort, server untouched) → health-gated rolling restart.** Ship changed tests together with changed runtime files, or the gate blocks with stale tests.
- **Code on disk ≠ code running.** Each process serves what it loaded at start; a partial upload that breaks the import graph is a mine that "runs fine until restart". Verify import after every upload; pick restart scope by change scope (cross-process protocol change → restart everything together; unsure → everything).
- **Done = deployed and verified on the real server.** Domain result markers ("N ok / 0 failed", zero errors in log), never exit codes; never infer deployment state from commit timestamps. No false "deploy complete" reports — check health output before announcing.
- **Test isolation**: cheat/wipe APIs exist only on test instances (IP-allowlisted); **live push always waits for an explicit owner go** (inherited hard rule). Wipe/ops scripts run in the venv — the system interpreter missing a driver "succeeds" with 0 rows.
- Graceful shutdown flushes all in-memory pending state (currency, progress, items) to DB. Back up whatever a deploy replaces — move, don't delete.
- **Load test before launch** (the launch member walks this gate): ramp concurrent sessions plus a day-one login storm against the test instance, race the heaviest endpoints, and record the capacity number and what breaks first.
- **External compute engines warm up once per machine** (game-AI engines like KataGo/Stockfish, local ML models): the first query may auto-tune/JIT for minutes on a new machine or GPU, then cache. Absorb it with a startup warmup query (server lifespan hook), give first-run integration tests generous timeouts (120s+), and put the warmup wait in the deploy runbook — otherwise the first real user eats it, and CI reads the tuning stall as a hang.

## Schedulers, time, sessions

- **Daily jobs: short poll (60–90s) against wall-clock targets with an idempotency guard.** A `sleep(24h)` loop drifts later every day on monotonic clocks (live incident: midnight settlement 20+ min late).
- Reconnect/grace timeouts are **named standard constants** — no ad-hoc 90/120s values scattered around.
- **Rekeying a session id must move every parallel keyed index** (realtime games). One missed map = permanent desync; the fingerprint is a periodic orphan-sweep log line. New keyed structure → add it to the rekey function in the same commit.

## Accounts & auth

- **Guests-first**: a device-bound guest account with a real server id from the first session; **linking** (OAuth / store account) upgrades that account in place — never create a second account on link (orphaned guest progress is a classic CS disaster). Design and test the collision case explicitly: guest progress + already-linked account on the same credential → an owner-approved merge/choice rule, not an accident.
- Sessions: short-lived tokens with server-side revocation; one canonical account id in every table (persistent keys are real account ids — same doctrine as above).
- **Account deletion is a launch requirement, not a feature**: stores and privacy law require it. Erase/anonymize personal data while keeping ledger integrity (anonymize the account, never break referential money records) — coordinate with the legal member's register.

## Security & secrets

- DB binds localhost-only; admin APIs = header key + IP allowlist (double gate); all probability uses CSPRNG, never a seeded Mersenne Twister.
- **User secrets stay local and gitignored** — help the owner manage them (env files, key storage), verify nothing is publicly exposed, but disposition (rotate/delete) is the owner's call, never forced. Non-reissuable credentials (store signing keys) get an offline backup.
- For headless self-verification behind auth, **mint a test session server-side** and inject it — the secret never leaves the server; the real auth path stays human.

## Observability foundation (liveops runs on this)

- **One log file per process** — shared files lose lines on rotation. After scale-out, grep **all** workers before concluding "it didn't happen" (single-worker grep produced false not-present verdicts twice, live).
- System-wide alerts fire from one designated instance only (per-instance metrics from each); alert on sustained breach, not single spikes. Dashboards aggregate across all processes — partial polling reads as "players ≈ 0".

## Party boundaries

**bm** designs monetization — you implement its rails (receipt validation, idempotent grants, money ledger). **liveops** runs the live game on the rails you built (monitoring, incidents, maintenance flow). **engine** owns the client half of every contract — a contract change is always a reviewed pair, never one side alone. The QA guard scans server diffs like any other change: economy paths and compat gates are exactly where its regression memory earns its keep.
