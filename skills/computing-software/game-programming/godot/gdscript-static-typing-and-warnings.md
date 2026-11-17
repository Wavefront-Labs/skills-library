---
id: computing-software.game-programming.godot.gdscript-static-typing-and-warnings
name: gdscript-static-typing-and-warnings
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, gdscript-static-typing, type-hints, warnings, untyped-declaration, game-programming]
level: practitioner
status: verified
description: "Use GDScript 4 static typing: type hints, inference with :=, typed arrays and dictionaries, casting with as/is, and the warning settings that enforce types project-wide."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/warning_system.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GDScript static typing and warnings

**Goal:** catch mistakes in the editor, get full autocompletion, and get faster code (typed
instructions are optimised by the VM).

## Syntax
```gdscript
var speed: float = 300.0
var dir := Vector2.ZERO                       # inferred (Vector2)
const MAX_HP: int = 100
var enemies: Array[Enemy] = []                # typed array
var scores: Dictionary[String, int] = {}      # typed dictionary (Godot 4.4+)
@onready var sprite: Sprite2D = $Sprite2D

func damage(amount: int, source: Node = null) -> bool:
    return amount > 0

func _physics_process(delta: float) -> void:
    pass
```
- `:=` infers from the right side and is a parse error when the right side is Variant: `var v := d["k"]` on a
  Dictionary fails with "Cannot infer the type of "v" variable because the value doesn't have a set type". Use an
  explicit type there. `var s := $Sprite2D` is accepted but infers `Node`, not `Sprite2D`; write
  `var sprite: Sprite2D = $Sprite2D` or `$Sprite2D as Sprite2D` to get the real type.
- Casting: `var e := body as Enemy` (null if not an Enemy); check with `if body is Enemy:`.
- Typed arrays reject wrong element types at runtime. `Array[Enemy].assign(untyped)` to convert. A typed parameter
  (`func f(a: Array[int])`) accepts an array literal (`f([1, 2])` ran) but a variable holding an untyped array fails with
  "The array of argument 1 (Array) does not have the same element type as the expected typed array argument".

## Safe lines
The script editor turns the line number green on lines the analyser can prove type-safe (the docs' "Safe lines"
section; casting such as `($Timer as Timer)` makes a node lookup safe). Aim for green in hot code. Typed code also uses
optimised opcodes (the docs' static typing page).

## Enforce with warnings
Project Settings > Debug > GDScript (enable Advanced Settings):
- `untyped_declaration` -> Warn or Error: every variable/parameter/return needs a type.
- `inferred_declaration` (if your style forbids `:=`).
- `unsafe_property_access`, `unsafe_method_access`, `unsafe_cast`, `unsafe_call_argument` -> Warn.
- `return_value_discarded`, `unused_parameter` (prefix with `_` to silence), `shadowed_variable`.
- `@warning_ignore("unsafe_method_access")` on a line/function for justified exceptions.
- Third-party addons: `debug/gdscript/warnings/directory_rules` (default `{ "res://addons": 0 }`, 0 = exclude) so addons
  don't flood warnings; include your own addons individually.

## Gotchas
- `null` is allowed for Object types but not for value types (`int`, `Vector2`); use sentinel values.
- Typed `Array[T]` parameters reject a variable that holds an untyped array; convert it with `assign` first.

## Verify
- [ ] Project opens with zero GDScript warnings under the chosen strictness.
- [ ] Hot scripts show green (safe) line numbers.
## Checked
Ran on Godot 4.7.2 headless: `Array[int]` and `Dictionary[StringName, int]` declarations; `append("x")` on an `Array[int]` logs "Attempted to push_back a variable of type 'String' into a TypedArray of type 'int'" and leaves the array unchanged; `:=` with `$Sprite2D` parses, `:=` with `d["k"]` and `var i: int = null` are parse errors; `@warning_ignore("unsafe_method_access")` annotation parses; the project settings list contains `untyped_declaration`, `inferred_declaration`, `unsafe_property_access`, `unsafe_method_access`, `unsafe_cast`, `unsafe_call_argument`, `return_value_discarded`, `unused_parameter` and `shadowed_variable` under `debug/gdscript/warnings/`; typed dictionaries "added in 4.4" from the GDScript reference; `directory_rules` default and description from the 4.7.2 `ProjectSettings` class reference. The Project Settings menu path ("Advanced Settings") is editor UI and was not opened.
