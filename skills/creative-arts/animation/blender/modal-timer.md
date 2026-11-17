---
id: creative-arts.animation.blender.modal-timer
name: modal-timer
category: creative-arts
field: animation
product: blender
tags: [blender, modal-timer, event-timer-add, modal-operator, timer-event, handlers-timers, bpy]
level: advanced
status: docs-checked
description: "Run periodic work inside a modal operator with event_timer_add: TIMER events, pass-through, cancel on Esc, removing the timer, and when to use bpy.app.timers instead."
sources:
  - https://docs.blender.org/api/current/bpy.types.WindowManager.html#bpy.types.WindowManager.event_timer_add
  - https://docs.blender.org/api/current/bpy.types.Operator.html#modal-execution
  - https://docs.blender.org/api/current/bpy.app.timers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# modal-timer

Goal: an operator that updates something every N seconds (poll a file, animate a preview, step a simulation) while the user keeps working, and stops cleanly.

## Pattern (based on the "Operator Modal Timer" template)

```python
import bpy

class WM_OT_watch_file(bpy.types.Operator):
    bl_idname = "wm.watch_file"
    bl_label = "Watch File"
    _timer = None

    def modal(self, context, event):
        if event.type in {'ESC'} or not context.scene.get("watching", True):
            self.cancel(context)
            return {'CANCELLED'}
        if event.type == 'TIMER':
            self.tick(context)               # keep this fast; it runs on the UI thread
        return {'PASS_THROUGH'}              # let every other event reach the UI

    def tick(self, context):
        ...

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.5, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None
```

- `event_timer_add(time_step, *, window=None)` generates periodic `TIMER` events (`time_step` is the interval in seconds); remove it with `event_timer_remove`. Treat the interval as approximate (practice).
- Return `{'PASS_THROUGH'}` for events you do not handle: it means "do nothing and pass the event on", so other input still reaches the UI.
- `Operator.cancel(context)` is called when the operator is canceled: remove the timer there.

## modal timer vs bpy.app.timers

| Need | Use |
|---|---|
| Needs operator context, report(), Esc to stop, per-window | Modal + `event_timer_add` |
| Background task not tied to a window; no operator needed | `bpy.app.timers.register(fn, first_interval=...)`; the function returns the seconds until its next call, or `None` to stop |

## Gotchas

- To run operators that need a specific area from `modal`, use `context.temp_override(window=, screen=, area=, region=)` (practice), and redraw with `area.tag_redraw()`.
- `bpy.ops.ed.undo_push` is documented as internal use only; avoid it in tools.
- Handlers registered with `bpy.app.handlers.load_post` need the `persistent` decorator to survive loading a file.

## Verify

Start the operator, keep orbiting the viewport (input still works), watch the tick run twice a second (print), press `Esc` and confirm the prints stop.

## Checked

Blender Python API 5.2 (docs.blender.org/api/current), read 2026-10-27.
- `WindowManager.event_timer_add(time_step, *, window=None)`, `modal_handler_add`, `event_timer_remove`; `Operator.modal/cancel`; `bpy.app.timers.register(..., first_interval=)` with the return-seconds-or-None convention; `Context.temp_override(window, screen, area, region, **kw)`; `bpy.ops.ed.undo_push` flagged internal use only; `persistent` decorator for load handlers.
- Removed as unconfirmed: background-mode and file-load behaviour of modal operators and the exact cancel-on-abort cases.

Method: documentation only; no commands were run.
