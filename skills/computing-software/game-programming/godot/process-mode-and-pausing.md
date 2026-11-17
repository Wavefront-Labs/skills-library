---
id: computing-software.game-programming.godot.process-mode-and-pausing
name: process-mode-and-pausing
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-scenes, process-mode, scene-tree-pause, pause-menu-godot, game-programming]
level: practitioner
status: docs-checked
description: "Pause Godot games properly with SceneTree.paused and process_mode (Inherit, Pausable, WhenPaused, Always, Disabled), including physics, timers, tweens, audio and UI."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/pausing_games.html", "https://docs.godotengine.org/en/stable/classes/class_node.html#enum-node-processmode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# process_mode and pausing

**Goal:** a pause menu that freezes gameplay while UI, music and certain effects keep running.

## Mechanism
`get_tree().paused = true` stops processing of nodes whose effective mode is Pausable.
`Node.process_mode`:
- `PROCESS_MODE_INHERIT` (default): uses the first ancestor with a non-Inherit mode; if none, the
  SceneTree pause state applies (so by default everything pauses).
- `PROCESS_MODE_PAUSABLE`: stops when paused.
- `PROCESS_MODE_WHEN_PAUSED`: runs only while paused (pause menu).
- `PROCESS_MODE_ALWAYS`: always runs (music manager, debug overlay).
- `PROCESS_MODE_DISABLED`: never processes (cheap way to freeze a subtree).

Stopped nodes get no `_process`, `_physics_process`, `_input` or `_input_event` calls. Pausing stops 2D and
3D physics for all nodes, even ones that keep processing; the physics servers can be kept active with their
`set_active` methods. Signals still run their connected functions on nodes that are not processing.

## Pause menu
```gdscript
# PauseMenu (CanvasLayer), process_mode = ALWAYS (set in inspector) so it also sees the key that pauses
func _unhandled_input(event):
    if event.is_action_pressed("pause"):
        get_tree().paused = not get_tree().paused
        visible = get_tree().paused
        get_viewport().set_input_as_handled()
```
A `WHEN_PAUSED` node only processes while paused, so the node that toggles pause on a key press must be
`ALWAYS` (as here). The docs' example instead gives the menu root `When Paused` and calls
`get_tree().paused = true` plus `show()` from a pause button that lives in the pausable part of the scene.

## What else pauses
- Animation nodes pause their current animation, audio nodes pause their current stream and particles
  pause; they resume automatically on unpause. Put music players on `ALWAYS` if it should keep playing.
- **Tweens** have a pause mode: `TWEEN_PAUSE_BOUND` (follows the bound node's process mode; without a bound
  node it behaves like STOP), `TWEEN_PAUSE_STOP` or `TWEEN_PAUSE_PROCESS` (runs regardless of the pause
  state): `tween.set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)` keeps UI tweens running.
- **SceneTreeTimer**: `get_tree().create_timer(time_sec, process_always = true, ...)`; `process_always`
  defaults to true, so it keeps running while paused. Pass false to pause it.

## Gotchas
- Signals still run their connected functions even if the receiving node is not processing.
- A node that keeps processing while the game is paused still gets no physics unless the physics servers
  are made active.

## Verify
- [ ] Pause during a jump: player, enemies, projectiles and timers freeze; music and menu work.
- [ ] Unpause resumes physics without velocity jumps.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: `SceneTree.paused` stops 2D and 3D physics and changes behaviour by process mode; Inherit, Pausable, WhenPaused, Always and Disabled semantics and the SceneTree fallback; `_process`, `_physics_process`, `_input` and `_input_event` stop; signals still run connected functions; physics servers can stay active with `set_active`; animation, audio and particles pause; `Tween.set_pause_mode` with BOUND, STOP and PROCESS; `SceneTree.create_timer(time_sec, process_always = true, process_in_physics = false, ignore_time_scale = false)`. The earlier example would not have unpaused from a `WHEN_PAUSED` node on the pause key and was corrected. Removed the unconfirmed Timer `process_callback`, `Engine.time_scale` and scene-change claims.

Method: documentation only; no commands were run.
