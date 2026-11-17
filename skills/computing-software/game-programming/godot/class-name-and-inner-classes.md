---
id: computing-software.game-programming.godot.class-name-and-inner-classes
name: class-name-and-inner-classes
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, class_name, inner-classes, global-classes, script-classes, game-programming]
level: intro
status: verified
description: "Use class_name for global script types and editor icons, inner classes for small helpers, preload-based script constants, and the trade-offs of global class registration."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#classes", "https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#inner-classes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# class_name and inner classes

**Goal:** organise GDScript types so they are typed, discoverable in the editor and don't clutter the
global namespace.

## class_name
```gdscript
@icon("res://icons/enemy.svg")
class_name Enemy
extends CharacterBody2D
```
- Registers `Enemy` globally: usable as a type (`var e: Enemy`), `Enemy.new()`, `is Enemy`, and appears in the
  Create Node dialog (and for Resources, in the inspector's New Resource list).
- Static functions and constants become globally reachable: `MathUtil.remap(...)`.
- Names must be unique across the project (including addons); prefix addon classes. With two scripts declaring
  `class_name Dupe`, the global class cache (`.godot/global_script_class_cache.cfg`) listed it once.
- Global classes are cached in `.godot/global_script_class_cache.cfg`; if a class "isn't found",
  re-save the script or restart the editor.

## Without class_name
```gdscript
const Bullet := preload("res://weapons/bullet.gd")      # local alias, typed
var b: Bullet = Bullet.new()
```
Use for internal helpers that shouldn't appear in the Create dialog.

## Inner classes
```gdscript
class_name Inventory extends Resource

class Slot:
    var item: ItemData
    var count := 0
    func is_empty() -> bool: return count == 0

var slots: Array[Slot] = []
func _init(size := 20) -> void:
    for i in size: slots.append(Slot.new())
```
- Inner classes extend `RefCounted` by default (auto-freed; run: `Inventory.Slot.new().get_class()` is `RefCounted`), can
  `extends` anything (an inner `class Child extends Node` instantiates as a Node), and are accessed externally as `Inventory.Slot`.
- Inner classes can't be exported to the inspector or saved as Resources on their own; promote them to
  `class_name` Resources if they need saving/editing.

## Inheritance
`extends "res://base_enemy.gd"` or `extends BaseEnemy`. Call parent with `super()` / `super.method()` (run:
`super.hi()` returned the parent's value). Override virtuals by name (GDScript has no override keyword).
Abstract classes: `@abstract` (Godot 4.5+) prevents instancing a base class: `AbBase.new()` is a parse error
"Cannot construct abstract class", though `load("res://ab.gd").new()` through a dynamic script reference still returned an instance.

## Gotchas
- `class_name` scripts load at project start for type registration; huge numbers can slow editor startup.
- Cyclic `class_name` references work in Godot 4 but `preload` cycles can still fail; prefer class_name
  types over cyclic preloads.

## Verify
- [ ] No duplicate class_name errors after adding addons.
- [ ] Helpers not meant for the Create dialog aren't registered globally.
## Checked
Ran on Godot 4.7.2 headless: `class_name` types usable as `Enemy`-style types and in `.new()`; inner class `Slot` and `Child extends Node`; `super.method()`; `@abstract class_name AbBase` static and dynamic construction; global class cache file exists at `.godot/global_script_class_cache.cfg` and lists a duplicated name once; `@icon` and `@export_range` annotations parse. `@abstract` since 4.5 from the GDScript reference ("Since Godot 4.5, you can define abstract classes"). `preload` cycles and editor startup cost statements were removed as unverified.
