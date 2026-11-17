---
id: computing-software.software-engineering.fsharp.struct-types
name: struct-types
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, struct-types, fsharp-struct-memory, struct-attribute, readonly-struct]
level: advanced
status: docs-checked
description: "Declare struct types, readonly structs and understand copy semantics and when structs help performance."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Struct types
**Goal:** use value types for small, short-lived data.

```fsharp
[<Struct>]
type V2 = { X: float; Y: float }                 // struct record

[<IsReadOnly; Struct>]
type P(x: int, y: int) =
    member _.X = x
    member _.Y = y

[<Struct>]
type Cell =
    val mutable Value: int
    new(v) = { Value = v }

[<Struct>]
type Opt = | A | B of int                          // struct union
let v = { X = 1.; Y = 2. }
```
- Structs are value types with pass-by-value semantics; they suit small aggregates that are copied often.
- `IsReadOnly` does not imply `Struct`; add both attributes.
- Structs cannot take part in inheritance, cannot contain `let` or `do` bindings and cannot recursively contain themselves.
- Records and discriminated unions can also be structs with `[<Struct>]`.

## Gotchas
- Structs cannot use `let` bindings; use `val` fields and explicit constructors as shown.

## Self-check
Check that every struct example carries `[<Struct>]` (or `struct ... end`), and `IsReadOnly` types carry both attributes.

## Checked
2026-11-03. Confirmed against the Structures language-reference page (value-type semantics, StructAttribute, IsReadOnly needing Struct, restrictions, struct records and unions) and the Discriminated unions page. Removed: defensive-copy, struct tuple and voption, default-constructor, boxing and BenchmarkDotNet claims.
Method: documentation only; no commands were run.
