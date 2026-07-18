---
description: Onboard the current game project into Fullparty's QA guard (profile + open the server-side judgment ledger). Run once per new project.
allowed-tools: Read, Grep, Glob, Bash, Write
---

# /fullparty:init

Onboard the current project with the Fullparty server. Respond to the user in their own language.

1. Lightly detect the project profile locally (a few files, not exhaustive): engine (Unity / web / Godot), genre, whether there's a server stack / DB. Ask the owner for the **code generator** (e.g. `claude-sonnet-4`, `manual`, `claude designs + codex implements`) — this is irreversible day-one metadata.
2. Call the server MCP tool **`qa_init`** with that metadata (engine, genre, server-stack flags, generator_model). Send metadata only — never raw source.
3. Save the returned `project_id` to `${CLAUDE_PROJECT_DIR}/.fullparty/qa/project.json` (just the id; no secrets) — the same `.fullparty/` state directory the party skills use.

The catalog, matching, and ledger all live server-side. This command only detects local metadata and registers it. Next: `/fullparty:scan`.
