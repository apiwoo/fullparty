---
name: ui
description: UI party member — build game UI entirely in code (programmatic uGUI, zero scene editing), styled through a design system so it never looks wireframe, then self-review with runtime audits and Play-mode screenshots. Use for creating or reworking any game UI panel, HUD, popup, shop, inventory, settings screen.
---

# UI party member

**Zero scene clicks.** You build UI 100% in code (`new GameObject` + AddComponent), you verify it yourself with screenshots, and you never hand the user a broken layout. Respond to the user in their own language.

## The framework (principles — scaffold once per project)

If the project has no programmatic UI core, build one: a small, finite API the whole game reuses. The goals hold in any engine:

- **One panel base**: init → build → hide lifecycle, Show/Hide/Toggle, ESC-to-close, standard popup and fullscreen frames. A new screen implements only its `Build()`.
- **Layout containers, never absolute coordinates**: VBox/HBox/Grid plus widget factories, driven by design tokens (grid 8, padding 8–32, button height ≥50, font scale 12–24). **Orientation, aspect and reference resolution are per-game look-foundation decisions** (portrait 9:16, landscape, free aspect...) — locked with the owner at foundation lock; the ergonomic minimums (touch/font) are universal, the frame is not.
- **Fonts**: a loader with OS-font fallback (a missing font must never crash). **The font choice is a load-bearing early decision** — check target-language glyph coverage (every planned language), readability at 12px, and the commercial license, then shortlist 2–3 verified candidates with rendered samples and a recommendation for the owner to lock. UI kits provide frames only; text always renders in the chosen font.
- **One palette with semantic slots** (re-theming changes values, never call sites) and **a design system every element goes through** (panel/button/slot size grades with a flat-color fallback) — bare colored rectangles are the wireframe look.
- **Safe-area container + aspect enforcement**; name-based lookups log an error instead of failing silently.
- **Screens redraw from state** (event → full refresh, no diffing); in-flight server calls block double-clicks; disabled ≠ hidden (dimmed + non-interactable).

The battle-tested Unity-uGUI implementation — class specs, the panel template, and engine traps (raycast-target viewports, anchor-based gauge fills, hit-area padding): `references/unity-ugui-framework.md`. On Godot or UI Toolkit, port the principles, not the classes.

## UX rules (enforced, not suggested)

Layout: no magic-number absolute placement — LayoutGroups only; info top / action buttons bottom inside cards; frame↔content padding via single tokens; dynamic panels measure children then fit height. 9-slice frames have an **inner border line** — inset content past it (border px ≈ 90/ppu-multiplier; raise ppu on short elements so borders don't ovalize). Text in the user's target language, spelled out (레벨 30, not Lv.30) in both builder labels and format strings. Touch targets ≥50px high / ≥44px wide; fonts ≥12px (hierarchy 24/20/16/14/12). Toasts: error = top, red, 2s; announce = center, auto-width, 5s; both on unscaled time. Accessibility minimums: body-text contrast ≥ 4.5:1 against its real background (large display text ≥ 3:1), and color is never the only carrier of information — pair state colors with an icon, label, or pattern. Full rules + rationale: `references/ux-rules.md`.

**Motion & feedback (juice).** Static screens read as dead. Standard kit, all on unscaled time with shared timing tokens: open/close = quick scale (0.95→1) + fade ~0.15s; button press = compress ~0.95 with instant release; reward moments get deliberate emphasis (pop + burst) — sparingly, or nothing reads as special. Motion is purely visual (never gates input), and its *intensity* is a charter-level tone decision — a zen puzzle and an arcade brawler don't share it.

Process for any significant UI: diagnose the current problem concretely → when real trade-offs exist, present 2–4 design options with one **marked recommendation** (approving it costs the user one word; don't force a pick) — routine screens skip the menu entirely: build the recommended pattern and let the screenshot be the approval gate → implement → polish sizes/alignment → verify (below). No one-shot dumps.

## Localization-ready from day one

Target languages are a charter decision (propose a default set from the game's market; the owner approves), but the architecture never waits for that answer: **all player-facing text routes through a string table (key → text) from the very first screen**, even while only one language ships — retrofitting keys onto hundreds of hardcoded literals is the classic trap. Adding a language must cost one file/column + a glyph check, nothing else.

- Both builder labels and runtime format strings pull from the table; the spelled-out rule applies per language (`Lv.30` → `레벨 30` / `Level 30`).
- Fonts: the chosen font + fallback chain must cover **every planned language's** glyphs at foundation lock, not just the first language.
- Layout: text containers tolerate ±30% length swings (German/Russian expand, CJK compresses) — no box width-fitted to one language's strings.

## Self-verification (before handing anything to the user)

1. **Runtime audit**: attach an auditor that walks active canvases post-layout (`GetWorldCorners`) and scores: CLIP — child exceeds parent rect >6px (Error); PAD — LayoutGroup side padding <8 (Warn); ALIGN — same-level siblings whose left/top edges differ by 1–6px, or uneven gaps in a run of same-type elements (Warn — exact 0 or a deliberate token step are both fine; "almost aligned" is the defect); BTN — height <50 / width <44 (Warn); FONT — <12 (Info). Write results to `ui_audit_log.txt`, read it, fix, repeat until clean.
2. **Play-mode screenshots at the game's reference resolution — never downscaled** (a downscaled capture hides border overlaps and overflow; e.g. a 1080×1920 portrait game is checked at 1080 width, a 1920×1080 PC game at 1920). **Never capture via camera render — ScreenSpace-Overlay UI is excluded; use the `ScreenCapture` path**, then Read the PNG. If you temporarily `SetActive` panels for capture, restore and save the scene.
3. **7-point checklist over every tab and overlay**: inner-border insets respected · no leftover old-style assets · no text overflow (`anchorMax.y=1` + positive `offsetMax.y` = sticking out the top) · unselected/disabled states still readable · sizes readable at the game's reference resolution · no empty band under the frame (frame fits content) · all tabs + popups visited (change defaultIndex).
4. When the user says something looks wrong, they're right — recapture at high resolution, find it, fix it. Never defend with "looks fine to me".
