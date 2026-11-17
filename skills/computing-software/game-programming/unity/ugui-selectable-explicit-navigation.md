---
id: computing-software.game-programming.unity.ugui-selectable-explicit-navigation
name: ugui-selectable-explicit-navigation
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-ui, selectable-navigation, gamepad-ui, focus-navigation-unity, game-programming]
level: practitioner
status: draft
description: "Make uGUI menus gamepad-navigable: Selectable navigation modes, explicit links, first-selected handling, regaining focus after mouse use, and visualising nav."
sources: ["https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/script-SelectableNavigation.html", "https://docs.unity3d.com/Packages/com.unity.ugui@2.0/api/UnityEngine.EventSystems.EventSystem.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# uGUI gamepad navigation with Selectables

**Goal:** every menu is fully usable with a gamepad/keyboard, focus never gets lost.

## Navigation modes (on each Selectable: Button, Toggle, Slider...)
- **Automatic**: picks nearest selectable in each direction by position. Fine for simple grids;
  breaks with irregular layouts or scroll views.
- **Horizontal / Vertical**: restrict to one axis (sliders: Horizontal would fight value change, so
  put sliders in Vertical-only lists).
- **Explicit**: set Up/Down/Left/Right targets manually — use for anything non-trivial.
- **None**: not reachable by navigation.
The **Visualize** button in the inspector draws arrows for every selectable in the scene.

## Focus management
```csharp
void OnEnable() {                         // when a panel opens
    EventSystem.current.SetSelectedGameObject(null);   // force OnSelect to fire
    EventSystem.current.SetSelectedGameObject(firstButton.gameObject);
}
```
- EventSystem "First Selected" only applies at startup.
- After a mouse click on empty space, selection becomes null; gamepad input then does nothing. Fix:
  in Update, if `currentSelectedGameObject == null` and a navigation input arrives, reselect the last
  remembered selection (store it in `OnSelect` via `ISelectHandler`).
- When closing a sub-menu, restore selection to the button that opened it.

## Building explicit nav in code (dynamic lists)
```csharp
for (int i = 0; i < buttons.Count; i++) {
    var nav = new Navigation { mode = Navigation.Mode.Explicit };
    nav.selectOnUp = buttons[(i - 1 + buttons.Count) % buttons.Count];
    nav.selectOnDown = buttons[(i + 1) % buttons.Count];
    buttons[i].navigation = nav;
}
```

## Scroll views
Selection does not scroll the view automatically: on select, compute the item's position and adjust
`ScrollRect.normalizedPosition` (or `content.anchoredPosition`) to keep it visible.

## Gotchas
- With the Input System, use `InputSystemUIInputModule` (not StandaloneInputModule) and bind Navigate/
  Submit/Cancel actions.
- Disabled (non-interactable) selectables are skipped automatically; hidden but active ones are not.
- Popups must block navigation to elements behind them (set those to None or disable their
  CanvasGroup interactable).

## Verify
- [ ] Unplug mouse: every screen reachable and escapable with gamepad.
- [ ] Click empty space, then press d-pad: focus returns.
