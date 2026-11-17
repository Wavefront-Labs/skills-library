---
id: computing-software.game-programming.godot.editor-vs-code-signal-connections
name: editor-vs-code-signal-connections
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, editor-signal-connections, signals, node-dock, game-programming]
level: practitioner
status: docs-checked
description: "Decide between Godot editor signal connections (Node dock, stored in .tscn) and code connections, find hidden connections, and fix broken method targets after renames."
sources: ["https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html", "https://docs.godotengine.org/en/stable/classes/class_object.html#class-object-method-connect", "https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Editor vs code signal connections

**Goal:** connections that are discoverable, survive refactors and match team conventions.

## Editor connections
Select a node > **Node dock > Signals** > double-click a signal > pick target node and method. Stored
in the scene file:
```
[connection signal="pressed" from="UI/StartButton" to="." method="_on_start_button_pressed"]
```
Options in the dialog: binds (extra args), Deferred, One Shot, Unbinds.

## Code connections
```gdscript
func _ready() -> void:
    $UI/StartButton.pressed.connect(_on_start_pressed)
    health.died.connect(_on_died, CONNECT_ONE_SHOT)
```

## Choosing
| | Editor | Code |
|---|---|---|
| Visible when reading the script | no | yes |
| Survive node renames | yes (editor updates path) | breaks `$Path` unless %UniqueName |
| Survive method renames | breaks | breaks unless the connect call uses the renamed Callable |
| Dynamic instances (spawned) | no | yes |
| Designer-friendly | yes | no |
Common convention: editor connections for UI wiring inside one scene; code for anything dynamic,
cross-scene or gameplay-critical. Pick one per project and document it.

## Finding and fixing
- Search `.tscn` files for editor connections: `grep -rn 'method="_on_' --include=*.tscn`.
- The Node dock lists the connections of the selected node.

## Gotchas
- Connecting the same signal in both editor and code calls the handler twice; `is_connected` checks
  help during migration.

## Verify
- [ ] No duplicate connections; renaming a handler shows up as an error, not silent breakage.

## Checked
Godot docs (stable) pages and godotengine/godot master doc/classes XML fetched 2026-10-28.
Confirmed: the signals tutorial and Object.connect (code connection form, `CONNECT_ONE_SHOT`), scene organisation page; `[connection ...]` entries are the .tscn format used in the tutorial.
Removed: gutter icon, `Method not found` log text, inherited-scene connection claims, and `get_signal_connection_list` runtime inspection (not on fetched pages); rewrote the rename row.
Method: documentation only; no commands were run.
