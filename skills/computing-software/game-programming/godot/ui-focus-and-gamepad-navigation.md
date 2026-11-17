---
id: computing-software.game-programming.godot.ui-focus-and-gamepad-navigation
name: ui-focus-and-gamepad-navigation
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-ui, focus-navigation, gamepad-ui, grab-focus, focus-neighbors, accessibility, game-programming]
level: practitioner
status: docs-checked
description: "Make Godot menus fully keyboard/gamepad navigable: focus modes, grab_focus on open, focus neighbours and wrapping, visible focus styles and ui_* input actions."
sources: ["https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html", "https://docs.godotengine.org/en/stable/classes/class_control.html#class-control-property-focus-mode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyboard and gamepad focus navigation

**Goal:** every menu works without a mouse; focus is always visible and never lost.

## Basics
- Navigation uses built-in actions `ui_up/down/left/right`, `ui_accept`, `ui_cancel`, `ui_focus_next/prev`
  (Tab). They are listed in Project Settings > Input Map and can be edited; do not reuse them for gameplay code.
- Controls need `focus_mode = FOCUS_ALL` (All: mouse click or keyboard/controller; Click: mouse only; None).
  Buttons default to All, Labels to None.
- **Something must have focus** when a menu opens:
```gdscript
func open() -> void:
    show()
    %ResumeButton.grab_focus()            # the docs use grab_focus.call_deferred() in _ready()
```

## Neighbours
- With no neighbour configured the engine guesses the next control, which can behave unexpectedly in
  complex layouts. Set `focus_neighbor_top/bottom/left/right` (4-way) and `focus_next/previous` (the Tab
  order) as NodePaths on each control where you need a defined flow (grids, wrap from last to first).

## Visible focus
- Theme `focus` StyleBox (Button has one); make it obvious (thick outline, scale tween on
  `focus_entered`).
- For mixed input, you can call `grab_focus()` from `mouse_entered` so keyboard navigation continues from
  the hovered button.

## Common patterns
```gdscript
func _unhandled_input(e: InputEvent) -> void:
    if visible and e.is_action_pressed("ui_cancel"):
        close(); get_viewport().set_input_as_handled()

# restore focus when returning from a submenu
var _last_focus: Control
func open_submenu() -> void:
    _last_focus = get_viewport().gui_get_focus_owner()
    submenu.open()
func on_submenu_closed() -> void:
    if is_instance_valid(_last_focus): _last_focus.grab_focus()
```
- A control can lose focus when it becomes hidden; move focus before hiding it.
- ScrollContainer: `follow_focus = true` (default false) scrolls to the focused child.

## Verify
- [ ] Unplug the mouse: every menu, settings screen and dialog is fully usable with a pad.
- [ ] Focus is visible at all times and returns to the previous button after closing submenus.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: `ui_up/down/left/right`, `ui_focus_next`, `ui_accept`-style built-in actions live in the Input Map and should not be used for gameplay; focus modes All, Click and None with Label None and Button All; focus neighbours (4-way) and Next/Previous; automatic guessing when no neighbour is set; focus is lost when a node is hidden; initial focus must be set in code with `grab_focus()` (docs use `grab_focus.call_deferred()` in `_ready`); `ScrollContainer.follow_focus` (default false); `Viewport.gui_get_focus_owner` and `set_input_as_handled`. Removed the unconfirmed gamepad-binding, container-predictability, hover-focus, disabled-control and slider claims.

Method: documentation only; no commands were run.
