---
id: computing-software.game-programming.godot.custom-controls-draw-and-gui-input
name: custom-controls-draw-and-gui-input
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, custom-control-draw, control, gui-input, ui, game-programming]
level: practitioner
status: docs-checked
description: "Write custom Godot Control nodes: _draw with draw_* calls and queue_redraw, _gui_input with accept_event, minimum size, focus and theme lookups."
sources: ["https://docs.godotengine.org/en/stable/tutorials/ui/custom_gui_controls.html", "https://docs.godotengine.org/en/stable/tutorials/2d/custom_drawing_in_2d.html", "https://docs.godotengine.org/en/stable/classes/class_control.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom controls with _draw and _gui_input

**Goal:** widgets the built-in nodes do not offer (radial menu, knob, graph) that behave like real
controls.

## Skeleton
```gdscript
@tool
class_name Knob
extends Control
signal value_changed(v: float)
@export_range(0, 1) var value := 0.5:
    set(v): value = clampf(v, 0, 1); queue_redraw(); value_changed.emit(value)
var _dragging := false

func _get_minimum_size() -> Vector2: return Vector2(48, 48)

func _draw() -> void:
    var c := size / 2
    var r := minf(size.x, size.y) / 2 - 2
    draw_circle(c, r, get_theme_color("bg", "Knob"))
    var a := lerpf(-PI * 0.75, PI * 0.75, value) - PI / 2
    draw_line(c, c + Vector2.from_angle(a) * r, get_theme_color("font_color", "Label"), 3, true)
    if has_focus(): draw_style_box(get_theme_stylebox("focus", "Button"), Rect2(Vector2.ZERO, size))

func _gui_input(e: InputEvent) -> void:
    if e is InputEventMouseButton and e.button_index == MOUSE_BUTTON_LEFT:
        _dragging = e.pressed; accept_event()
    elif e is InputEventMouseMotion and _dragging:
        value -= e.relative.y * 0.005; accept_event()
    elif e.is_action_pressed("ui_right"): value += 0.05; accept_event()
    elif e.is_action_pressed("ui_left"):  value -= 0.05; accept_event()
```
Set `focus_mode = FOCUS_ALL` in `_ready` or the Inspector so keyboard/gamepad can focus it.

## Rules
- `_draw` is called once and its commands are cached; call `queue_redraw()` on state change to redraw.
- `_gui_input` only receives events inside the control's rect (and when mouse_filter is Stop/Pass);
  `accept_event()` stops propagation to parents and `_unhandled_input`.
- Report size via `_get_minimum_size()` (and `update_minimum_size()` when it changes) so containers
  lay it out.
- Theme lookups (`get_theme_color`, `get_theme_stylebox`) with a theme type make it skinnable; add
  `theme_type_variation` support.
- React to `NOTIFICATION_THEME_CHANGED`, `NOTIFICATION_RESIZED`, `NOTIFICATION_FOCUS_ENTER/EXIT` via
  `_notification` and redraw.

## Gotchas
- `clip_contents` (default false) clips CanvasItem children to the control's rectangle; clipped parts
  also receive no input.
- Accessibility: Control has `accessibility_name` and `accessibility_description` properties; set them for screen readers.
- `get_theme_color`/`get_theme_stylebox` take `(name, theme_type)`; `focus_mode` defaults to none and
  `mouse_filter` to Stop, so set `focus_mode` explicitly.

## Verify
- [ ] Control works with mouse, keyboard and gamepad focus; resizes correctly inside containers.

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from the Control class page and the custom GUI controls and custom drawing tutorials: _get_minimum_size, update_minimum_size, accept_event and _unhandled_input behaviour, NOTIFICATION_THEME_CHANGED/RESIZED/FOCUS_ENTER/FOCUS_EXIT, get_theme_color/get_theme_stylebox signatures, clip_contents/focus_mode/mouse_filter/theme_type_variation, _draw cached. Fixed: clip_contents clips children, not the control's own drawing; replaced the 4.5+ AccessKit claim with the accessibility_name/accessibility_description properties. Removed: draw_* outside _draw errors claim.
Method: documentation only; no commands were run.
