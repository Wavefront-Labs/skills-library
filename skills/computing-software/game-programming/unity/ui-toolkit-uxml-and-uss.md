---
id: computing-software.game-programming.unity.ui-toolkit-uxml-and-uss
name: ui-toolkit-uxml-and-uss
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-ui, ui-toolkit, uxml, uss, uidocument, ui-builder, data-binding, game-programming]
level: practitioner
status: draft
description: "Build runtime UI with UI Toolkit: UIDocument and Panel Settings, UXML structure, USS selectors and variables, querying and events, runtime data binding, uGUI trade-offs."
sources: ["https://docs.unity3d.com/Manual/UIElements.html", "https://docs.unity3d.com/Manual/UIE-USS.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UI Toolkit with UXML and USS

**Goal:** menus and HUDs built like web UI (structure in UXML, style in USS, logic in C#).

## Setup
- GameObject with **UIDocument** referencing a UXML (VisualTreeAsset) and **Panel Settings**
  (scale mode, reference resolution, theme style sheet, sort order). Several UIDocuments can share one panel.
- Author in **UI Builder** (Window > UI Toolkit > UI Builder); it writes UXML/USS.

```xml
<!-- MainMenu.uxml -->
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <Style src="Menu.uss" />
  <ui:VisualElement name="root" class="menu">
    <ui:Label text="My Game" class="title" />
    <ui:Button name="play" text="Play" class="menu-button" />
    <ui:Slider name="volume" low-value="0" high-value="1" label="Volume" />
  </ui:VisualElement>
</ui:UXML>
```
```css
/* Menu.uss */
:root { --accent: rgb(255, 180, 0); }
.menu { flex-grow: 1; align-items: center; justify-content: center; }
.menu-button { width: 240px; margin: 4px; transition-duration: 0.1s; }
.menu-button:hover { scale: 1.05 1.05; border-color: var(--accent); }
```
Layout is **Flexbox** (Yoga): `flex-direction` defaults to column.

## Code
```csharp
void OnEnable() {
    var root = GetComponent<UIDocument>().rootVisualElement;   // rebuilt on enable: query here
    root.Q<Button>("play").clicked += StartGame;
    root.Q<Slider>("volume").RegisterValueChangedCallback(e => audioMixer.SetFloat("Vol", Mathf.Log10(Mathf.Max(e.newValue, 0.0001f)) * 20));
}
```
- `Q<T>(name, className)` finds one; `Query<T>().ForEach(...)` many. Cache results.
- Events bubble: `RegisterCallback<PointerDownEvent>(...)`, `ClickEvent`, `NavigationSubmitEvent`.
- Toggle visibility with `style.display = DisplayStyle.None` (removes from layout) or
  `AddToClassList("hidden")`.
- Runtime data binding (Unity 6): set `dataSource` to an object and bind with `SetBinding` or
  `data-source-path` attributes in UXML; mark properties `[CreateProperty]`.
- Lists: `ListView` with `makeItem` / `bindItem` virtualises rows.

## UI Toolkit vs uGUI (Unity 6)
UI Toolkit: screen-space menus, data-heavy screens, editor tools. uGUI still needed for world-space
UI in older versions, custom shaders on UI, and some animation-driven UI. Mixing both is fine.

## Gotchas
- USS is a subset of CSS: no `display: grid`, limited selectors, `scale`/`translate` transitions only on supported properties.
- Gamepad navigation needs focusable elements and an EventSystem with the Input System UI module.
- Hot reload: changing UXML at runtime rebuilds the tree and drops your callbacks; re-register in OnEnable.

## Verify
- [ ] Layout holds at 16:9, 21:9 and 4:3 (Panel Settings scale mode checked).
- [ ] Menu fully operable with gamepad.
