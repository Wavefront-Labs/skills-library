---
id: computing-software.game-programming.godot.3d-gizmo-plugins
name: 3d-gizmo-plugins
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, editornode3dgizmoplugin, editor-plugins, gizmos, tool-scripts, game-programming]
level: practitioner
status: docs-checked
description: "Draw and edit custom 3D gizmos in the Godot editor with EditorNode3DGizmoPlugin: materials, lines and handles, _set_handle with undo, and registering via an EditorPlugin."
sources: ["https://docs.godotengine.org/en/stable/tutorials/plugins/editor/3d_gizmos.html", "https://docs.godotengine.org/en/stable/classes/class_editornode3dgizmoplugin.html", "https://docs.godotengine.org/en/stable/classes/class_editornode3dgizmo.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 3D gizmo plugins

**Goal:** a custom node (spawn area, trigger radius, patrol path) shows and edits its shape in the 3D
viewport.

## Plugin registration
```gdscript
# addons/spawn_area/plugin.gd
@tool
extends EditorPlugin
var gizmo := preload("res://addons/spawn_area/spawn_gizmo.gd").new()
func _enter_tree() -> void: add_node_3d_gizmo_plugin(gizmo)
func _exit_tree() -> void: remove_node_3d_gizmo_plugin(gizmo)
```

## Gizmo plugin
```gdscript
@tool
extends EditorNode3DGizmoPlugin
func _init() -> void:
    create_material("lines", Color(0.2, 0.9, 0.4))
    create_handle_material("handles")
func _get_gizmo_name() -> String: return "SpawnArea"
func _has_gizmo(node: Node3D) -> bool: return node is SpawnArea

func _redraw(g: EditorNode3DGizmo) -> void:
    g.clear()
    var n := g.get_node_3d() as SpawnArea
    var lines := PackedVector3Array()
    for i in 32:
        var a := TAU * i / 32.0; var b := TAU * (i + 1) / 32.0
        lines.append(Vector3(cos(a), 0, sin(a)) * n.radius); lines.append(Vector3(cos(b), 0, sin(b)) * n.radius)
    g.add_lines(lines, get_material("lines", g))
    g.add_handles(PackedVector3Array([Vector3(n.radius, 0, 0)]), get_material("handles", g), [])

func _get_handle_value(g, id, secondary) -> Variant: return g.get_node_3d().radius
func _set_handle(g, id, secondary, camera: Camera3D, screen_pos: Vector2) -> void:
    var n := g.get_node_3d() as SpawnArea
    var from := camera.project_ray_origin(screen_pos); var dir := camera.project_ray_normal(screen_pos)
    var plane := Plane(n.global_basis.y, n.global_position)
    var hit = plane.intersects_ray(from, dir)
    if hit != null: n.radius = maxf(0.1, n.to_local(hit).length()); n.update_gizmos()
func _commit_handle(g, id, secondary, restore, cancel: bool) -> void:
    var n := g.get_node_3d() as SpawnArea
    if cancel: n.radius = restore; return
    var ur := EditorInterface.get_editor_undo_redo()
    ur.create_action("Change spawn radius")
    ur.add_do_property(n, "radius", n.radius); ur.add_undo_property(n, "radius", restore)
    ur.commit_action()
```
The node's `radius` setter should call `update_gizmos()` so Inspector edits redraw too.

## Other drawing calls
`add_mesh`, `add_unscaled_billboard`, `add_collision_segments`/`add_collision_triangles`, `create_icon_material`.

## Gotchas
- Keep `_has_gizmo` cheap.
- Add collision segments or triangles (`add_collision_segments`, `add_collision_triangles`) so the gizmo can be clicked.

## Verify
- [ ] Dragging the handle changes the value, Ctrl+Z restores it, and the shape redraws on Inspector edits.

## Checked

2026-10-28. Confirmed against: EditorNode3DGizmoPlugin and EditorNode3DGizmo references (create_material, create_handle_material, _get_gizmo_name, _has_gizmo, _redraw, _get_handle_value, _set_handle, _commit_handle, get_material, add_lines, add_handles, add_mesh, add_unscaled_billboard, add_collision_segments, add_collision_triangles, get_node_3d, clear, create_icon_material), EditorPlugin add/remove_node_3d_gizmo_plugin, Node3D.update_gizmos, EditorInterface.get_editor_undo_redo.

Removed or rewritten: the local-space and scale statement and the cost claim for _has_gizmo.

Method: documentation only; no commands were run.
