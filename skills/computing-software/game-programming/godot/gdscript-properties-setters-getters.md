---
id: computing-software.game-programming.godot.gdscript-properties-setters-getters
name: gdscript-properties-setters-getters
category: computing-software
field: game-programming
product: godot
tags: [godot, gdscript, gdscript-setget, property-setter, exported-setter, game-programming]
level: practitioner
status: verified
description: "Write GDScript 2.0 properties with set/get blocks: backing fields, setters firing in the editor via @tool, @export with setters, and avoiding recursion and ready-order bugs."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#properties-setters-and-getters", "https://docs.godotengine.org/en/stable/tutorials/plugins/running_code_in_the_editor.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GDScript properties with setters and getters

**Goal:** properties that validate, emit change signals and update visuals — without infinite
recursion or null-node errors.

## Syntax (Godot 4)
```gdscript
signal health_changed(value: int)
@export var max_health := 100
var health: int = 100:
    set(value):
        health = clampi(value, 0, max_health)   # assigning inside its own setter does NOT recurse
        health_changed.emit(health)
    get:
        return health
```
Named functions variant:
```gdscript
var speed: float = 5.0: set = set_speed, get = get_speed
func set_speed(v: float) -> void: speed = maxf(v, 0.0)
```
Inside the setter, assigning to the property writes the backing value directly. Assigning from
anywhere else in the class (`health = 5`) **does** call the setter (unlike Godot 3's `self.` rule).

## Exported properties with setters and node access
Setters for `@export` vars run when the scene loads — **before `_ready`**, so `$Sprite` may be null (run: a scene whose
`.tscn` stores `tint = Color(1, 0, 0, 1)` called the setter with `is_node_ready()` false, `is_inside_tree()` false and no
`Sprite2D` child yet):
```gdscript
@export var tint := Color.WHITE:
    set(value):
        tint = value
        if is_node_ready(): $Sprite2D.modulate = tint
func _ready(): $Sprite2D.modulate = tint
```
Or `if not is_inside_tree(): await ready`.

## Editor updates
With `@tool`, setters run in the editor when the inspector changes them — handy for previews. Guard
gameplay-only code with `if Engine.is_editor_hint(): return`. Call `notify_property_list_changed()` if
a setter changes which properties are visible.

## Gotchas
- Mutating a container in place (`items.append(x)`) does not call the setter — reassign or emit
  manually.
- Getters run on every read; keep them cheap.
- Static typing in setters: `set(value: int)` is allowed and enforced.

## Verify
- [ ] Setting health from code and from the inspector both emit `health_changed`.
- [ ] Scene loads with no null-instance errors from setters.
## Checked
Ran on Godot 4.7.2 headless: `health = 500` inside the class goes through the setter and `clampi` with no recursion; the named-function form `set = set_speed, get = get_speed`; `items2.append(1)` on a property with a setter does not call the setter; a scene-stored `@export` value triggers the setter before the tree exists (see above). The `@tool` setter behaviour, `Engine.is_editor_hint()` and `notify_property_list_changed()` are from the Godot docs pages "Running code in the editor" and "GDScript exports" (the editor was not opened).
