---
description: Judge the latest scan's findings one at a time (plain language + choices) and record them to the server-side ledger, so the next scan stops re-asking.
allowed-tools: Read, Grep, Glob, AskUserQuestion
---

# /fullparty:triage

Walk the owner through the latest scan's findings and promote judgments to the server ledger. Respond to the owner in their own language.

1. Take the confirmed findings from the latest scan (returned by `qa_scan`/`qa_report`, or fetch via the server tool).
2. For each, **one at a time**: explain in plain language (what code / where / when it breaks / impact), then ask via multiple choice (AskUserQuestion): the disposition — intended / real-not-fixed / real-fixed / real-do-not-touch / not-sure — plus "did you know before the scan?". When several findings share one pattern/root cause, offer a grouped disposition first ("these N are the same class — treat alike?") and fall back to per-finding only if the owner splits them.
3. Call the server MCP tool **`qa_triage`** with `project_id` + the dispositions. The server appends them to this project's ledger (the moat). A question answered once is never asked again.

No catalog or judgment data lives in this command — it only relays the owner's decisions to the server.
