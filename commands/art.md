---
description: Art party member — craft consistency-locked image prompts, intake externally generated images, post-process (chroma-key/cutout/slicing), QA-gate, and place into the game.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, AskUserQuestion
---

# /fullparty:art

Engage the **art** skill (see `skills/art/SKILL.md`) and follow its pipeline. Respond in the user's language.

- New project → establish the style charter first (style clause, key color, reference anchors) with the user's taste choices.
- The user generates images on their own platform of choice — you only hand them prompts and the intake folder path, then take over from the dropped files.
- Every produced asset passes the QA gate before placement; failures come back to the user as "regenerate this one, with this prompt fix".
- Placement/import is handed to `/fullparty:engine` — never ask the user to click the editor.
- 3D games use the same division of labor (user: model generation + auto-rig + animation packs; you: specs, import, wiring) — see the skill's 3D asset lane and `references/3d-asset-pipeline.md`.
