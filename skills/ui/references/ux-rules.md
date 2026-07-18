# UX rules — full set with rationale

## Layout / padding
- **Absolute-coordinate manual placement is banned.** It's the root cause of recurring overlap defects (short cards, grown content). Dense grids (slots/codex/roster) = `GridLayoutGroup`; evenly-split rows = `HorizontalLayoutGroup`; cell children use cell-normalized anchors.
- Card interiors: information (name/grade/stats) on top, action buttons at the bottom — never share a y-band. Don't cram short cards.
- Frame↔content padding flows through single tokens (e.g. `PANEL_BORDER 90 / PANEL_PAD 94 / HEADER_CLEAR 104`). Static tabs: fit the frame to content height. Dynamic tabs: measure children at runtime, then set height.
- **Sibling alignment is exact or deliberate — never approximate.** Same-level elements share edges precisely (left edges of stacked sections, tops of a row); a 1–6px drift reads as sloppiness even when nobody can name it. Runs of same-type elements (list rows, stat lines, buttons) use **one** spacing token — mixed gaps in a run are a defect, different tokens between different levels are hierarchy.
- **Pivot matches the anchoring intent.** Centered element = pivot (0.5, 0.5); top-stretched bar = (0.5, 1); bottom button = (0.5, 0). A mismatched pivot produces the "why is this 3px off-center" class of drift that no padding fix cures — check pivot before touching offsets.

## 9-slice borders
- Frame-style 9-slices have an outer edge **and an inner line**; content must sit inside the inner line.
- Border render width ≈ `spriteBorder / (pixelsPerUnit/100) / ppuMultiplier` UI px (ppu1≈90px, ppu3.4≈26, ppu5≈18). Give content that much inset, or raise ppu to thin the border.
- Short elements (rows/chips/buttons) need higher ppu (≈3.4/4.5/2.2) or the border corners ovalize. Top-anchored icons and bottom bars are the usual victims.

## Text language
- All UI strings in the user's target language, spelled out — no abbreviations from dev jargon: `Lv.30→레벨 30`, `XP→경험치`, `HP→체력`, `ATK→공격력`; units too (`/분`, `골드`, `초`, `개`). Replace in **both** builder label strings and runtime format strings. Proper nouns/brands exempt.
- All player-facing strings route through a string table (key → text) from the first screen — hardcoded literals are banned even while only one language ships. Adding a language = one file/column + a glyph-coverage check, never a codebase sweep; containers tolerate ±30% length swings across languages.

## Safe area / resolution (per-game decision — example values from a portrait game)
- **Orientation + reference resolution are locked per game at look-foundation time**, not inherited defaults. A mobile-portrait game: reference **1080×1920, 9:16**, `ScaleWithScreenSize`, `matchWidthOrHeight 0`. A landscape/PC game sets its own frame (e.g. 1920×1080, free aspect) — do not letterbox it to portrait.
- Whatever the chosen aspect: enforce it consistently — 3D via `Camera.rect`, overlay UI via a SafeArea container + bars (sort 32000) covering outside. Orientation lock in builds only (`#if !UNITY_EDITOR`).
- Self-review screenshots are taken at the game's own reference resolution (the "1080-width" rule elsewhere = that portrait game's real resolution; the principle is *real resolution, never downscaled*).

## Touch / typing / fonts
- Touch: buttons ≥50px high, ≥44px wide (square icon buttons 40 OK); expand small buttons with an invisible HitArea child (±20px).
- Fonts ≥12px. Hierarchy: title 24 / subtitle 20 / body 16 / sub 14 / small 12.
- IME guard: IME on only while an InputField is focused, forced off otherwise (Korean IME otherwise swallows WASD as composition keys); block game input while typing.

## Accessibility minimums
- Body-text contrast ≥ 4.5:1 against its **real** background (the 9-slice art, not the palette swatch); large display text ≥ 3:1. Check the worst tab, not the prettiest.
- Color never carries information alone: rarity/state/team colors are paired with an icon, label, or pattern (colorblind players lose pure hue coding).
- Disabled states must still pass readability (the `alpha 0.45` dim is a floor, not a free pass — verify on dark frames).

## Toast policy
- Error toast: top (anchor ~0.9–0.95), red text, 2s display + 0.5s fade, `sortingOrder 999`.
- Announce toast: center, `ContentSizeFitter` auto-width, 5s, optional `[공지]` prefix.
- Fades run on `WaitForSecondsRealtime` / `unscaledDeltaTime` (work at timescale 0).

## Design system discipline
- Flat colored `Image`s only → wireframe look. Run every element through the 3-layer slice design system (`ApplyPanel/ApplyButton/ApplySlot...`).
- Actually assign L/M/S grades: main/popup panel = L (with dim), button = M, row/slot/full-width bar = S. All-S = wireframe again.
- Sprite-less `Image` ignores `type=Filled` (draws a full quad) — gauge fills must be anchor-based (`anchorMax.x = ratio`).

## Re-theming trick
- Keep palette **field names** as semantic slots (e.g. `Cyan` = "accent") and swap only values when changing theme — call sites stay untouched.

## Process
1. Diagnose the current UI's problems concretely (info overload, duplicated grids, grade scatter...).
2. When real trade-offs exist, present 2–4 design options (A/B/C/D) with trade-offs and a **marked recommendation** — the user picks another or just approves yours. Routine screens: build the recommended pattern directly; the screenshot is the approval gate. Don't hide alternatives, but don't force a choice either.
3. Implement, then polish sizes/readability/alignment repeatedly (incl. 9-slice insets).
4. Verify with the runtime audit + Play screenshots at the game's reference resolution + the 7-point checklist, across **all** tabs and overlays. Demo with the previously-worst case, not the prettiest tab.
