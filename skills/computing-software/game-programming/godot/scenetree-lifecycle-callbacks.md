---
id: computing-software.game-programming.godot.scenetree-lifecycle-callbacks
name: scenetree-lifecycle-callbacks
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, scenetree, _enter_tree, _ready, _process, node-lifecycle, notifications, game-programming]
level: practitioner
status: verified
description: "Know Godot 4's node lifecycle order: _init, _enter_tree, _ready (children first), _process/_physics_process, _exit_tree, notifications, process modes and when @onready runs."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/scene_tree.html", "https://docs.godotengine.org/en/stable/classes/class_node.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SceneTree lifecycle

**Goal:** initialise in the right callback so references exist and nothing runs twice or too early.

## Order
| Callback | When | Order in hierarchy |
|---|---|---|
| `_init()` | object constructed (also for `new()`) | n/a; no tree, no children for scripted nodes |
| `_enter_tree()` | node added to the tree (each time) | **parent before children** |
| `_ready()` | after node and all children entered, first time only | **children before parent** |
| `_process(delta)` / `_physics_process(delta)` | every frame / physics tick | tree order (run: `A, A's child K, B`); lower `process_priority` runs first (run: `B` with priority -1 ran before `A`) |
| `_exit_tree()` | removed from tree | children before parent |
| `NOTIFICATION_PREDELETE` | about to be freed | |

- `@onready var hp_bar := $HPBar` assigns right before `_ready()`.
- `_ready` runs once per node lifetime; removing and re-adding a node calls `_enter_tree` again but not
  `_ready` unless you call `request_ready()`.
- Because children are ready first, a parent's `_ready` can use its children; a child's `_ready` must
  not rely on the parent being ready (use signals or `await owner.ready`).
- `_physics_process` runs at Physics Ticks Per Second (default 60 in the 4.7.2 `ProjectSettings` reference and `Engine.physics_ticks_per_second` returned 60), independent of render FPS.
- Run on 4.7.2 with parent `P` and children `C1`, `C2`: add to tree printed `enter P, enter C1, enter C2, ready C1, ready C2, ready P`; removal printed `exit C2, exit C1, exit P`; re-adding printed enter only (no ready); `request_ready()` on `P` before re-adding gave `ready P` again.

## Notifications
```gdscript
func _notification(what: int) -> void:
    match what:
        NOTIFICATION_WM_CLOSE_REQUEST: save_game()
        NOTIFICATION_APPLICATION_FOCUS_OUT: pause_game()
        NOTIFICATION_PREDELETE: release_native_handle()
```
Also `NOTIFICATION_PAUSED`/`UNPAUSED`, `NOTIFICATION_PARENTED`, `NOTIFICATION_TRANSFORM_CHANGED`
(enable with `set_notify_transform(true)`).

## Process control
- `set_process(false)` / `set_physics_process(false)` to stop callbacks (also stops `_input` with `set_process_input`).
- `process_mode`: `PROCESS_MODE_INHERIT`, `PAUSABLE`, `WHEN_PAUSED`, `ALWAYS`, `DISABLED`. With
  `get_tree().paused = true`, pause menus need `ALWAYS` / `WHEN_PAUSED`.
- `get_tree().process_frame` / `physics_frame` signals to await the next frame.

## SceneTree itself
`get_tree()` gives: `current_scene`, `paused`, `create_timer()`, `call_group()`, `quit()`,
`change_scene_to_file()`, `root` (the Window; run: `root is Window` true). Nodes outside the tree return null for `get_tree()` (and log `Parameter "data.tree" is null`).

## Verify
- [ ] No "Node not found" errors from `$Path` in `_ready` of children that expected parent state.
- [ ] Pausing stops gameplay but not the pause menu.
## Checked
Ran on Godot 4.7.2 headless: callback order with `_init`, `_enter_tree`, `_ready`, `_exit_tree`, `NOTIFICATION_PREDELETE`, `NOTIFICATION_PARENTED`, `NOTIFICATION_PAUSED`/`UNPAUSED` (all fired in a pause test); `@onready` var assigned before `_ready` (the parent saw its child, the child and sibling did not have a `K` child); `_process` order and `process_priority`; `set_process(false)` stopped the callback; `process_mode = PROCESS_MODE_ALWAYS` kept processing while `paused` (children inherit it); `NOTIFICATION_TRANSFORM_CHANGED` exists on `Node2D` (not on `Node`) with `set_notify_transform`; `NOTIFICATION_WM_CLOSE_REQUEST` and `NOTIFICATION_APPLICATION_FOCUS_OUT` exist in the 4.7.2 `Node` reference.
