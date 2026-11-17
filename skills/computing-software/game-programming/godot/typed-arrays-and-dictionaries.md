---
id: computing-software.game-programming.godot.typed-arrays-and-dictionaries
name: typed-arrays-and-dictionaries
category: computing-software
field: game-programming
product: godot
tags: [godot, gdscript, typed-array, typed-dictionary, packed-arrays, game-programming]
level: practitioner
status: verified
description: "Use GDScript typed arrays and typed dictionaries (4.4+), packed arrays for bulk data, and avoid the conversion, assignment and export pitfalls between them."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#typed-arrays", "https://docs.godotengine.org/en/stable/classes/class_dictionary.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typed arrays and typed dictionaries

**Goal:** collections that catch type errors early, autocomplete well and run faster.

## Typed arrays
```gdscript
var enemies: Array[Enemy] = []
@export var spawn_points: Array[Marker2D]
var ids: Array[int] = [1, 2, 3]
enemies.append(Enemy.new())     # OK
enemies.append("x")             # runtime error (and static error when inferable)
```
- Element type checked on insert. Typed loops give typed variables: `for e in enemies: e.attack()`
  autocompletes.
- Assigning an untyped `Array` to a typed variable errors at runtime unless the content matches and
  you convert: `var typed: Array[int] = Array(untyped, TYPE_INT, "", null)` or `typed.assign(untyped)`.
- Return types: `func get_targets() -> Array[Node3D]:`.
- `get_children()` returns `Array[Node]` (run: `is_typed()` true, builtin type `TYPE_OBJECT`); some other engine methods
  still return untyped `Array`; `assign()` into typed vars.

## Typed dictionaries (Godot 4.4+)
```gdscript
var stock: Dictionary[StringName, int] = {&"wood": 10}
@export var loot_weights: Dictionary[ItemData, float]
```
Keys and values type-checked; exported typed dictionaries get proper inspector editors.

## Packed arrays
`PackedFloat32Array`, `PackedVector2Array`, `PackedInt32Array`, `PackedByteArray`, `PackedStringArray`:
contiguous memory, much smaller and faster for large numeric data (meshes, heightmaps, nav points).
Per the class reference they are **always passed by reference** (like `Array`); use `duplicate()` for an independent
copy (run: `var y := x; y.append(2)` changed `x` too). The exception is built-in properties and methods, which return a
copy: `polygon.polygon.append(v)` on a `Polygon2D` changed nothing, so modify the returned array and assign it back. A
packed array in your own script variable (`obj.points.append(p)`) is changed in place.

## Performance notes
- Packed arrays store raw elements contiguously (no per-element Variant); measure before assuming a speedup for your use.

## Gotchas
- `Array[int]` and `PackedInt32Array` are different types; conversion with `PackedInt32Array(arr)`.
- Nested typed collections (`Array[Array[int]]`) are not supported: parse error "Nested typed collections are not
  supported." (`Array[Array]` is allowed); use classes or packed rows.
- `duplicate()` keeps the type; `duplicate(true)` deep copies (both ran and stayed typed).

## Verify
- [ ] Static typing warnings enabled (Project Settings > Debug > GDScript, UNTYPED_DECLARATION) show
  no untyped collections in gameplay code.
## Checked
Ran on Godot 4.7.2 headless: `assign()` and `Array(untyped, TYPE_INT, "", null)` conversions; typed dictionary `Dictionary[StringName, int]` with `is_typed_key()`; `PackedInt32Array(arr)` conversion; the aliasing and property-copy runs described above; wrong-type `append` error; nested typed array parse error. Pass-by-reference text from the 4.7.2 `PackedByteArray` and `Array` class references; typed dictionaries since 4.4 from the GDScript reference.
