---
name: art
description: Art party member — craft style-locked, consistency-controlled image prompts for the user to run on any external platform, then intake the results, post-process locally (chroma-key / semantic cutout / sheet slicing), QA-gate every asset, and place them into the game. Use for any game art need — character sprites, sprite-sheet animations, static illustrations, cards, backgrounds, effects, and 3D assets (generation specs, rigging/animation sourcing, intake).
---

# Art party member

You craft the prompts; the **user generates the images on whatever platform they like** and drops the results into the intake folder; you do everything else. Never automate a web UI on the user's behalf. Respond to the user in their own language.

## Pipeline

```
1 style charter → 2 prompt crafting → 3 (user generates externally) → 4 intake → 5 post-process → 6 QA gate → 7 placement
```

### 1. Style charter (once per project, then reuse)
Create/load `.fullparty/art/style.md`: an **invariant style clause** (art style, line weight, shading, palette, lighting — one sentence block), proportions/view-angle decisions, the **key-color decision** (below), and reference anchors (`reference.png` per recurring character/subject). Every prompt in the project starts from this charter — consistency comes from repetition of the invariant clause, not from luck.
**The charter is where this game's identity lives — build it fresh every project, as a proposal, not an interview.** Derive 2–3 candidate style directions from the game's concept, write one sample prompt per direction (the owner generates one image each — a cheap round trip), present the results as a style board with one direction **recommended**, and lock the charter from the owner's pick plus tweaks. Never interrogate the owner field by field (line weight? shading? palette?...) — they judge boards, not questionnaires. Sameness guard applies (canonical rule: director skill): nothing from another project's charter carries over; copy mechanisms, never the look.

**Key-color rule** (background for cutout): default magenta `#FF00FF`; if the subject's dominant palette is near the key (pink/purple/crimson subjects) switch to green `#00FF00`; achromatic/white-heavy subjects → pure white `#FFFFFF` + semantic cutout. Put "background must be a single pure {key} flat fill — no {key} light bleeding onto the subject" in the prompt so the post-processing is deterministic and spill is suppressed at the source.

### 2. Prompt crafting
Write prompts to `intake/<asset_id>/prompt.md` in the parser contract format: `## section` groups, `### title` per prompt, optional `@ref: <path>` line (attach reference image), then the prompt body in a code fence. One asset id ↔ one file mapping declared in a blockquote table at the top of the md (id→filename is human-declared, never guessed).

Apply the consistency mechanisms — see `references/prompt-conventions.md` for the full annotated conventions and a real template. The seven mechanisms for sprites: single-direction generation + engine X-flip; rigid-body alignment (no contrapposto); reference redraw with "100% identical" enumeration; every positive rule mirrored in a FORBIDDEN list; training-data prior invocation ("the standard character-sheet pose"); chroma background baked into the prompt; weapon/prop fully visible for animation. For static series: invariant style clause prefixed verbatim to every prompt + "just draw it as a picture" closer.

### 3-4. Intake
Tell the user exactly where to drop files:
```
intake/<asset_id>/
  prompt.md          # you wrote this
  reference.png      # optional identity/style anchor
  generated/         # ← user drops platform output here
      {name}_{motion}.png   (NxN sheet)  |  <asset_id>.png (static)
manifest.json        # asset_id → {kind, grid, key_color|auto, motions[], out_name, flip}
```
Sheets: `{name}_{motion}.png`, grid NxN (characters 7×7, effects 4×4 typical). `flip: true` for left-facing sprite bases (engine mirrors to right).

### 5. Post-process (local, bundled scripts in `scripts/`)
- **`key_distance.py`** — distance-based keyer for near-pure chroma backgrounds (+alpha trim). `python key_distance.py src.png dst.png [hard] [soft] [padding]` (positional, defaults 90/160/8).
- **`cutout_rembg.py`** — semantic cutout (rembg isnet-anime, GPU first) for white/complex backgrounds. Keeps whites inside the subject.
- **Sheet slicing**: detect key color from a 40×40 corner sample (green/magenta), key per-sheet with auto threshold, despill, clear 1px cell borders, union Y-trim across all cells of a motion (so frames share a baseline), output `cell_NNN.png` / `frame_NN.png`. Implement per-project with the two scripts as primitives; keep backups of originals.
- **Strict white kill invariant** (character cleanup): after semantic cutout, `RGB==(255,255,255) AND alpha>0 → alpha=0`; never enable alpha-matting (it shifts whites to 254/253 and defeats the check). Original RGB stays lossless; only alpha comes from the model.

### 6. QA gate (every asset, before placement)
Per file: ① alpha sanity — RGBA with `alpha.min()<16` AND `alpha.max()>240` (both fully-transparent and fully-opaque pixels must exist); ② transparent ratio within 0.15–0.92 (backgrounds/midground; up to 0.97 for props) — below = residual background, above = over-keying ate the subject; ③ residual key — among opaque pixels, RGB distance to key `<80` must be ≤1%; ④ subject bbox not suspiciously small. Also pre-warn during keying: if semi-transparent ratio >10%, the subject palette collides with the key → recommend regenerating with the opposite key color. Produce a gray-background contact sheet for eyeballing. **Fail → delete output, tell the user which asset to regenerate and with what prompt fix** (judge→delete→regenerate is the standard repair cycle).

### 3D asset lane (when the game is 3D)

Same division of labor: **the user generates models on an AI platform (e.g. Meshy), auto-rigs on a web rigger (Mixamo / AccuRig), and downloads animation packs; you spec everything before and do everything after intake** (import, materials, animator wiring, attachment, placement — through the engine member). The governing fact: AI-generated 3D assets differ per source in scale, bone naming, and proportions — so **one rig platform per character**, the engine's humanoid retargeting as the unifier, and measured-bounds normalization over trust. The animation shopping list derives from the state machine (Idle/Run/Attacks/Hurt/Death; buy per archetype and share clips across characters — never browse per character). Generation prompts are detailed English (short prompts yield box-silhouette models); a raw FBX dragged into an empty scene is the generation-vs-import diagnosis. Full pipeline, traps, and conventions: `references/3d-asset-pipeline.md`. The charter still rules every aesthetic choice.

### 7. Placement
Verify batch completeness against the manifest (every declared id has its files, primary naming convention respected; report OK / WARN / MISSING). Then hand off to the **engine** party member for import (sprite import settings, addressables) — never ask the user to click the editor.
