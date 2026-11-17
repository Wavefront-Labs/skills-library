---
id: computing-software.game-programming.godot.node-owner-and-saving-scenes
name: node-owner-and-saving-scenes
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, node-owner, packedscene, tool-scripts, reparenting, game-programming]
level: practitioner
status: verified
description: "Set the Godot Node owner so nodes created by tool scripts or at runtime are saved with PackedScene.pack and editor scenes, and keep owner correct when reparenting."
sources: ["https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-property-owner", "https://docs.godotengine.org/en/stable/classes/class_packedscene.html", "https://docs.godotengine.org/en/stable/tutorials/plugins/running_code_in_the_editor.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node owner and saving scenes

**Goal:** nodes added by code actually appear in the saved scene file.

## The rule
`PackedScene.pack(root)` and the editor's save only include nodes whose `owner` is the scene root
(or an owner chain leading to it). Nodes added with `add_child` have `owner = null`, so they exist at
runtime/in the editor tree but vanish on save.

## Tool scripts adding nodes in the editor
```gdscript
@tool
extends Node3D
@export var count := 10:
    set(v): count = v; if is_inside_tree(): _rebuild()

func _rebuild() -> void:
    for c in get_children(): c.queue_free()
    for i in count:
        var m := MeshInstance3D.new()
        m.mesh = BoxMesh.new()
        m.position.x = i * 2.0
        add_child(m)
        m.owner = get_tree().edited_scene_root   # visible in Scene dock and saved
```
Set owner **after** `add_child`. Leave owner null on purpose for helper nodes you regenerate (they
are not saved and not shown in the Scene dock).

## Saving a runtime-built scene
```gdscript
func save_level(root: Node, path: String) -> void:
    for n in root.find_children("*", "", true, false):
        n.owner = root
    var ps := PackedScene.new()
    if ps.pack(root) == OK:
        ResourceSaver.save(ps, path)
```
Nodes inside an instanced sub-scene keep their sub-scene owner; set owner only on nodes you created,
or the instance gets flattened into the saved file (run: packing with only the instance's owner set kept the
instance as one `Sub` entry; also setting the owner of its `Inner` child added `Inner` as a node of the saved scene).

## Reparenting
`reparent(new_parent, keep_global_transform)` (Godot 4) keeps global transform by default (run: global position stayed (5, 5) while the local position became (-95, 5)); with manual
`remove_child`/`add_child` re-set owner. Assigning an owner that is not an ancestor errors (`Invalid owner. Owner must be an ancestor in the tree.`), and a node whose owner stays null is left out of `pack()` (run).

## Gotchas
- `get_tree().edited_scene_root` is null at runtime (run) and the class reference says it does nothing in release builds; guard with `Engine.is_editor_hint()`.
- Duplicated nodes (`duplicate()`) keep children but the owner of the copies must be re-set (run: `get_child(0).owner` was null on the duplicate).

## Verify
- [ ] Generated nodes survive save and reload; Scene dock shows exactly the intended nodes.
## Checked
Ran on Godot 4.7.2 headless: `PackedScene.pack` with and without owners (a child with owner null vanished from `instantiate()`, set via `find_children("*", "", true, false)` all appeared), instance flattening, invalid owner error, `duplicate()` owner, `reparent` with default and `false`, `edited_scene_root` null. `m.owner = get_tree().edited_scene_root` and the Scene dock visibility only apply inside the editor; the 4.7.2 `Node.owner` reference ("nodes not owned by the scene root ... will not be saved. To prevent this, remember to set the owner after calling `add_child()`") and the Godot "Running code in the editor" page (`node.owner = get_tree().edited_scene_root`) document it.
