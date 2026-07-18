---
description: Run a QA scan on the current project. Sends a diff/manifest summary to the server, which returns the relevant verification slice; runs the checks locally and reports.
argument-hint: 'optional: "diff" for recent changes only'
allowed-tools: Read, Grep, Glob, Bash, Write, Task
---

# /fullparty:scan

Run a catalog-based QA scan via the Fullparty server. Read-only on the target. Respond to the user in their own language.

1. Gather a **summary** of what to scan — never raw source, only a summary (§ privacy):
   - Full scan: a lightweight manifest (file tree + key structural facts from the profile).
   - Diff scan (arg `diff`, or "recent changes"): `git diff --name-only {range}` + the nature of the changes.
   - Load `${CLAUDE_PROJECT_DIR}/.fullparty/qa/project.json` for `project_id`.
2. Call the server MCP tool **`qa_scan`** with `project_id` + the summary. The server matches against its catalog, applies this project's ledger (suppression / known / regression), and returns **only the verification-instruction slice relevant to this diff/project**, plus how to run it (finder/verifier orchestration).
3. Execute the returned instructions **locally** against the project's code (read files locally, spawn finder/verifier subagents as the server specifies). Raw code stays on the machine.
4. Call **`qa_report`** with the **distilled** findings (pattern id, file:line, brief — not raw code). The server stores them in project memory and returns the report + loop metrics.
5. Show the report. Point the owner to `/fullparty:triage`.

All catalog patterns and judgment memory are server-side. This command carries no patterns — it only drives the local execution of server-supplied instructions.
