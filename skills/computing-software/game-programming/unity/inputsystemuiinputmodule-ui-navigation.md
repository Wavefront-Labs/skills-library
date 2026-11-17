---
id: computing-software.game-programming.unity.inputsystemuiinputmodule-ui-navigation
name: inputsystemuiinputmodule-ui-navigation
category: computing-software
field: game-programming
product: unity
tags: [unity, inputsystemuiinputmodule, input-system, ugui, ui-navigation, eventsystem, game-programming]
level: practitioner
status: docs-checked
description: "Configure InputSystemUIInputModule so uGUI and UI Toolkit get pointer, navigation and tracked input from Input System actions, plus MultiplayerEventSystem."
sources: ["https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/UISupport.html", "https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/api/UnityEngine.InputSystem.UI.MultiplayerEventSystem.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InputSystemUIInputModule

**Goal:** menus navigate with gamepad, keyboard and mouse through the Input System. Package version 1.11 docs.

## When the module is needed
- Unity UI (uGUI): always required. UI Toolkit: required before Unity 2023.2; from 2023.2 the UI actions in the default
  project-wide actions map directly to UI Toolkit input and the module is not required (if present, its settings take
  priority over the project-wide actions). IMGUI: not compatible; to keep legacy input for `OnGUI` set Active Input
  Handling to Both (input is processed twice).
- Add it to a GameObject via Add Component > "Input System UI Input Module". If an older Standalone Input Module is
  present and the Input System is installed, the Inspector offers a button to replace it.
- With the module in the scene, the UI action map is enabled along with the default action map set on the module.

## Required actions
The default project-wide actions include a "UI" action map. To stay compatible with UI Toolkit, keep the map name "UI",
the action names and their Action Types:

| Action | Action Type / Control Type |
|---|---|
| Navigate | PassThrough / Vector2 |
| Submit, Cancel | Button / Button |
| Point | PassThrough / Vector2 |
| Click, RightClick, MiddleClick | PassThrough / Button |
| ScrollWheel | PassThrough / Vector2 |
| Tracked Device Position / Orientation | PassThrough / Vector3 / Quaternion |

## Module properties
- **Move Repeat Delay**: delay before navigation events repeat while Move stays actuated. **Move Repeat Rate**: interval
  between repeats, capped by frame rate (at most one repeat per frame).
- **Actions Asset**: defaults to the built-in `DefaultInputActions`; assigning your own asset makes the Editor try to map
  actions by common naming conventions.
- **Deselect on Background Click**: default clears the selection when a click hits nothing; set false so keyboard and
  gamepad navigation keep the current selection.
- **Pointer Behavior**: Single Mouse or Pen But Multi Touch And Track (default), Single Unified Pointer, All Pointers As Is.
- **Cursor Lock Behavior**: origin of UI raycasts when the cursor is locked; the pointer is otherwise pinned at (-1,-1).

## Input types
- Pointer (point, click actions, scroll): set the actions to PassThrough so no filtering is applied. Binding a click
  without a point on the same device routes it to another pointer (Space as left click clicks at the mouse position).
- Navigation: only one move vector, one submit and one cancel are processed per frame. Move is PassThrough; submit and
  cancel must be Button. Navigation acts on the current selection, not a position.
- Tracked (XR): needs a `TrackedDeviceRaycaster` next to the Canvas's `GraphicRaycaster`; not supported with UI Toolkit.

## Multiplayer UI
Replace the EventSystem with `MultiplayerEventSystem` (several can be active at once). Each player has their own UI
Input Module and event system. Set **Player Root** (`playerRoot`) to the Canvas or hierarchy part owned by the player:
mouse selection ignores objects outside it, and keyboard or gamepad navigation is constrained to it. Player Input can be
set to configure the player's UI Input Module automatically.

## Notes
- UI Toolkit: `button.clicked` fires for both pointer and gamepad submit; `RegisterCallback<ClickEvent>` does not fire for
  gamepad (a NavigationSubmitEvent).
- No automatic mechanism stops a click consumed by UI from also reaching gameplay actions. For pointers, poll in `Update`
  and use `EventSystem.IsPointerOverGameObject` (calling it inside `InputAction` callbacks gives a warning); for
  navigation, split controls (d-pad for UI, sticks for game) or use an explicit mode switch that suspends gameplay actions.
- Virtual Mouse (uGUI only): do not also bind gamepad navigation on the module, or input triggers twice.

## Checked
Date: 2026-11-07.
Read in full: Input System 1.11 "UI support" manual page and the MultiplayerEventSystem API page. The 30K
InputSystemUIInputModule API page was only searched for property names and defaults (`deselectOnBackgroundClick`,
`pointerBehavior`, `moveRepeat*`, `actionsAsset`, `AssignDefaultActions`), not read end to end, so the draft's source link
to it was removed.
Corrected: the draft said Active Input Handling = Input System only makes the old module throw, and that Unity UI
needed only some actions; the page lists the full required action set with Action Types and says UI Toolkit from 2023.2
needs no module.
Removed as unconfirmed: "PlayerInput enables only its default map" and `SwitchCurrentActionMap("UI")` advice,
`PlayerInput.uiInputModule`, `EventSystem.SetSelectedGameObject` first-button advice, the gamepad south button
Jump/Submit clash, the "mouse steals selection" remark and the invented Verify checklist.
Method: documentation only; no commands were run.
