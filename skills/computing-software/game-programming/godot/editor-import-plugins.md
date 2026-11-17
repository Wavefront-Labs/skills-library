---
id: computing-software.game-programming.godot.editor-import-plugins
name: editor-import-plugins
category: computing-software
field: game-programming
product: godot
tags: [godot, gdextension, editorimportplugin, custom-importer, asset-import, game-programming]
level: practitioner
status: docs-checked
description: "Write Godot EditorImportPlugin importers for custom file formats: recognized extensions, import options, presets, saving resources to .godot/imported and reimport behaviour."
sources: ["https://docs.godotengine.org/en/stable/tutorials/plugins/editor/import_plugins.html", "https://docs.godotengine.org/en/stable/classes/class_editorimportplugin.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Editor import plugins

**Goal:** designers drop a custom file (level `.ldtk`, dialogue `.yarn`, CSV item table) into the
project and Godot turns it into a usable Resource automatically, with options in the Import dock.

## Plugin skeleton
```gdscript
# addons/items_importer/plugin.gd
@tool
extends EditorPlugin
var importer
func _enter_tree(): importer = preload("importer.gd").new(); add_import_plugin(importer)
func _exit_tree(): remove_import_plugin(importer); importer = null
```
```gdscript
# addons/items_importer/importer.gd
@tool
extends EditorImportPlugin
func _get_importer_name(): return "studio.items_csv"
func _get_visible_name(): return "Item Table"
func _get_recognized_extensions(): return ["items"]
func _get_save_extension(): return "res"
func _get_resource_type(): return "Resource"
func _get_priority(): return 1.0
func _get_import_order(): return 0
func _get_preset_count(): return 1
func _get_preset_name(i): return "Default"
func _get_import_options(path, preset): return [{"name": "id_column", "default_value": 0}]
func _get_option_visibility(path, option, options): return true
func _import(source_file, save_path, options, platform_variants, gen_files):
    var f := FileAccess.open(source_file, FileAccess.READ)
    if f == null: return FileAccess.get_open_error()
    var table := ItemTable.new()          # your custom Resource
    while not f.eof_reached():
        var row := f.get_csv_line()
        if row.size() > 1: table.add_row(row, options.id_column)
    return ResourceSaver.save(table, "%s.%s" % [save_path, _get_save_extension()])
```

## How import works
- The source file stays in `res://` and the editor imports it with your plugin, saving the result with the save extension you return. Check the import plugin tutorial for where Godot stores import metadata and output in your version.
- `load("res://data/weapons.items")` then returns the imported resource.

## Tips
- Return proper `Error` codes so failures show in the editor.
- `gen_files` lets you report additional generated files; `append_import_external_resource` imports
  referenced files (textures) first.
- For formats that should become scenes, use `_get_resource_type() = "PackedScene"` and save a packed
  scene, or an `EditorScenePostImportPlugin` for scene post-processing instead.

## Gotchas
- Override `_get_format_version` and bump it when importer logic changes, so existing imports are redone.
- Choose a unique importer name (`_get_importer_name`).

## Verify
- [ ] Dropping a new `.items` file creates a loadable resource without manual steps.
- [ ] A clean clone reproduces the imports.

## Checked

2026-10-28. Confirmed against: EditorImportPlugin class reference (_get_importer_name, _get_recognized_extensions, _get_save_extension, _get_resource_type, _get_priority, _get_import_order, _get_preset_count, _get_option_visibility, _get_format_version, append_import_external_resource, _import signature with gen_files) and the import plugins tutorial.

Removed or rewritten: claims about the .import sidecar and .godot/imported folder (the tutorial text predates the 4.x layout), what to commit, export filtering, plugin enablement per team member, the headless import CI command and the renaming-orphans warning.

Method: documentation only; no commands were run.
