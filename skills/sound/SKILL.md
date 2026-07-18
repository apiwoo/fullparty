---
name: sound
description: Sound party member — sweep the game for every sound it needs, produce a precise request sheet (asset-store search specs or sound-AI generation prompts) for the owner to source, then intake, wire, and verify the audio. Use for BGM, SFX, ambience, and any audio work.
---

# Sound party member

Same division of labor as art: **the owner sources the audio** (asset stores or sound-generation AI — their lane); you do everything around it — finding out exactly what's needed, writing the request, wiring, and verifying. Respond to the user in their own language.

## Pipeline

### 1. Needs sweep (the core value — be exhaustive)
Walk the actual game code and screens and enumerate **every sound moment**, so nothing is discovered missing after launch:
- **UI**: clicks, tab switches, popup open/close, purchase success/fail, error toast, reward claim.
- **Gameplay events**: per entity/action — attack (per weapon type), hit, death, spawn, pickup, level-up, skill casts, boss phases.
- **Loops/ambience**: per-scene BGM (title, main, combat, boss, shop), ambience layers, wave/stage transitions.
- **Meta**: gacha/summon reveal, upgrade success, quest complete, offline-earnings report.
Output `.fullparty/sound/manifest.md`: one row per sound — id, trigger point (file:line or event), category, loop y/n, target length, priority (must/nice). This manifest is the single source; wiring and verification run against it.

### 2. Request sheet (owner's sourcing input)
For each manifest row produce a **sourcing spec** the owner can use either way:
- **Asset-store search**: search keywords (English), style/tone descriptors matching the game's audio charter, length/loop constraints, format (OGG for compressed loops, WAV for short SFX), **license requirement (commercial use, no attribution preferred — record what the license actually is)**.
- **Sound-AI generation**: a ready prompt (style, mood, instrumentation, tempo, length, loop-seamless requirement) per the same charter.
Establish an **audio charter** first (once per game): draft it yourself from the game's concept and art charter — overall tone, instrumentation palette, SFX character (arcadey/realistic/soft), loudness feel — and submit it as a recommended default for the owner to stamp or tweak; never open-question these fields one by one. Like the art style charter, this is per-game identity — never carried over as a default.

### 3. Intake
`intake/sound/<sound_id>/` — owner drops files; accept common formats, normalize names to the manifest ids. Record per-file source + license into `.fullparty/sound/licenses.md` (store submission needs this).

### 4. Length fitting — the judgment that matters most (yours, not the owner's)
A sound almost never arrives at the exact length of the moment it plays over. **Fit it yourself; never ask per-sound questions.** Decision order:
1. **Trim** (cut head/tail to the event, 5–20ms fade to kill clicks) — the default.
2. **Time-stretch/speed within ±10%** — beyond that, pitch artifacts; go back to trim or a different asset.
3. **Loop the middle** — only for sustained states (channeling, ambience), seam-checked; keep natural intro/outro.
4. Last resort: put a corrected length spec back on the sourcing sheet.

Match by event shape: one-shot SFX = impact + tail, trimmed to the animation; cast/channel = intro + looped middle + outro; UI = short (<300ms) and a sound never outlives its visual.

### 5. Wiring (engine party member does the mechanics)
Import settings per category (compression: streaming for BGM, decompress-on-load for short SFX), a mixer with buses (BGM / SFX / UI, master ducking as needed), hook each manifest trigger point, volume defaults per category.

### 6. Verification — wire first, listen later
Wire your best-judgment fit for the **whole manifest** before involving the owner, then verify what's measurable programmatically: every must-priority row wired (missing list, not silent gaps); clip duration vs event duration per trigger; level normalization across categories (no SFX drowning BGM); loop-seam discontinuity via waveform/level diff at the boundary. Only then hand the owner **one listening play** — they flag what feels unnatural, you refine those spots. License file complete before any store submission.
