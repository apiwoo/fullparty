# Unity-uGUI programmatic framework — battle-tested implementation

The proven Unity implementation of the ui skill's framework principles. On Godot / UI Toolkit, port the *principles* (see SKILL.md), not these classes.

## Core classes (scaffold under `Scripts/UI/`)

- **`UIBase`** — abstract panel base: `Start() → fonts init → Build() → Hide()`, `Show/Hide/Toggle`, ESC-to-close, `BuildPopupFrame(name, sortOrder, w, h, title)` (canvas + dim + centered panel + close button) and `BuildFullscreenFrame()`. New panels subclass and implement `Build()` only.
- **`UILayout`** — canvas factory (`ScreenSpaceOverlay` + `CanvasScaler.ScaleWithScreenSize`, `GraphicRaycaster`), **SafeArea container** (aspect-fit; all content goes inside; Show/Hide via its `CanvasGroup`), layout containers `VBox / HBox / Grid` (never absolute coordinates), and widget factories: `CreateTitle/Subtitle/Body/Button/Bar/TabBar/Slot/Divider/ScrollView`. Design tokens: grid 8, padding 8–32, button height 50, fonts 12/14/16/20/24.
- **`UIFonts`** — font loader with OS-font fallback (never crash on missing font). Text always renders in the charter's chosen font; UI kit assets provide frames only.
- **`UIColors`** — single palette class every UI file references; **keep field names as semantic slots and change only values** when re-theming (250 call sites survive a theme swap).
- **`UISprites` + `UITheme`** — the design system: 3-layer sliced sprites (BG+Pattern+Border) with size grades `ApplyPanel(L)/ApplyButton(M)/ApplySlot(S)`, falling back to flat colors when no assets exist. **Every element must go through `Apply*`** — bare colored `Image`s produce the wireframe look. Assign grades for real: main/popup panels=L (with dim), buttons=M, rows/slots/bars=S.
- **`ScreenLetterbox`** — aspect enforcement + orientation lock + letterbox bars (set `TARGET_ASPECT` to the game's charter frame).
- **`UIFindGuard.FindOrWarn`** — name-based lookups log an error instead of silent NRE (catches prefab renames).

## Known engine traps to bake in

- Scroll viewports need a raycast-target `Image` (transparent GOs don't receive drag).
- Gauge fills on sprite-less `Image` must be anchor-based (`anchorMax.x = ratio`), not `type=Filled` (sprite-less `Filled` draws a full quad).
- Small buttons get an invisible ±20px HitArea child (`ApplyTouchPadding`).
- **`ContentSizeFitter` + nested `LayoutGroup` don't resolve on the frame you build them** — sizes read 0/stale, so padding and alignment look wrong on screen while the code is "correct". After building or mutating layout-driven children, call `LayoutRebuilder.ForceRebuildLayoutImmediate(rect)` innermost-out (or defer reads one frame); never trust a same-frame read of a layout-driven size. This is the #1 cause of "the numbers are right but the screen is wrong".

## Panel template (the one pattern to repeat)

```csharp
public class MyPanel : UIBase {
    Text title; RectTransform list;
    protected override void Build() {
        var panel = BuildPopupFrame("MyCanvas", sortOrder:200, width:660, height:900, title:"제목");
        var col = UILayout.VBox(panel, "Body", spacing:12);
        title = UILayout.CreateSubtitle(col, "부제");
        (_, list) = UILayout.CreateScrollView(col, "List");
        UILayout.CreateButton(col, "확인", OnConfirm);
    }
    public override void Show(){ base.Show(); GameEventBus.OnChanged += Refresh; Refresh(); }
    public override void Hide(){ base.Hide(); GameEventBus.OnChanged -= Refresh; }
    void Refresh(){ /* rebuild list children, update texts — redraw whole state, no diffing */ }
}
```

Update rules: event bus fires "changed", `Refresh()` redraws from current state (no diffing). In-flight server calls set a flag to block double-clicks. Disabled ≠ hidden: `CanvasGroup.alpha 0.45 + interactable=false`.
