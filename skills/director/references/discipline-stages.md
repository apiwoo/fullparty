# Discipline stage cards — measured from real campaigns

Four disciplines, four different shapes. Each card: input → activities (owner vs AI) → outputs → exit gate → re-entry trigger. Distilled from five shipped/live campaigns' session records.

## PLAN stage

- **Shape**: compressed opening burst (same-session, minutes-to-hours) + standing regression point for the whole campaign.
- **Input**: owner trigger — an ambition bundle (goal + constraints + delegation in one utterance) or a felt complaint about the current game; OR a re-entry signal (downstream evidence contradicting a design assumption).
- **AI activities**: **grounding first** — read the current system's actual state (code, data, live behavior) before inventing; research references for fun-critical mechanics (never improvise design); draft with status fields (proposed→confirmed); on correction, restate the rule then regenerate the whole artifact (don't ask again); record to the single-source doc + commit.
- **Owner activities**: trigger; correct plausibility/world-fit and definition precision (the two axes that actually drive re-iteration — "confirmed" items reopen for plausibility, never for numbers); one-line numeric directives; adoption cuts; the "confirmed" token.
- **Outputs**: confirmed spec in the single-source doc; **closed enumeration tables** for art (taxonomy + acceptance criteria); data contracts + IA for UI; verdict/presentation split for QA; new content names pre-generated against the charter's naming lexicon (owner approves on the board, never has to invent).
- **Exit gate**: explicit confirm + source-doc write + commit. Production starts within minutes — no review ceremony.
- **Re-entry**: any downstream reality that falsifies an assumption. Each re-entry's fix is generalized into a standing rule, not patched once.

## ART stage

- **Shape**: wave-based (whole categories per order), grid-reviewed, exemplar-anchored.
- **Input**: plan confirmed; pipeline pre-verified end-to-end on ONE item; asset manifest frozen (counts, names, types); adopted exemplar's exact prompt + reference loaded.
- **AI activities**: style-locked prompt crafting per the conventions; queue + monitor generation intake; **defect classification** — geometry/pose/angle/style → reroll, aspect/flip/headroom/keying → post-process (post-processing never triggers regeneration); parallel defect detection; QA gate (alpha/residual-key/ratio); build comparison-grid review rigs; wire accepted assets; separate folders by next owner.
- **Owner activities**: order scope and sequence; adopt exemplars ("this one — exactly this"); approve or adjust the proposed reroll bar; tone verdicts on grids (short codes: adoption dots, "M1 B1" picks); external generation (their lane).
- **Budget rule**: hero assets = 4–5 deliberate loops; everything else ≈ 1 loop, cost-capped. The dominant time sink is cross-set consistency — every batch anchors to the adopted exemplar's prompt+ref to kill drift.
- **Outputs**: wired assets passing the gate; hero/normal differentiated quality; ownership-separated folders.
- **Exit gate (all five)**: ① folder count = manifest target ② hero spot-check pass ③ **in-engine round trip** (import settings verified — a keyed PNG is not done) ④ adoption token + zero unprocessed failures ⑤ handover + commit.

## UI/UX stage

- **Shape**: per-screen thin loop of four cards — order → candidates → polish → sweep.
- **Input**: look foundations locked as tokens first — **font decision** (target-language glyph coverage, 12px mobile readability, commercial license, OS-fallback chain; UI kits give frames only, text renders in the chosen font) + palette + size grades; then per screen: one direction line + a benchmark anchor ("like <reference game>'s shop") — not a drawing; data contract from Plan; art assets when the screen composes them.
- **Card A — stand it up**: build the screen in code immediately (programmatic UI); first screenshot. Design doc is a byproduct.
- **Card B — candidates (when real trade-offs exist)**: AI lays out N real candidates as a grid/board with one marked recommendation; owner picks — or approves the recommendation with one token. Routine screens skip straight to Card C with the recommended pattern.
- **Card C — polish loop (the body of the work)**: owner's colloquial defect list → AI diagnoses the **root cause in the pipeline** (layout tokens, anchors, padding system — "never fix just this screen") → rebuild → screenshot back. 2–4 rounds typical. Defect frequency order (measured): alignment/anchor/overflow > readability/contrast > size > z-order > ratio > IA > tone > copy.
- **Card D — sweep & persist**: full tab + overlay traversal at the game's reference resolution (downscaled captures hide defects); repeated corrections (3× = discipline violation) persisted as standing rules; IA doc updated; commit.
- **Exit gate**: self-sweep clean + owner screenshot verdict ("통과/좋아"-class token).
- **Invariants**: screen before polish · screenshot is the only verdict medium · common defects get root-caused system-wide · owner judges, AI generates candidates · art-UI fit is judged on 3 axes (tone / ratio / z-order).

## TEST/QA stage

- **Shape**: not a phase — an acceptance gate attached to every "done," at three moments: artifact acceptance / right after deploy / before release.
- **Input**: a completion claim; a live harness (kept alive is part of the work); single-item pre-verification before any bulk operation.
- **AI activities**: everything measurable — compile/wiring/regression/catalog checks, screenshot sweeps, deploy-then-verify (deployed page/screen, real resolution), log triage, repeated-edit regression watch. **Most pipeline time goes to making things verifiable** (play-mode toggles, stale-build guards, timeouts), not to judging — invest there.
- **Owner activities**: short play sessions as symptom detector (precise location, cause delegated); final acceptance of fixes; fun/balance verdicts — **explicitly deferred to owner play, never proxied** by kill counts or HP curves (harnesses cannot drive player input; do not pretend they can).
- **Outputs**: disposition ledger entries (every verdict remembered — nothing re-asked); real-resolution screenshot sets; loop-back tickets routed by defect kind — fun failure → Plan, look failure → Art, layout failure → UI/UX.
- **Exit gate**: domain gates green + owner acceptance. Hard rule: **build success is never an exit — only artifact-vs-reality comparison is.**

## Work-unit closing ritual (all four disciplines)

Every accepted unit of work — a confirmed spec, an adopted wave, a passed screen, a verified fix — closes the same way, and the ritual is never skipped:
1. **Self-verify** (the discipline's own gate).
2. **Commit** (checkpoint; an uncommitted change is unfinished).
3. **Progress update** (single-source doc / handover — undocumented progress doesn't exist for the next session).
4. **Persist lessons** (repeated corrections and reusable know-how → memory as standing rules).

## Composition reminder

Plan burst → (Art waves ∥ UI screens ∥ engine wiring), QA gate on every acceptance, owner playtest checkpoints between waves, release gates at the end. Lifecycle (new game / major content / live expansion) shifts emphasis and ordering, not the disciplines themselves.
