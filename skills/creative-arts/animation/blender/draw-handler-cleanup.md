---
id: creative-arts.animation.blender.draw-handler-cleanup
name: draw-handler-cleanup
category: creative-arts
field: animation
product: blender
tags: [blender, draw-handler-cleanup, draw-handler-remove, draw-handler, gpu-module-drawing, unregister, bpy]
level: advanced
status: docs-checked
description: "Add and remove viewport draw handlers safely: keep the handle, remove on unregister and reload, avoid duplicate overlays, redraw areas and survive file loads."
sources:
  - https://docs.blender.org/api/current/bpy.types.SpaceView3D.html#bpy.types.SpaceView3D.draw_handler_remove
  - https://docs.blender.org/api/current/gpu.html
  - https://docs.blender.org/api/current/bpy.types.SpaceView3D.html#bpy.types.SpaceView3D.draw_handler_add
  - https://docs.blender.org/api/current/bpy.app.html#bpy.app.driver_namespace
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# draw-handler-cleanup

Goal: an overlay that appears once, disappears when disabled, and never leaves a ghost drawing after Reload Scripts.

## Pattern

```python
import bpy
_handles = {}

def draw_cb():
    ...  # gpu drawing; must not raise every frame

def enable():
    if "overlay" not in _handles:
        _handles["overlay"] = bpy.types.SpaceView3D.draw_handler_add(draw_cb, (), 'WINDOW', 'POST_VIEW')
    redraw()

def disable():
    h = _handles.pop("overlay", None)
    if h is not None:
        try:
            bpy.types.SpaceView3D.draw_handler_remove(h, 'WINDOW')
        except ValueError:
            pass          # already removed
    redraw()

def redraw():
    for win in bpy.context.window_manager.windows:
        for area in win.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

def register():
    ...
def unregister():
    disable()
```

## Rules

- `SpaceView3D.draw_handler_add(callback, args, region_type, draw_type)` returns a handler object (all arguments positional); remove it with `draw_handler_remove(handler, region_type)` using the same region type. `draw_type` is usually `POST_PIXEL` for 2D drawing and `POST_VIEW` for 3D. Keep the handle in module state, not in scene properties.
- Reload Scripts re-imports the module, creating a fresh `_handles` while the old handler still draws: `unregister()` must run (it does for add-ons). For Text Editor scripts, store the handle in `bpy.app.driver_namespace["myoverlay"]` (an editable dict that is reset on file load) so a rerun finds and removes the previous one.
- After add/remove, tag redraw so the viewport updates immediately.

## Gotchas

- Wrap the callback body in try/except during development so one error does not repeat on every redraw (practice).
- Look data up by name inside the callback rather than holding `bpy.types.Object` references across file loads (practice).
- Modal operators that add handlers should remove them on every exit path, including `cancel()` (practice).

## Verify

Enable, disable, enable again: only one overlay; Reload Scripts, then confirm nothing draws twice.

## Checked

Blender Python API 5.2 (docs.blender.org/api/current), read 2026-10-27.
- `SpaceView3D.draw_handler_add(callback, args, region_type, draw_type)` (positional-only, returns a removable handler), `draw_handler_remove(handler, region_type)`, draw_type guidance (POST_PIXEL, POST_VIEW, PRE_VIEW, BACKDROP); `bpy.app.driver_namespace` is editable in place and reset on file load: API 5.2.
- Removed as unconfirmed: that handlers survive File > Open, and the claim that an unreferenced handle cannot be removed until restart. Remaining advice is labelled practice.

Method: documentation only; no commands were run.
