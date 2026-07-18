---
description: UI party member — build game UI entirely in code (no scene editing), design-system styled, self-verified with runtime audits and Play screenshots.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, AskUserQuestion, Task
---

# /fullparty:ui

Engage the **ui** skill (see `skills/ui/SKILL.md`). Respond in the user's language.

- If the project lacks the programmatic UI core, scaffold it first (principles in the skill; Unity-uGUI class specs in `references/unity-ugui-framework.md`).
- For significant UI with real trade-offs: present 2–4 options with a marked recommendation; routine screens build the recommended pattern — the screenshot is the approval gate.
- Build panels from the one template pattern; run every element through the design system (no wireframe look).
- Before handing over: runtime audit clean + Play screenshots at the game's reference resolution (ScreenCapture path) + 7-point checklist across all tabs/overlays.
