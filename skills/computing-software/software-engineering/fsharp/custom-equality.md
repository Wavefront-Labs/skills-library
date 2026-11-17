---
id: computing-software.software-engineering.fsharp.custom-equality
name: custom-equality
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, custom-equality, fsharp-generics, structural-equality, custom-comparison]
level: advanced
status: draft
description: "Control structural equality and comparison on F# types with attributes and custom overrides."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Equality and comparison
**Goal:** know the defaults and change them safely.

```fsharp
// Records and unions: structural equality + comparison by default.
type P = { X: int; Y: int }
{ X = 1; Y = 2 } = { X = 1; Y = 2 }          // true

[<ReferenceEquality>]
type Node = { Id: int; mutable Next: Node option }

[<CustomEquality; NoComparison>]
type Ci =
    | Ci of string
    override this.Equals(o) =
        match o with
        | :? Ci as other ->
            let (Ci a), (Ci b) = this, other
            System.String.Equals(a, b, System.StringComparison.OrdinalIgnoreCase)
        | _ -> false
    override this.GetHashCode() = (let (Ci a) = this in a.ToUpperInvariant().GetHashCode())

[<NoEquality; NoComparison>]
type Handler = { Run: unit -> unit }
```
- Attributes: `[<ReferenceEquality>]`, `[<CustomEquality>]`, `[<NoEquality>]`, `[<CustomComparison>]`, `[<NoComparison>]`, `[<StructuralEquality>]`, `[<StructuralComparison>]`.
- Types containing functions are not equatable/comparable; the constraint failure appears when you use them in `Set`, `Map`, `=`.
- Custom equality requires overriding both `Equals` and `GetHashCode`.

## Gotchas
- `=` on floats uses IEEE semantics (nan <> nan) but `Set`/`hash` treat values differently; avoid float keys.
- Custom comparison needs `IComparable` implementation.

## Self-check
Use the case-insensitive type as a Set element and confirm `Ci "A"` and `Ci "a"` collapse.
