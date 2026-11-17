---
id: computing-software.software-engineering.fsharp.nullable-references
name: nullable-references
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, nullable-references, fsharp-interop, nullness-checking, option-ofobj]
level: advanced
status: draft
description: "Handle null from .NET with isNull, Option.ofObj, Nullable, and enable F# nullness checking where supported."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Null and nullness
**Goal:** keep null out of F# code.

```fsharp
let name : string = null                       // allowed only for .NET types
let safe = Option.ofObj name                   // None
let len = match name with null -> 0 | s -> s.Length
let nn = if isNull name then "n/a" else name
let nb = System.Nullable<int>(5)
let opt = Option.ofNullable nb
let back = Option.toNullable (Some 3)
let n2 = Nullable 7
if nb.HasValue then nb.Value else 0
```
- F# types (records, unions, F# classes) do not admit `null` unless `[<AllowNullLiteral>]`.
- `.NET` reference types accept `null`; wrap at the boundary.
- F# 9 introduces opt-in nullness checking (`<Nullable>enable</Nullable>` in the project, `string | null` syntax) aligned with C# nullable references; unconfirmed details, check the F# 9 what's-new page for your SDK.
- `Unchecked.defaultof<'T>` yields null/zero without a check; avoid it.

## Gotchas
- `match x with null -> ..` requires `x` to be a null-admitting type.
- `Option.ofObj` on a string treats empty string as `Some ""`.

## Self-check
`Option.ofObj (null: string)` is `None`.
