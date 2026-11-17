---
id: computing-software.software-engineering.fsharp.comprehensions
name: comprehensions
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, comprehensions, fsharp-sequences-maps, list-comprehensions, yield-bang]
level: practitioner
status: docs-checked
description: "Generate collections with for, yield, yield bang and conditionals inside list, array and seq expressions."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collection comprehensions
**Goal:** construct collections declaratively.

```fsharp
let squares = [ for i in 1 .. 5 -> i * i ]
let sq = seq {
    for i in 1..10 do
        yield i * i }
let implicitYield = seq {
    for i in 1..10 do
        i * i }
let arr = [| 1; 2; 3 |]
let flat = seq { for _ in 1..10 do yield! seq { 1; 2; 3; 4; 5 } }   // yield! splices a sequence
```
- `->` is shorthand for `do yield` with a single expression; it does not work when a branch has no value (for example `if` without `else`), use `do` instead.
- In a sequence expression `yield` is optional in most cases: a bare expression is yielded implicitly.
- `yield!` includes a whole sequence inside another sequence.

## Gotchas
- With an `if` that has no `else` branch use `do` with `yield` (or an implicit yield), not `->`.

## Self-check
`[ for i in 1..3 -> i ] = [1;2;3]`.
## Checked
2026-11-02. Confirmed against Microsoft Learn "Lists", "Arrays" and "Sequences" (F# language reference): `->`, `do ... yield`, implicit yield, `yield!`. Removed: F# 4.7 version tag, `dict`/`Set`/`Map` construction, the tail-call and warning notes.
Method: documentation only; no commands were run.
