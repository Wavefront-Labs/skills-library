---
id: computing-software.software-engineering.fsharp.let-immutability
name: let-immutability
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, let-immutability, fsharp-bindings, shadowing, value-bindings]
level: intro
status: draft
description: "Bind values with let, shadow names in inner scopes, and understand why F# bindings are immutable by default."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/tour
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# let bindings and shadowing
**Goal:** write bindings the idiomatic way.

```fsharp
let x = 5
// x <- 6              // error: x is not mutable
let f () =
    let y = 1
    let y = y + 1      // shadowing inside a function body is allowed
    y
let a, b = 1, "two"    // tuple pattern binding
let private helper = 1
let inline sq x = x * x
let use1 () =
    use r = new System.IO.StringReader("hi")   // disposed at end of scope
    r.ReadToEnd()
```
- `let` binds a value or function; the binding is immutable, though the object it refers to may be mutable.
- Shadowing is allowed in function and expression scopes.
- `use` replaces `let` for `IDisposable` values.
- `let rec ... and ...` for mutually recursive bindings.

## Gotchas
- A duplicate top-level `let x` in a compiled module is an error (duplicate definition); scripts (.fsx) and FSI accept it.
- Shadowing hides, never mutates: closures captured earlier keep the old value.
- Incomplete pattern bindings such as `let (Some v) = opt` give warning FS0025 and can throw MatchFailureException.

## Self-check
Write a function that shadows a parameter; confirm an earlier closure still sees the old value.
