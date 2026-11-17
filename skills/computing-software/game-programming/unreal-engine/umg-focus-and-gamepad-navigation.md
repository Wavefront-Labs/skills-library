---
id: computing-software.game-programming.unreal-engine.umg-focus-and-gamepad-navigation
name: umg-focus-and-gamepad-navigation
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, umg, umg-navigation, widget-focus, navigation-rules, game-programming]
level: practitioner
status: draft
description: "Make Unreal UMG menus gamepad-friendly: focusable widgets, SetUserFocus, navigation rules (explicit/wrap/custom), focus loss recovery and the Widget Reflector."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/widget-navigation-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/widget-reflector-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UMG focus and gamepad navigation

**Goal:** every menu works with a gamepad; focus is always somewhere sensible.

## Focus basics
- Only focusable widgets (Buttons, or UserWidgets with **Is Focusable**) receive keyboard/gamepad focus.
- Set focus when a screen opens:
```cpp
void UMainMenu::NativeConstruct() { Super::NativeConstruct(); PlayButton->SetFocus(); }
// multiplayer-safe: PlayButton->SetUserFocus(GetOwningPlayer());
```
- `NativeOnFocusReceived` / `NativeOnAddedToFocusPath` for highlight effects; Buttons' Hovered style
  doesn't apply to focus by default — style focus explicitly (or use CommonUI buttons).

## Navigation rules (Details > Navigation per widget)
- **Escape** (default): leave this widget in that direction, engine picks next by geometry.
- **Explicit**: go to a named widget.
- **Wrap**: wrap within the parent.
- **Stop**: block.
- **Custom** / **CustomBoundary**: Blueprint function returns the target widget.
Set on containers to apply to children. Project Settings > User Interface > Render Focus Rule controls
the dashed focus outline (Never in shipping, NavigationOnly during development).

## Focus loss
Mouse clicks on non-focusable areas set focus to the viewport; gamepad then does nothing. Recovery:
- override `NativeOnFocusLost`/track last focused, and on any navigation key with no focused widget,
  restore it (`NativeOnKeyDown` on the root widget or a game viewport client hook).
- CommonUI solves this with activatable widgets' `GetDesiredFocusTarget()` restored on activation.

## Analog stick
Analog navigation is handled by `FNavigationConfig` (Slate). Customise repeat rates and thresholds via
`FSlateApplication::Get().SetNavigationConfig(MakeShared<FMyNavConfig>())`, or disable analog
navigation during gameplay so sticks don't move hidden UI focus.

## Debugging
Widget Reflector (`WidgetReflector` command): "Pick Hit-Testable Widgets" and focus info show who has
focus per user. `Slate.Debug.TraceNavigation` CVar logs navigation decisions in recent versions.

## Gotchas
- Hidden but `Visible` focusable widgets steal navigation; use Collapsed.
- Focus on a widget inside a ScrollBox doesn't auto-scroll unless using `ScrollWidgetIntoView`
  (Scroll Box has "Scroll when focus changes").

## Verify
- [ ] Every screen reachable and escapable with gamepad only.
- [ ] Click outside then use d-pad: focus restores.
