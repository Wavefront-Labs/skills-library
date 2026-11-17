---
id: computing-software.game-programming.godot.csharp-api-differences-and-marshalling
name: csharp-api-differences-and-marshalling
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, csharp, dotnet, variant-marshalling, godot-collections, garbage-collection, performance, game-programming, godot-collections-array]
level: advanced
status: docs-checked
description: "Know Godot C# API differences from GDScript (naming, signals, Mathf and GD, Variant conversions) and where native interop and marshalling cost performance."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_differences.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_variant.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_basics.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# C# API differences and marshalling costs

**Goal:** write C# that avoids interop and conversion traps.

## API differences
- PascalCase instead of snake_case: `GetNode<T>()`, `GlobalPosition`, `QueueFree()`, `_Ready()`.
- Math functions live in `Mathf` (`abs` is `Mathf.Abs`, `PI` is `Mathf.Pi`, `TAU` is `Mathf.Tau`); random and
  misc globals live in `GD` (`GD.Print`, `GD.RandRange`, `GD.VarToStr`). `System.Math` and `System.MathF`
  are also available.
- Only primitive types can be constants in C#: `Vector2.RIGHT` becomes the read-only property `Vector2.Right`.
- `is_instance_valid(obj)` becomes `GodotObject.IsInstanceValid(obj)`.
- `@onready` has no direct equivalent: assign the member in `_Ready()`.
- Declare signals with `[Signal]` on a delegate whose name ends in `EventHandler`; an event with the name
  minus the suffix is generated. Prefer the generated C# events over the `Signal` type.
- Await a signal with `await ToSignal(timer, Timer.SignalName.Timeout);`.

## Variant
- `Godot.Variant` represents Godot's Variant. The docs recommend avoiding it unless needed for untyped
  engine APIs, to keep C# type safety.
- Convert to Variant with implicit conversion, `Variant.CreateFrom(x)` or `Variant.From(x)`; convert back
  with an explicit cast, `Variant.As<T>()` or `AsInt32()` and similar. A mismatched conversion can return
  a similar value, the default, an empty array, or throw: convert to the correct type.
- `Variant.Obj` returns a boxed object for value types and runs a switch; prefer specific conversions.
- Variant is a struct and cannot be null; use `default` for a "null" Variant.
- Variant `Int` is C# `long` and `Float` is `double`. Collections from the `Godot.Collections` namespace
  are Variant-compatible.

## Interop cost
- Most properties of GodotObject-based classes (any Node) make native interop calls into the C++ core.
  Read such a property into a local variable and write it back once rather than reading and setting it
  repeatedly in a loop.
- Passing raw arrays or strings to the engine API requires marshalling, which is comparatively pricey.
  Implicit conversion from `string` to `NodePath` or `StringName` pays both interop and marshalling; use the
  generated `PropertyName`, `MethodName` and `SignalName` StringNames.
- Structs are copied: `Position.X = 100.0f` does not compile (CS1612); copy, modify and reassign.

## Verify
- [ ] Hot loops read engine properties once into locals.
- [ ] No string-to-StringName conversions inside per-frame code.

## Checked
2026-11-08. Read: C# differences page (naming, Mathf/GD, signals, onready, await/ToSignal, IsInstanceValid),
C# Variant page (conversions, Obj, null, type table start) and C# basics (interop, marshalling, CS1612).
Removed unconfirmed claims: `double delta` rule, collection element-access cost and `Span<T>` advice,
GC and LINQ allocation advice, object disposal behaviour, and "where C# wins" comparison.
Method: documentation only; no commands were run.
