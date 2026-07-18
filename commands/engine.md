---
description: Engine party member — drive Unity/Godot headlessly (compile gates, builds, imports, editor-script generation, wiring verification, screenshot loops). The user never clicks the editor.
allowed-tools: Read, Grep, Glob, Bash, PowerShell, Write, Edit, Task
---

# /fullparty:engine

Engage the **engine** skill (see `skills/engine/SKILL.md`). Respond in the user's language.

- Pin the editor version from `ProjectVersion.txt`; close the interactive editor before batch runs.
- "Need to see the screen?" no → batch mode, yes → MCP with the editor open.
- Never trust exit codes alone: compile gate = exit 0 AND zero `error CS` in the log; builds pass the mtime freshness double-gate.
- Prefer writing editor scripts (prefab builders, scene bakers, wiring verifiers) over any manual editor operation.
