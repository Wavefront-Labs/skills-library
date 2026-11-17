---
id: computing-software.software-engineering.fsharp.ce-builders
name: ce-builders
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, ce-builders, fsharp-ce, computation-expressions, monad-builder]
level: advanced
status: draft
description: "Define a computation expression builder with Bind, Return, ReturnFrom, Zero and Delay for let!, return and use!."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom computation expression builder
**Goal:** write a builder and know which method each keyword calls.

```fsharp
type MaybeBuilder() =
    member _.Bind(x, f) = Option.bind f x          // let!
    member _.Return(x) = Some x                     // return
    member _.ReturnFrom(x) = x                      // return!
    member _.Zero() = None                          // if without else
    member _.Combine(a, b) = match a with Some _ -> a | None -> b()
    member _.Delay(f) = f ()
    member _.TryWith(body, handler) = try body () with e -> handler e

let maybe = MaybeBuilder()

let r =
    maybe {
        let! a = Some 1
        let! b = Some 2
        return a + b
    }                                                // Some 3
```
- Mapping: `let!` to Bind, `return` to Return, `return!` to ReturnFrom, `use!` to Using + Bind, `yield` to Yield, `for` to For, `while` to While, `try/with` to TryWith, `try/finally` to TryFinally.
- Implement only what you use; unsupported constructs give a compile error naming the missing member.
- `and!` (F# 5+) needs `MergeSources` on the builder (or BindN overloads in newer versions; unconfirmed).
- Custom operations use `[<CustomOperation("name")>]`.

## Gotchas
- Delay/Run semantics matter for laziness; if Delay forces immediately, effects run at construction.
- Write builder members as methods on a class; module functions cannot serve.

## Self-check
`maybe { let! a = None in return a }` is `None`.
