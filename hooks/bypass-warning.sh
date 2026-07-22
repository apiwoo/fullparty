#!/usr/bin/env bash
# SessionStart hook: when the session runs permissions-bypassed, show the user a
# one-line banner and hand the model its caution doctrine (AGENTS.md setup step 4).
input=$(cat)
case "$input" in
  *'"permission_mode":"bypassPermissions"'* | *'"permission_mode": "bypassPermissions"'*)
    cat <<'EOF'
{"systemMessage":"⚠ Fullparty: bypass-permissions session — the party edits files and runs commands without asking. Keep this mode scoped to trusted game projects with an off-site backup.","hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"This session runs with permissions bypassed (Fullparty full-auto default). Doctrine: mention the mode in one line at session start, and announce irreversible operations (deletes, live pushes, mass regeneration) in one line before running them."}}
EOF
    ;;
esac
exit 0
