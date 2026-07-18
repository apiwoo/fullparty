# 3D asset pipeline — auto-rig era knowledge (from a live 3D MMORPG campaign)

Division of labor is the same as 2D: **the user generates models on an AI platform (e.g. Meshy), auto-rigs on a web rigger (Mixamo / AccuRig), and downloads animation packs (Mixamo / ActorCore)** — their lane. You write every spec before that and do everything after intake: import, materials, animator wiring, attachment, placement (through the engine member).

## 0. The one root cause

**AI-generated 3D assets differ per source in scale, unit, bone naming, and proportions.** Every trap below derives from this single fact. Two standing defenses: (a) filename/folder conventions drive automated import settings — the name IS the contract; (b) measure, don't trust — renderer bounds, bone lists, and validation logs over assumptions.

## 1. Generation (user's lane; you write the specs)

- **Detailed English prompts only.** Short/vague prompts produce box-silhouette models — vertex count means nothing (5,000 verts of surface noise on a box is still a box). Spec template: subject detail + "highly detailed, game-ready, clean quad topology, PBR textures".
- **Diagnosis rule**: drag the raw FBX into an empty scene. Box there = generation problem, not an import problem — regenerate; don't debug the importer. One Refine/Remesh (quad) pass after generation; image-to-3D (2D concept → 3D) for hero-quality pieces.
- **PBR texture suffix contract**: `_texture` (albedo) / `_normal` / `_metallic` / `_roughness` — import automation keys texture types (sRGB, normal-map flag) off these names; a violated name renders wrong.
- **Static props have no bones.** Never treat a generated prop as a character; they get transform-based procedural motion or none.

## 2. Rigging & animation sourcing (user's lane; you define the shopping list)

- **One rig platform per character.** Auto-riggers and animation stores use different skeletons — bone counts, finger chains, naming (`mixamorig:*` vs `CC_Base_*`; one auto-rigger shipped 89 bones with 3-finger hands vs the animation store's 101-bone full hand). Mixing them raw = retarget errors ("bone length mismatch", corrupted poses).
- **The engine's humanoid retargeting is the unifier** (Unity: import everything as Humanoid) — muscle-space retargeting absorbs cross-platform bone differences that direct bone mapping cannot:
  - Character mesh FBX = the avatar source (CreateFromThisModel).
  - Animation FBXs from a *different* skeleton family → give each its **own self-avatar** (CreateFromThisModel); retargeting happens at runtime through the humanoid layer.
  - `CopyFromOther` **only** when animation and avatar share the exact same skeleton — cross-skeleton CopyFromOther corrupts poses.
- **The shopping list comes from the state machine**, not from browsing: `Idle · Run · Attack1–3 · Hurt · Death` is the minimal combat set (monsters get a smaller set). **Buy per archetype, share across characters** — one greatsword attack clip serves every greatsword user via shared animator wiring; magic casts unify across all casters.
- Small retarget warnings (~mm bone-length offsets) are cosmetic if playback looks right at gameplay camera distance. **Purge dead rig files to `_Legacy/`** — stale skeletons from an abandoned rigging platform keep generating warnings and get "fixed" by mistake.

## 3. Import (yours, via the engine member)

- **Scale**: embedded unit scales differ per platform (cm/mm; one platform bakes a 0.01 factor). Proven Unity combo for baked-scale sources: `globalScale=1, useFileScale=false`. Better: auto-detect from measured bounds and normalize — never hardcode per-model scale guesses.
- **Axis**: Z-up sources get `bakeAxisConversion=true` at import. Never fix orientation with runtime −90° rotations — it interacts with scale inheritance and squashes models flat.
- **Materials**: import with materials off; code-generate URP materials from the suffix texture set (`_BaseMap` **and** `_MainTex` dual-set, normal-map keyword enabled). Texture meta trap: a model texture imported as Sprite type breaks on meshes — Default type, wrap Repeat, mipmaps on.
- **Animation import**: skip T-pose/rest takes (pick the longest take in the file), set loop per motion, **lock root XZ on run clips** (or characters slide forward), and log `avatar isValid / isHuman` + curve counts after import — that log is the gate, not the absence of errors.
- **Stylized proportions fight the humanoid muscle model** (chibi/anime bodies): tune the human description in a second import pass — limit leg spread (~70%), drop unused upper-chest mappings, translation DoF off — while preserving the generated T-pose.

## 4. Attachment (weapons/props to bones)

- **Defensive bone search, always**: exact name → case-insensitive partial → common-name fallback array (`R_Hand`, `RightHand`, `Right_Hand`, `hand_r`, `Hand_R`) → dump the full bone hierarchy on failure. Auto-rig bone names are not standardized; assume nothing.
- **Scale by measurement**: normalize the item's mesh-bounds max dimension to a target (~1 m for weapons), correcting only outside sane thresholds (0.1–5 m), then apply the per-item multiplier. The generation platform's export scale is never trustable.
- **Rotation**: compose axis-independent quaternions (`AngleAxis` per axis, Y·Z·X) — `Quaternion.Euler` gimbal-locks at ±90° and weapon orientations live exactly there.
- **Sheathe/draw** = reparenting between hand bone and sheath bone (back = spine bone, hip = hips bone), **re-applying localScale after every SetParent** — world-scale preservation corrupts auto-scaled items.
- **Attachment failures are silent** (the item simply isn't visible): log renderer count / mesh verts / world bounds / material per attach. Numbers are tuned by eye, not blind: live-edit in the inspector during Play, then export the values back into the setup code (value-copy workflow).

## 5. Scale breaks at five layers — know which one you're in

import scale · **animation scale tracks** (Generic rigs: lock localScale per frame — but never on Humanoid, it kills hip motion; Humanoid gets runtime muscle scaling instead) · muscle proportions · runtime multipliers (elite/boss sizing) · **culling bounds** (scaled skinned meshes vanish at screen edges → expand localBounds / updateWhenOffscreen).

## 6. Procedural placement (props/structures)

- Placement rules live in **data assets per prop type**: footprint auto-measured from renderer bounds, category inferred from folder + size (tile / small prop / large prop / medium structure / hero structure / functional), spacing/area/door-clearance fields with per-category default presets.
- Passes run **big-first** (hero structures → medium → large props → small → functional); organic scatter = Poisson-disk sampling + cluster seeding, structured items = grid-jitter. Random yaw is a per-prop-type judgment, never a global default.
- **A validator with coded rule names** (overlap, allowed-area, door clearance, front visibility) runs after placement, dumps a JSON report per map+seed, and retries with a new seed on failure. Seed-based generation makes every layout reproducible and reviewable.

## 7. URP rendering

Shader/material traps (magenta causes ranked, build stripping, `_BaseMap` vs `_MainTex`, BiRP particle mapping, alpha-preserving tints): **engine skill → "URP & rendering traps"**.
