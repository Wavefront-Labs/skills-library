---
id: computing-software.game-programming.godot.editor-plugins-and-custom-docks
name: editor-plugins-and-custom-docks
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdextension, editorplugin, plugin-cfg, custom-dock, add-custom-type, editor-tooling, game-programming]
level: practitioner
status: docs-checked
description: "Build a Godot 4 EditorPlugin: plugin.cfg, @tool scripts, adding docks and toolbar buttons, custom node types, undo/redo, and enabling it per project."
sources: ["https://docs.godotengine.org/en/stable/tutorials/plugins/editor/making_plugins.html", "https://docs.godotengine.org/en/stable/classes/class_editorplugin.html", "https://docs.godotengine.org/en/stable/classes/class_editorundoredomanager.html", "https://docs.godotengine.org/en/stable/classes/class_editorinterface.html", "https://docs.godotengine.org/en/stable/classes/class_editordock.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Editor plugins and custom docks

**Goal:** add project-specific tooling to the Godot editor (a level-tools dock, a "bake spawn points"
button) as a reusable addon.

## Layout
```
addons/level_tools/
  plugin.cfg
  plugin.gd
  dock.tscn
```
`plugin.cfg`:
```ini
[plugin]
name="Level Tools"
description="Spawn point baking and checks"
author="Studio"
version="1.0"
script="plugin.gd"
```
Project > Project Settings > Plugins > enable. Plugins are ordinary folders; copy them between projects.

## plugin.gd
```gdscript
@tool
extends EditorPlugin

var dock: EditorDock

func _enter_tree() -> void:
    var content := preload("res://addons/level_tools/dock.tscn").instantiate()
    content.get_node("BakeButton").pressed.connect(_on_bake)
    dock = EditorDock.new()
    dock.title = "Level Tools"
    dock.default_slot = DOCK_SLOT_RIGHT_UL
    dock.add_child(content)
    add_dock(dock)
    add_tool_menu_item("Validate level", _validate)

func _exit_tree() -> void:
    remove_dock(dock)
    dock.queue_free()
    remove_tool_menu_item("Validate level")

func _on_bake() -> void:
    var root := EditorInterface.get_edited_scene_root()
    if root == null: return
    var ur := get_undo_redo()
    ur.create_action("Bake spawn points")
    for marker in root.find_children("*", "Marker3D"):
        ur.add_do_property(marker, "position", marker.position.snapped(Vector3.ONE))
        ur.add_undo_property(marker, "position", marker.position)
    ur.commit_action()

func _validate() -> void:
    print("validating...")
```
- The EditorPlugin script must be `@tool` and inherit EditorPlugin; any other GDScript the plugin uses
  must also be `@tool` (a script without it acts like an empty file in the editor).
- Initialize in `_enter_tree()` and clean up in `_exit_tree()`, mirroring each other.
- `add_control_to_dock()` and `remove_control_from_docks()` are deprecated in 4.7 in favour of
  `add_dock()` with an `EditorDock` and `remove_dock()`; on earlier 4.x use the older calls (version of the
  introduction of EditorDock not checked here).
- Use `EditorUndoRedoManager` (via `get_undo_redo()`) for any scene modification so Ctrl+Z works and
  the scene is marked unsaved.

## Other hooks
- `add_custom_type("Spawner", "Node3D", preload("spawner.gd"), preload("icon.svg"))` adds a node to
  the Create dialog.
- `_has_main_screen()` + `_make_visible()` + `_get_plugin_name()` for a main-screen tab (like 2D/3D/Script).
- `_handles(object)`, `_edit(object)`, `_forward_3d_gui_input(camera, event)` to draw/handle input in
  the viewport for a selected node type.
- `add_inspector_plugin`, `add_import_plugin`, `add_export_plugin` for those extension points.
- `EditorInterface.get_selection()` returns the EditorSelection.

## Gotchas
- `EditorInterface` is a singleton accessed by its name (class page: do not instantiate it).

## Verify
- [ ] Enable/disable the plugin repeatedly: no duplicate docks, no errors in Output.
- [ ] Bake action undoes with Ctrl+Z and marks the scene modified.

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from the Making plugins tutorial and the EditorPlugin, EditorInterface, EditorDock and EditorUndoRedoManager class pages: plugin.cfg, @tool requirements, _enter_tree/_exit_tree, add_dock/remove_dock with EditorDock.title/default_slot, add_tool_menu_item, create_action/add_do_property/add_undo_property/commit_action, get_edited_scene_root and get_selection on the EditorInterface singleton, main-screen and viewport virtuals, add_inspector/import/export_plugin. Fixed: add_control_to_dock and remove_control_from_docks are deprecated in the 4.7 docs; example rewritten with EditorDock. Removed: editor-crash claim, toggle-off-on advice, 4.2+ singleton gate.
Method: documentation only; no commands were run.
