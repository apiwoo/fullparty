# Production doctrine — evidence and case histories

Distilled from five real solo-dev campaigns run with an AI party, one per lifecycle stage:

| Campaign | Lifecycle | Shape |
|---|---|---|
| A | New game 0→1 | One-week survivor-like sprint on top of an existing combat prototype; art pipeline built first |
| B | Major campaign, in-engine | Fantasy action RPG built live inside the engine via MCP (assets, meshes, terrain, VFX, launch prep) |
| C | Major content pivot | Idle RPG full concept pivot: research → 300+ art assets → wiring → hardening |
| D | Web live service | Browser game platform with **no local runtime** — deploy-to-verify loop on the live server |
| E | Live MMO expansion | 4 characters + 4 dungeons + 4 biomes added to a running MMO with backward-compat constraints |

A rule made core doctrine only if the owner had to enforce it in **three or more** of these campaigns. Everything narrower is in the "special patterns" section at the end.

---

## Part 1 — Core doctrine: where each rule came from

### 1. Reality is the only proof
- **A**: The AI reported a UI fix "complete" while the screen was unchanged — "are you actually looking at this in the editor?" repeated three times. Root cause of one miss: inspecting a 720px downscaled screenshot where overlapping borders blur away. Rule extension: inspect at real resolution (1080).
- **B**: Left alone, the AI inserted 30 toolbox models trusting their names — "giant spider" turned out to be a tree, a playground ride, an NPC. The asset load-state API was also proven untrustworthy (reported 0/100 loaded while all 100 rendered). The only ground truth that survived: force-render + screen capture.
- **C**: The AI reported a generation batch "complete" from a log's exit 0; physical inspection showed no run had actually happened since the last interruption and two failures were never regenerated. Rule: completion is judged by opening the artifacts (files, pixels, counts), and by domain result markers ("N ok / 0 failed", "0 compile errors") — batch runs returned exit 0 while actually aborting midway.
- **D**: The decisive event of the whole project — the owner asked "can't you look at the browser yourself and give feedback?" and the headless-screenshot self-verification loop was born on the spot, becoming the standard cycle (deploy → screenshot → fix). For logged-in pages, the AI minted a test session server-side (secret never leaves the server) to see past the login wall.
- **E**: Every batch closes with a verification checklist (migration counts, import settings, bundle format scan, log error scan, ScriptableObject value diff) before the final report.

**Violation cost**: repeated owner rage, silent half-done batches, a week of art built on unverified assumptions. This is the #1 most-repeated correction across all five campaigns.

### 2. Enumerate before you build
- **E** (origin, strongest): Before adding 4 dungeons, a parallel survey mapped every hardcoded `COUNT = 20`, the `entries.Length != COUNT → reject` gates scattered across client files, and the `dungeon_id = array index + 1` scheme — which surfaced that two special dungeons lived *outside* the array, so naive append would collide slots. The survey also exposed the hidden max-workload item: each generic dungeon boss is a full new character. Both became explicit decisions **before** code.
- **C**: Before the pivot, read-only agents surveyed the source project's newest pipeline and inventoried reuse (49/63 monsters, 18/19 effects kept); a later hardening pass swept 44 client literal sites into a single roster constant.
- **B**: Content phase opened with "check what's *not* built yet in the current systems" before the economy simplification; scrapping the loot currency was preceded by a 6-script impact survey.
- **D**: Every task starts with a full read of existing docs and game code before the handoff spec is written.

**Violation cost**: on live systems, backward compatibility breaks silently — a count-gate mismatch makes the client reject the server's data wholesale.

### 3. Precedent before invention
- **E** (most-repeated instruction of that campaign): "check how it was wired before", "check the original monster prompts first", "look at the existing legendary aura effect properly". When the AI generated from an abbreviated prompt instead of the original, style and spec drifted (chibi proportions went stubby, wrong chroma color chosen).
- **C**: "0-stage tool migration first" — the proven pipeline was excavated from the source project and ported (hardcoding removed), each tool verified before use, instead of reinventing.
- **A**: "check what exists first, then rewrite the plan" before scrapping anything; the shell screens were ported wholesale from a sibling project's proven pattern; when confused about asset formats: "look at the existing sprites."

### 4. One through the pipeline before many
- **C**: The full chain (generate → chroma → derive) was proven on a single asset before the ~300-asset run. The biggest rework of the campaign (104 images regenerated) came precisely from a spec error that a single-item check against *use* (attack/run motion bases, not idle) would have caught.
- **E**: "Don't go all at once — cut it up": one character generated and approved before the batch of four; sample-then-batch as standing rule.
- **A**: Day one was mostly pipeline debugging on single images; mass biome/monster production only started once the pipeline held. The payoff: a full theme swap (total reskin) later cost half a day.
- **D**: Expensive generation (≈25 min/asset) made the owner explicitly forbid regeneration when post-processing sufficed — same economy, different lever.

### 5. Minimal delta by default; rewrite is an owner verdict
- **B**: "The axe just needed a small angle tweak from the earlier pose — what are you doing?" after the AI began rebuilding a grip from scratch. The opposite verdict also exists — "this terrain is a patchwork, delete the river and redo it from zero" — and the deciding party in both directions was the owner, never the AI.
- **D**: "I'm not asking you to remake it, just touch it up" — canvas re-composition, chroma cleanup, frame re-layout instead of regeneration; a standing post-processing toolset exists for exactly this.
- **A**: Tone fixes were always "keep the approved reference, change only X" — never regenerate the identity.
- **E**: "16:9 means pad the square image with margin, not generate at 16:9" — reinterpret instructions in the owner's vocabulary; the minimal transformation is the intended one.

### 6. Back up before you break
- **B**: Terrain edits (hardest to undo) were preceded by region snapshots, replayable in reverse to restore.
- **E**: Every replaced asset went to a dated `_Legacy_{date}/` folder — delete forbidden; batches are idempotent so a crash mid-run re-executes safely ("stopped before overwrite; the existing 34 images are untouched").
- **A**: A 4GB cleanup was done as *move to `_Legacy` (recoverable)*, after reference-safety verification — never delete.
- **C**: During the redesign adoption gate, existing versions were preserved until the owner formally adopted the new direction.

### 7. Suspect your own inertia
- **C** (origin, three separate incidents): the AI carried the source roster's all-female cast into a pantheon ("not every god can be a woman?"), copied the source's idle-pose chibi when the actual need was attack/run motion bases (104-image rework), and drifted into dictionary-translation naming ("reads like translated text") requiring a full renaming pass. All three had the same root: repeating the source project's pattern without asking whether it fit the new world/use.
- **A**: Tone drifted batch-over-batch (cutesy↔sexy, skin color, chibi ratio) unless anchors were explicitly restated in each prompt.
- **B**: Rivers were placed in every region including desert and ice ("no rivers in a desert"), stone-named materials weren't stone — theme coherence lost to habit.

### 8. Lock set standards and anchor to references
- **A**: A monster source was regenerated five times because its view angle (3/4-right) didn't match the set and the AI kept flip-flopping between side and 3/4. Fix: pin the set standard in writing, force direction words into prompts, and diff every new item against the existing set. Same campaign: one-conversation generation for style-locked sets; approved reference attached with "keep face/ratio/style, change only X".
- **E**: Standing per-project invariants the owner had to repeat until made automatic: floor color ≠ monster color, chroma key must be a specified color (never white), no border lines at frame edges, headroom above heads so weapons don't clip.
- **B**: Tier progression must read simple→ornate low→high (mixed-up tiers called out instantly); bosses/landmarks at presence scale (a 1.4× boss rule was constant-ized).
- **C**: In-chat generation drifted by image 3–4 of a group (hat/mane color mutating) — fixed by pairing every generation with an approved full-body reference image.

### 9. Automation first
- **A** (strongest single correction in the corpus): the AI answered an image task with "I'll give you the prompt to run yourself" while the owner's own automation pipeline existed — met with fury and immediately burned into memory: if a tool exists, the AI runs it end-to-end; handing back manual work is forbidden.
- **E**: "I closed the editor — you do all of it yourself" — batch-mode builds, migrations, verifications fully delegated (with the live push explicitly carved out).
- **D**: "You can do image generation in parallel too" — sequential processing where parallel was possible got called out; two worker sessions + art pipeline concurrently became the norm.
- Caveat for the shipped product: the plugin's art member deliberately hands *generation* to the user (external platforms, ToS boundary). "Automation first" applies to local tools and pipelines and must never override the division-of-labor boundary.

### 10. Increments with visible markers; kill on wrong direction
- **A**: "How many minutes until this counts as failed?" — background generation had no timeout/rate-limit detection; the owner demanded self-detecting failure handling (and new unrecognized failure strings get added to the detector).
- **C**: Queue + monitor split, with the monitor's filter tightened after it mistook normal wait logs for failures; slowdown vs content-block diagnosed by failure pattern. Batch B was **killed mid-run** the moment the all-female-cast problem was spotted — correction beats completion.
- **E**: "Stop the running generation immediately and check the existing output" — wrong-direction work is killed, not finished. Numeric tuning ran as explicit before→after loops ("what did you change, X→Y?"), including converting "new offset" to "0→0.18".

### 11. Never improvise design
- **A**: The AI admitted "I was building from my own arbitrary interpretation" and was stopped; fun-critical systems (augments, weapon archetypes) were designed only after competitor/genre reference research, with direction set by the owner. AI-invented mechanics (escort/evac) were rejected for simpler proven models.
- **B**: The standing response shape was mandated: organize the rules → propose → ask only the questions that need a decision. The owner only decides.
- **C**: The campaign opened with a parallel research fan-out (folk-religion systems, media references, market) and the design emerged from findings ("the lore already exists — map it") rather than invention.
- **D**: In economy simulation the AI's own assumptions were wrong twice (invented a product tier, proposed removing the jackpot); the owner's frame won both times and the AI recomputed inside it.

### 12. Persist every correction permanently
- **A**: "Never make this UI mistake again" (after three rounds on 9-slice borders) — the lesson went into a permanent self-review checklist. UI-language preference (spell things out, no abbreviations) also memory-pinned.
- **D**: Banned words, rejected concepts, a marketing phrase the AI reused after rejection ("you used that again") — all stored as negative rules in memory + the single-source doc; re-proposing a rejected game idea is treated as a worst-case signal.
- **B**: Reusable discoveries (import pipeline, grip normalization formula, capture-side-effect fix) were written to memory the moment they were found.
- **C**: A disposition ledger accumulates fixed/acknowledged/intended so no question is ever asked twice; fixed items get regression-verified next scan.

### 13. Organize outputs by next owner; clean as you go
- **C**: "You wire, I animate" — artifacts physically split into AI-wiring folders vs owner's-external-tool folders, each with a README; mixing them made handoff impossible.
- **A**: Fixed asset contract per type (AI: source still, padding, keying, import, in-game wiring; owner: external animation, effect sheets) — violated several times before being pinned.
- **E**: Owner hands artifacts back by explicit path/ID ("I made this, wire it in") — the handoff is part of the workflow, so intake locations must be unambiguous.
- **B**: Inspection scaffolding (showcase grids, floating display rows) removed immediately upon approval, reusable meshes preserved in storage — workspace kept clean.

---

## Part 2 — Lifecycle flows in detail

### Flow 1: New game 0→1 (campaign A)

The counter-intuitive finding: the sprint did **not** start with the core loop. Order actually observed:

1. **Concept screening**: ~20 candidates → competitor research ("first find out if similar games exist") → red-ocean verdict → differentiate via genre-combination gap. Title fixed here too.
   ⚠ **Authority note (owner corrections, standing rules):** this screening is *information for* the owner's choice, never a genre recommendation engine. The concept starts from **what the owner wants to make** — desire is where fun comes from. Present each option's pros/cons (saturation, asset economics, live-ops burden) with open-minded breadth; do NOT rank genres or steer toward statistically "viral" ones. A director that always recommends the same safe genre is malfunctioning.
   And **never issue "impossible for a solo dev" verdicts.** The empirical counterexample is this doctrine's own source: the owner solo-built and solo-operates a live MMORPG — a genre every AI prior calls team-only. Had they listened to that prior, the game would not exist; front-loading impossibility is the single worst directional failure a director can make. Treat scale ambitions as decomposition problems ("what would it take, in what order, what does the party absorb") and surface risks as engineering line-items, not as gates.
2. **Art tech decision simultaneous with concept**: derived from "what won't break in AI generation" — e.g. *one still image + all movement in code (transforms), frame sprites for effects only*. This zeroes future rework at design time.
3. **Inventory before demolition**: survey existing assets; keep everything theme-agnostic (combat code, effect libs, server systems), replace only the theme layer.
4. **Production pipeline established and debugged** (most of day one): generation → background removal → keying/trim → engine import.
5. **MVP = reskin the working core loop**, then play-verify. Half a day.
6. **Hero character gets the rework budget** (4–5 approval loops) — everything else is economized; the hero look is judged by owner's eye.
7. **Shell screens ported** from a sibling project's proven pattern.
8. Mid-sprint: **theme pivot** (total reskin) — half a day *because the pipeline existed*. This is the payoff event for step 4.
9. **Meta layer mass build-out** (tokenize/pipeline the structure, port proven systems wholesale from sibling projects on owner's instruction).
10. **Core gameplay redesign** only now, to match the identity — followed by content mass production under the fixed division of labor.

Director takeaway: front-load *pipeline capital*, reuse everything theme-agnostic, spend taste-budget on the hero asset, and schedule the fun redesign mid-sprint when the identity is proven.

### Flow 2: Adding major content (campaigns C, B)

1. **Research fan-out**: 3–4 parallel research agents on distinct axes; owner adds axes mid-flight. Best outcome: discovering the design already exists in the source material ("map it 1:1, don't invent").
2. **System-mapping Q&A**: owner probes concept↔system fit point by point; AI answers each with grounding + implementation cost (P0–P2); scope decision: minimize core-code changes.
3. **Enumeration gate**: survey the pipeline that will be reused, inventory what's reusable, map every constant/gate the addition touches.
4. **Stage-0 tool migration**: port proven tools, generalize (strip hardcoding), verify every tool works, commit.
5. **Single-item pipeline pass** (against *actual use*, not the source's use — see doctrine 7's 104-image lesson).
6. **Mass production in owner-declared dependency order** ("characters first, biomes last"), serial background queue + monitor. Expect and budget for reroll loops: quality, plausibility, spec, perfectionism, naming — five distinct loop types observed in one campaign.
7. **Wiring**: replace-in-place, preserve references/GUIDs, zero new files where possible; outputs pre-split by next owner.
8. **Session-close documentation** every session; **hardening/QA phase** at the end once art stabilizes (guards, negative tests, ledger dispositions) — the observed handoff point from "building" to "guarding".

### Flow 3: Live-service expansion (campaign E)

1. **Design settled through multi-round owner negotiation** (direction reversals expected — plan for them).
2. **Enumeration gate first** — this is where live differs: index=ID schemes, count-rejection gates, out-of-array special cases. Slot-collision resolution is a *decision*, made before code.
3. **Backward-compatible insertion**: don't append into occupied ID space; isolate new content (separate shard); keep every count-gate satisfied across all client files.
4. **Backup discipline absolute**: dated `_Legacy_{date}/` for every replaced asset; idempotent batches; delete forbidden.
5. **Verification checklist before any deploy**: counts, import values, bundle format, log scans, value diffs.
6. **Deployment gate**: everything runs on editor/test server; the live push (scp) is *explicitly excluded from delegation* — "you do all of it yourself, but no scp" in one sentence. Live reflection happens only after a separate, explicit owner decision. Development sessions and deployment are separate events.

---

## Part 3 — Special patterns (1–2 campaigns only; apply when the context matches)

**Web live service with no local runtime (D)**
- "Done" *is* deployment: with no local preview, the loop is deploy → headless screenshot → fix. Completion reports must say "deployed and verified live", never "implemented".
- **Deterministic dual kernel**: game-judgment logic implemented twice (client TS ↔ server-side Python) and locked with hundreds of bit-identical cross fixtures. Every owner instruction is classified *kernel change* (edit both + re-verify fixtures) vs *render-only* (visuals, safe to iterate freely). This contract is what made an 8-round live-sculpting session safe.
- **Deploy contract check**: with N independent deploy tracks (server / web / game bundles), verify no track overwrites another's artifacts — an SPA fallback returning 200 masked exactly this failure for multiple deploys.
- **Session-cookie self-issuance**: to verify logged-in pages, mint a test session inside the server (secret never leaves) and hand it to the headless browser.
- **Aesthetic delegation line**: mechanical wiring → worker AI in parallel; taste/UX judgment ("nobody builds it like this") → orchestrator does it personally with the screenshot loop. When a worker's output is bad, pull the line back in.

**In-engine live building via MCP (B / Roblox)**
- Edit/Play mode guard: datamodel edits fail in Play mode — fix in Edit, test in Play; ask the owner to stop Play if needed.
- Screen capture locks the camera (Scriptable) and kills editor navigation — restore `CameraType=Custom` after every capture (recurred until wired in).
- Terrain fill rounds outward to the voxel grid — repeated patch-fills stack into stair-step patchwork; use grid-aligned targets and large overlapping blocks; thin roofs over voids read taller than terrain after smoothing.
- Generated meshes arrive with random orientation/roll/grip/scale — unify by programmatic measurement (thin-axis = blade), not by eye; mesh swaps sever the handle weld (restore or the item won't sit in the hand).
- Free marketplace models: name ≠ contents, missing meshes, scattered parts — robust bounding boxes (ignore outlier parts) + full visual capture review.
- Audience-calibrated naming: for a child audience, reject fantasy-dictionary terms for the simplest familiar progression (wood→stone→iron→gold→diamond tier metaphor).
- In-place triple source of truth (design doc + manifest + build log objects inside the workspace) synchronized with disk docs at session close; a build-log lock protocol before touching a collaborator's systems.

**Owner-absence protocol (B)**
- When the owner steps away: proceed on defaults, but only for easily reversible work; park destructive or taste-loaded decisions; flag everything done in absence with "say the word and I'll change it". (The 30-models-by-name incident is what happens when this is violated.)

**Content-risk filters (C)**
- Age-rating tone (no blood/skulls/horror at 12+), real-person name transformation, market-censorship avoidance, framing choices — wired as standing filters at both generation and review ends, with rating violations as a distinct review item.

**Server as single source of truth + negative tests (C hardening phase)**
- Client literals removed in favor of server-owned constants; contract gates (entry counts, config guards) verified by *deliberately breaking them* to prove detection works. A guard that has never fired is unproven.

**Instruction-vocabulary calibration (E, D)**
- The owner's terms may not match standard definitions ("16:9" = pad with margin, not re-compose). Reinterpret ambiguous instructions in the owner's established vocabulary; maintain a translation table (internal term → user-facing term) in memory.

**Crash/interruption self-recovery (D, E)**
- After a session crash the owner says only "continue" — recover the exact stopping point from tree/build state without asking "where were we". Know which background processes survive a session teardown and which monitoring/automation dies with it; state this in the handover.
