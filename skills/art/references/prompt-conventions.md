# Prompt conventions — consistency mechanisms (annotated)

> **⚠ Sameness guard — read first** (canonical rule: director skill). The *mechanisms* below are universal; the *aesthetic values* in the examples (chibi, 3-head proportions, left three-quarter view, neo-noir style...) are **one game's style-charter choices, not defaults** — every aesthetic slot must come from THIS project's charter. Copy the mechanism, never the look.

Two families. Both use the same md parser contract: `## section` / `### title` / optional `@ref:` / code-fenced body (>20 chars). Selection syntax `all | 1,3,5 | 2-6`.

## A. Animated sprite sheets (character/monster)

Example instantiation (from one real game — **every bracketed/aesthetic value is a per-game charter variable**; only the ★-clause *structure* and FORBIDDEN mirroring are the reusable part):

```
Redraw the attached [CHAR] character as a [3]-head-tall chibi sprite in the CLASSIC THREE-QUARTER DESIGN POSE (this is the STANDARD character-sheet angle used in 99% of illustration references — AI training data is overwhelmingly this pose).

★ VIEW — THREE-QUARTER VIEW FACING SCREEN-LEFT (WEST): both eyes visible. NOT pure 90° side profile. NOT full front. NOT back view.
★ BODY ALIGNMENT (CRITICAL — no contrapposto): the ENTIRE body (head + neck + shoulders + chest + hips + feet) rotates as ONE rigid unit. Head is NOT turned independently. NO over-the-shoulder look.
★ GAZE: toward SCREEN-LEFT. NO eye contact with camera.
★ CAMERA: eye-level, 0° tilt.
★ PROPORTIONS: [3]-head-tall (head:body = 1:2).
★ POSE: [idle standing / attack / hit ...]. Foreground foot slightly ahead.
★ WEAPON PLACEMENT (CRITICAL — whole weapon VISIBLE for animation): the ENTIRE [weapon] fully visible, nothing hidden behind the body. Hilt top no higher than the top of the head.
★ BACKGROUND: pure solid [GREEN #00FF00], flat fill (for clean chroma-key cutout). NO gradient, NO shadow, NO floor, NO environment, NO effects, NO text.
★ OUTPUT: 1:1 square 1024x1024. Character occupies ~85% of vertical frame, centered.
★ REFERENCE FIDELITY: keep the reference's face, hair style/color, eye color, skin tone, outfit, outfit colors, [weapon] design 100% identical.
★ POST-PROCESSING NOTE: this LEFT-facing sprite will be X-axis flipped in the game engine to produce the RIGHT-facing version. Generate the LEFT-facing base only.

FORBIDDEN:
- Facing screen-right / pure side profile / full front / back view / multi-view / turnaround
- Contrapposto, head-twist, over-the-shoulder look
- Eye contact with camera, centered pupils
- High angle, bird's-eye, looking down
- Colored/gradient background, environment, ground, shadow, effects
- [5]-head-tall, realistic adult proportions
```

Why it works (the seven mechanisms — teach these, not just the template):
1. **Single direction + engine flip.** Models draw the left three-quarter "character-sheet pose" reliably and drift to full profile on the right — so generate LEFT only and mirror in-engine. Removes an entire axis of variation.
2. **Rigid-unit alignment.** Head+torso+hips rotating as one block kills inter-frame drift (independently turned heads are the #1 consistency killer across motions).
3. **Reference redraw + "100% identical" enumeration.** Same `@ref` image attached to every motion; identity features enumerated item by item.
4. **Assert + forbid double writing.** Every ★ rule mirrored in FORBIDDEN — instructions land twice.
5. **Prior invocation.** "99% of references are this pose" pushes the model into its highest-confidence mode.
6. **Chroma baked into the prompt.** Pure flat key + no shadow/effects makes downstream keying deterministic — the prompt designs the post-processing.
7. **Animation-safe prop placement.** Fully visible weapon/prop so nothing is amputated when frames are cut.

## B. Static series (cards, portraits, biome layers)

Real-shape example (Korean original; any language works — repetition is what matters):

```
### 02_[member]

세련된 네오누아르 그래픽노블 카툰 스타일로, [PROJECT] 조직의 "[role]" 캐릭터 한 명을 상반신 정면으로 그려줘.
[subject-specific description ...] 굵은 검은 외곽선, 평면 셀셰이딩, 딥 네이비·차콜 의상에 틸 포인트,
한쪽에서 들어오는 강한 림라이트. 상반신, 정면, 화면 정중앙, 그림자 없음, 순수한 흰색 배경(#FFFFFF), 글자 없음. 그냥 그림으로 그려줘.
```

- **Invariant style clause + variable subject**: the style sentence (style, outline, shading, palette, lighting, background, "no text") is prefixed **verbatim** to every prompt in the series. Only the subject part varies.
- **Charter blockquote at the top of the md**: one style line + the id→filename mapping table (e.g. order ↔ code id ↔ `card_N.png`). Humans own this mapping; scripts trust it.
- **Closer "그냥 그림으로 그려줘" / "just draw it as a picture"**: stops chat UIs from answering with code/SVG.
- **Layered scenes (biomes)**: template-engine approach — 6 templates (backdrop/floor/midground/prop/seam) share one `{style}` token per theme; one md per theme so the user can generate a whole theme in a single chat session (session continuity itself aids consistency). A theme table (style, palette, props) + key-color-per-theme function regenerates all mds deterministically.

## Key-color selection table

| Subject dominant palette | Key |
|---|---|
| default | magenta `#FF00FF` |
| pink / purple / crimson / void-dark subjects | green `#00FF00` |
| achromatic, white-heavy | white `#FFFFFF` + semantic cutout (rembg) |

Always add: "background must be a single pure {key} flat fill — no {key} light on the subject."
