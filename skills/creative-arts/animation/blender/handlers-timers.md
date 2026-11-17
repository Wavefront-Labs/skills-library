---
id: creative-arts.animation.blender.handlers-timers
name: handlers-timers
category: creative-arts
field: animation
product: blender
tags: [blender, handlers, app-handlers, timers, modal-operator, frame-change, load-post, save-pre, depsgraph-update, render-handlers, msgbus, persistent, event-loop, bpy, frame-change-handlers, timer-register]
level: advanced
status: verified
description: "React to Blender events from Python: bpy.app.handlers (frame, depsgraph, load/save, render), persistent, bpy.app.timers, msgbus subscriptions and modal operators."
sources:
  - https://docs.blender.org/api/current/bpy.app.handlers.html
  - https://docs.blender.org/api/current/bpy.app.timers.html
  - https://docs.blender.org/api/current/bpy.msgbus.html
  - https://docs.blender.org/api/current/bpy.types.Operator.html#modal-execution
  - https://docs.blender.org/api/current/bpy.types.DepsgraphUpdate.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# handlers-timers

Goal: code that runs *when something happens* — a frame changes, a file loads, a render finishes, a property is edited, the mouse moves — without blocking the UI.

## Application handlers (`bpy.app.handlers`)

Lists of callbacks; append a function, remove it on unregister.

| Handler | Fires | Args |
|---|---|---|
| `frame_change_pre` / `frame_change_post` | after a frame change for playback and rendering (post: after the data was evaluated for the new frame) | `(scene)` or `(scene, depsgraph)` |
| `depsgraph_update_pre` / `_post` | on depsgraph update; expect it to fire often | `(scene)` or `(scene, depsgraph)` |
| `load_pre` / `load_post` / `load_post_fail` | loading a blend file (before / after / on failure); use post for per-file setup | `(filepath)`; empty string for the startup file |
| `save_pre` / `save_post` / `save_post_fail` | saving a blend file (before / after / on failure) | `(filepath)` |
| `render_init`, `render_pre`, `render_post`, `render_write`, `render_cancel`, `render_complete`, `render_stats` | render lifecycle: `render_init` (job start), `render_pre`/`render_post` (around a render), `render_write` (right after a frame is written), `render_cancel`, `render_complete` (completion of the render job), `render_stats` (progress string) | `(scene)` / `(stats_text)` |
| `undo_pre/post`, `redo_pre/post` | on loading an undo/redo step (before / after) | `(scene)` |
| `annotation_pre/post`, `object_bake_pre/complete/cancel`, `composite_pre/post`, `animation_playback_pre/post`, `translation_update_post`, `xr_session_start_pre`, `version_update`, `load_factory_startup_post`, `load_factory_preferences_post` | as named | — |

```python
import bpy
from bpy.app.handlers import persistent

@persistent                       # callback is not removed when loading new files
def on_frame(scene, depsgraph):
    txt = bpy.data.objects.get("Counter")
    if txt and txt.type == 'FONT':
        txt.data.body = f"{scene.frame_current:04d}"

def register():
    if on_frame not in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.append(on_frame)
def unregister():
    if on_frame in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(on_frame)
```
Rules:
- Use `@persistent` on handlers an add-on registers if they must survive loading files; check membership before appending so Reload Scripts does not double them (practice; compare by `__name__` if the function object changed).
- Alter data from handlers carefully. The docs warn that while rendering, `frame_change_pre`/`frame_change_post` run on a different thread from viewport updates, so changing data the viewport reads can crash Blender; lock the interface first (Render → Lock Interface, `RenderSettings.use_lock_interface`). In `depsgraph_update_post`, avoid edits that trigger another update (practice) and filter with `depsgraph.updates` (`for u in depsgraph.updates: u.id, u.is_updated_geometry, u.is_updated_transform`).
- `frame_change_pre` runs **before** evaluation: set properties here so drivers/modifiers see them in the same frame. Post is for reading evaluated results (use `ob.evaluated_get(depsgraph)`).
- Render handlers are the hooks for render automation: `render_pre` to switch settings per frame, `render_write` to act on each written frame, `render_complete` when the job completes.
- `load_post` is the hook for studio setup: enforce fps/colour management (`creative-arts.animation.blender.scene-units-setup`), relink libraries, register per-file UI; `bpy.context` may be limited there, so prefer the data API over operators that need a window (practice).
- Keep handlers fast (frame_change runs every frame during playback); never block on network/IO there — queue work for a timer.

## Timers (`bpy.app.timers`)

Run a function on the main thread after a delay, optionally repeating; the UI stays responsive between calls.
```python
def poll_job():
    if job_done():
        bpy.ops.wm.save_mainfile(); return None     # None = stop
    return 2.0                                      # seconds until next call
bpy.app.timers.register(poll_job, first_interval=1.0, persistent=True)
bpy.app.timers.is_registered(poll_job); bpy.app.timers.unregister(poll_job)
```
- Returning a float reschedules; `None` stops. `persistent=True` survives file loads.
- Use for: polling farms/subprocesses, deferred setup after `load_post`, auto-save scripts, progress updates. To run UI operators from a timer, supply the context yourself (practice): `win = bpy.context.window_manager.windows[0]; with bpy.context.temp_override(window=win, area=win.screen.areas[0]): bpy.ops...`.
- Threads (practice, not covered by the pages checked): do heavy work in a `threading.Thread` or `subprocess`, hand results back through a `queue.Queue` drained by a timer, and touch `bpy` only from the main thread.

## msgbus (property change subscriptions)

React to one specific property without a depsgraph handler:
```python
owner = object()
def on_active_change(*_): print("location changed")
bpy.msgbus.subscribe_rna(key=(bpy.types.Object, "location"), owner=owner, args=(), notify=on_active_change)
bpy.msgbus.subscribe_rna(key=bpy.context.scene.path_resolve("frame_current", False), owner=owner, args=(), notify=...)
# cleanup: bpy.msgbus.clear_by_owner(owner)
```
Notifications come from the RNA system: changes via the Python API (`some_object.location.x += 3`) and via sliders, fields and buttons in the UI trigger them; moving objects in the 3D Viewport and changes by the animation system do not. Callbacks are postponed until all operators have finished and their changes are not part of the related undo steps. Keys: `(bpy.types.Object, "location")` or a resolved property for one data-block. All subscribers are cleared on file load — re-subscribe from a `load_post` handler.

## Modal operators (interactive tools)

```python
class MYTOOL_OT_drag(bpy.types.Operator):
    bl_idname = "mytool.drag"; bl_label = "Drag Value"; bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}
    def invoke(self, context, event):
        self.start = event.mouse_x; self.orig = context.object.location.x
        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(0.1, window=context.window)  # optional TIMER events
        return {'RUNNING_MODAL'}
    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            context.object.location.x = self.orig + (event.mouse_x - self.start) * 0.01
            context.area.header_text_set(f"X: {context.object.location.x:.3f}")
        elif event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            self.finish(context); return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.object.location.x = self.orig; self.finish(context); return {'CANCELLED'}
        elif event.type == 'TIMER':
            pass
        return {'RUNNING_MODAL'}          # or {'PASS_THROUGH'} to let the event reach the UI (navigation)
    def finish(self, context):
        context.window_manager.event_timer_remove(self._timer); context.area.header_text_set(None)
```
- `event.type` (`'MOUSEMOVE'`, `'LEFTMOUSE'`, `'WHEELUPMOUSE'`, `'A'`, `'RET'`, `'ESC'`, `'TIMER'`, `'INBETWEEN_MOUSEMOVE'`…), `event.value` (`'PRESS'`/`'RELEASE'`/`'CLICK_DRAG'`), modifiers `event.shift/ctrl/alt`, `event.mouse_region_x/y`, `event.pressure`, `event.tilt`.
- Return `'PASS_THROUGH'` (do nothing and pass the event on) for events you don't consume so orbit/zoom keep working; `'RUNNING_MODAL'` keeps the operator running.
- Draw overlays while modal with a `SpaceView3D.draw_handler_add` (`creative-arts.animation.blender.gpu-module-drawing`); remove in `finish`.
- For long jobs: a modal operator with a timer polls a thread/subprocess and updates a progress bar (`wm.progress_begin/update/end`) — the classic non-blocking export/bake pattern.
- `bl_options` `'BLOCKING'` blocks anything else from using the cursor; `'GRAB_CURSOR'` makes the operator grab the mouse focus (enables wrap when continuous grab is enabled).

## Gotchas

- Handlers without `@persistent` are removed when a new file is loaded.
- Timers registered with `persistent=False` are removed on file load; use `is_registered` to avoid duplicates on reload.
- Prefer the data API over `bpy.ops` inside handlers, or build a context with `temp_override` (practice).
- `frame_change` handlers run every frame during playback, so keep them cheap (practice).
- Clear msgbus subscriptions with `clear_by_owner(owner)` on unregister.

## Verify

- `frame_change_post`: scrubbing updates the text object every frame and the handler survives `File → Open` (persistent).
- Reload Scripts twice: `len(bpy.app.handlers.frame_change_post)` doesn't grow.
- Timer: returns a float and `is_registered` stays True; returning `None` stops it; UI remains responsive during a fake 10-second job driven from a thread.
- Modal: `Esc` restores the original value and leaves no draw handler/timer behind (`header_text_set(None)` cleared the header).

## Checked

Blender Python API 5.2 (docs.blender.org/api/current), read 2026-10-27.
- Every handler name in the table exists in `bpy.app.handlers`; argument lists for frame_change/depsgraph_update (scene, optional depsgraph), load/save (file path, empty string for startup file), render_* (scene), render_stats (string), undo/redo (scene), version_update and translation_update_post (none); `persistent` decorator; the thread/Lock Interface warning for frame_change handlers.
- `bpy.app.timers.register(function, *, first_interval=0, persistent=False)`, `is_registered`, `unregister`, return-float-or-None rule.
- msgbus limitations page: Python-API and UI changes notify, 3D Viewport moves and animation do not; subscribers cleared on file load (re-register from load_post); `clear_by_owner`. Corrected the old claim that Python assignments do not notify.
- Operator flags BLOCKING and GRAB_CURSOR, `Event` attributes (mouse_x, mouse_region_x, pressure, tilt, type, value incl. CLICK_DRAG), `DepsgraphUpdate.is_updated_geometry/is_updated_transform`, `WindowManager.progress_begin/update/end`, `Area.header_text_set`.
- Removed as unconfirmed: the `_bpy_persistent` attribute, non-main-thread timer registration, exception-handling behaviour of handlers, and performance thresholds. Thread-safety guidance is labelled practice.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: every handler name in the table exists on `bpy.app.handlers`; a `@persistent` `frame_change_post` function with `(scene, depsgraph=None)` was called with a Scene and a Depsgraph and a one-argument `frame_change_pre` function was also accepted; `load_post` received an empty string for the factory-startup load and a persistent handler stayed registered; `bpy.app.timers` has `register(function, first_interval=0, persistent=False)`, `is_registered` and `unregister` (unregistering twice raised ValueError); `WindowManager` has `progress_begin/update/end`, `modal_handler_add`, `event_timer_add/remove`, `Area` has `header_text_set`, `RenderSettings.use_lock_interface` exists, `DepsgraphUpdate` has `is_updated_transform`, `is_updated_geometry`; operator `bl_options` includes BLOCKING and GRAB_CURSOR; `Event` has `mouse_x`, `mouse_region_x/y`, `pressure`, `tilt` and value `CLICK_DRAG`; a font `body` string can be set. Unrun (need a UI session): msgbus notifications, the modal operator, timers firing, the threading and Lock Interface warnings, handler behaviour during playback and render.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
