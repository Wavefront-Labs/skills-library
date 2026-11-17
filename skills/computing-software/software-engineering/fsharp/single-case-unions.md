---
id: computing-software.software-engineering.fsharp.single-case-unions
name: single-case-unions
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, single-case-unions, fsharp-unions, struct-unions, require-qualified-access]
level: practitioner
status: docs-checked
description: "Wrap primitives in single-case unions, mark unions Struct or RequireQualifiedAccess, and keep constructors private for validation."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single-case, struct and qualified unions
**Goal:** get typed IDs and validated values.

```fsharp
type UserId = UserId of int
type OrderId = OrderId of int
let (UserId raw) = UserId 5           // unwrap by pattern

type Email = private Email of string
module Email =
    let create (s: string) =
        if s.Contains "@" then Ok (Email s) else Error "invalid email"
    let value (Email s) = s

[<Struct>]
type Result2 = | Good of v: int | Bad of e: string   // struct union

[<RequireQualifiedAccess>]
type Color = Red | Green | Blue
let c = Color.Red                      // Red alone no longer resolves
```
- A private constructor plus a smart-constructor module enforces invariants.
- Before F# 9, struct unions needed unique case field names; F# 9 lifts that limit (Discriminated unions page).
- `[<RequireQualifiedAccess>]` forces case names to be qualified with the union name.

## Gotchas
- Struct unions are copied as value types.

## Self-check
`UserId 1 = OrderId 1` does not compile (different types).

## Checked
2026-11-03. Confirmed against the Discriminated unions page (single-case syntax, RequireQualifiedAccess, struct unions, unique-name rule before F# 9, value-type copy semantics). Removed: the size-versus-reference and serialisation gotchas, the Option.None example and the pattern-only-inside-module claim.
Method: documentation only; no commands were run.
