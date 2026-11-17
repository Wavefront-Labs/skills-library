---
id: computing-software.game-programming.godot.tool-scripts-in-the-editor
name: tool-scripts-in-the-editor
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, tool-script, editor-scripting, is-editor-hint, configuration-warnings, game-programming]
level: practitioner
status: docs-checked
description: "Write @tool scripts that run in the Godot editor safely: Engine.is_editor_hint guards, live previews, configuration warnings, editor-only code and avoiding scene corruption."
sources: ["https://docs.godotengine.org/en/stable/tutorials/plugins/running_code_in_the_editor.html", "https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-private-method-get-configuration-warnings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tool scripts running in the editor

**Goal:** live previews (procedural meshes, path visualisation, auto-layout) in the editor without
gameplay code running there.

## Basics
```gdscript
@tool
class_name Fence extends Node3D

@export var length := 10.0:
    set(v): length = v; _rebuild()
@export var post_scene: PackedScene:
    set(v): post_scene = v; _rebuild(); update_configuration_warnings()

func _ready() -> void:
    _rebuild()
    if Engine.is_editor_hint():
        return                         # editor: stop here
    start_gameplay()                   # game only

func _process(delta: float) -> void:
    if Engine.is_editor_hint(): return
    # gameplay per-frame logic

func _get_configuration_warnings() -> PackedStringArray:
    return ["Assign a post scene."] if post_scene == null else []
```
- Put `@tool` at the top of the script, before `extends`/`class_name`.
- Every callback (`_process`, `_ready`, setters, `_input`) runs in the editor; guard gameplay with
  `Engine.is_editor_hint()`.
- Scripts that a tool script calls into also need `@tool` if their code must run in the editor.
- Configuration warnings show a yellow triangle in the scene tree; call `update_configuration_warnings()`
  when inputs change.

## Generated children
- Nodes created by the tool and added with `add_child` are **not saved** unless `owner` is set to the
  edited scene root: `child.owner = get_tree().edited_scene_root` (or `owner` of self). Decide: either
  regenerate every load (don't set owner) or bake and save (set owner).
- Clear previously generated children before rebuilding to avoid duplicates.

## Safety
- Tool code bugs run in the editor: infinite loops freeze the editor, `queue_free()` on the wrong node
  deletes scene content. Save often; keep tool logic small.
- `EditorInterface` (editor-only singleton) is available in tool scripts only within the editor; guard references.
- Gameplay-only autoloads may not exist in the editor; check `has_node("/root/GameState")`.

## Verify
- [ ] Opening the scene shows the preview; running the game doesn't double-generate.
- [ ] Saved .tscn doesn't contain generated nodes you intended to regenerate.

## Checked
Godot docs (stable) pages and godotengine/godot master doc/classes XML fetched 2026-10-28.
Confirmed: running-code-in-the-editor tutorial (`@tool`, `Engine.is_editor_hint()`, `owner = get_tree().edited_scene_root`) and Node `_get_configuration_warnings`/`update_configuration_warnings`.
Removed: the claim that the scene must be reopened to re-run `_ready` after editing a tool script.
Method: documentation only; no commands were run.
