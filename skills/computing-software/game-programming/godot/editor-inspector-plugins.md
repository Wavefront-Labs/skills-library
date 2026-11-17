---
id: computing-software.game-programming.godot.editor-inspector-plugins
name: editor-inspector-plugins
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdextension, editorinspectorplugin, editorproperty, inspector, custom-property-editor, game-programming]
level: advanced
status: docs-checked
description: "Customise Godot's Inspector with EditorInspectorPlugin and EditorProperty: custom editors for properties, extra buttons per object type, and correct undo."
sources: ["https://docs.godotengine.org/en/stable/tutorials/plugins/editor/inspector_plugins.html", "https://docs.godotengine.org/en/stable/classes/class_editorinspectorplugin.html", "https://docs.godotengine.org/en/stable/classes/class_editorproperty.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Editor inspector plugins

**Goal:** replace the default editor for a property (e.g. an int shown as a dice roller, a
`Vector2i` shown as a grid picker) or add buttons to an object's inspector.

## Registering
Inside an `EditorPlugin` (see godot editor-plugins-and-custom-docks):
```gdscript
@tool
extends EditorPlugin
var inspector_plugin := preload("res://addons/stat_editor/stat_inspector.gd").new()

func _enter_tree(): add_inspector_plugin(inspector_plugin)
func _exit_tree(): remove_inspector_plugin(inspector_plugin)
```

## The EditorInspectorPlugin
```gdscript
@tool
extends EditorInspectorPlugin
const StatProperty = preload("res://addons/stat_editor/stat_property.gd")

func _can_handle(object: Object) -> bool:
    return object is EnemyStats            # which objects this plugin sees

func _parse_begin(object: Object) -> void:
    var b := Button.new()
    b.text = "Roll random stats"
    b.pressed.connect(func(): object.randomize_stats())
    add_custom_control(b)                  # appears at the top of the inspector

func _parse_property(object, type, name, hint_type, hint_string, usage_flags, wide) -> bool:
    if type == TYPE_INT and name.ends_with("_stat"):
        add_property_editor(name, StatProperty.new())
        return true
    return false
```

## The EditorProperty
```gdscript
@tool
extends EditorProperty
var spin := SpinBox.new()
var updating := false

func _init():
    spin.min_value = 1; spin.max_value = 20
    add_child(spin)
    add_focusable(spin)
    spin.value_changed.connect(_on_changed)

func _on_changed(v: float) -> void:
    if updating: return
    emit_changed(get_edited_property(), int(v))

func _update_property() -> void:
    var v = get_edited_object()[get_edited_property()]
    updating = true
    spin.value = v
    updating = false
```
- Use `emit_changed` (not a manual signal emit) to report a new value from the editor; the class reference says not to emit the signal manually.
- `_update_property` refreshes the control from the edited object; guard against feedback loops with a flag.
- `set_bottom_editor(control)` places a control as a bottom editor.

## Gotchas
- Every script involved needs `@tool`.
- `_parse_property` is called for every property of a handled object; filter by name and type.
- Custom Resource subclasses also go through `_can_handle`; check `is` against the class_name.

## Verify
- [ ] Changing a value via the custom editor is undoable with Ctrl+Z.
- [ ] Undo updates the custom editor display.
- [ ] Other objects' inspectors are unaffected.

## Checked

2026-10-28. Confirmed against: EditorInspectorPlugin class reference (_can_handle, _parse_begin, _parse_property, add_custom_control, add_property_editor), EditorProperty reference (emit_changed, add_focusable, set_bottom_editor, _update_property, get_edited_object, get_edited_property) and EditorPlugin add_inspector_plugin.

Removed or rewritten: undo/redo behaviour claims for emit_changed, the semantics of returning true from _parse_property, and the usage_flags advice, which the fetched pages did not state.

Method: documentation only; no commands were run.
