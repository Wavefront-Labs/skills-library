---
id: computing-software.software-engineering.fsharp.hot-path-pitfalls
name: hot-path-pitfalls
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, hot-path-pitfalls, fsharp-perf-code, structural-equality-cost, boxing]
level: advanced
status: draft
description: "Avoid typical F# slowdowns: generic structural equality and comparison, boxing, big tuples, list indexing, and printf."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hot-path pitfalls
**Goal:** know what is slow before profiling.

- Generic `=` / `compare` on non-primitive types go through slow generic paths; for hot code use specialised comparers, `String.Equals(a, b, StringComparison.Ordinal)`, or `HashIdentity.Structural` only when needed.
- `Map`/`Set` are O(log n); prefer `Dictionary`/`HashSet` when no ordering or immutability is required.
- `list` indexing is O(n); `xs.[i]` in a loop is quadratic.
- `sprintf`/`printf` are slow (format parsing); use string interpolation or `String.Format`, or `StringBuilder` in hot code.
- Boxing: casting a value type to `obj` or `IComparable` allocates; generic constraints avoid it.
- `seq` pipelines add enumerator overhead; arrays and loops are faster for tight code.
- `Seq.length` re-enumerates; `List.length` is O(n).
- Exceptions are expensive; do not use them for control flow in loops (use `TryParse`).

```fsharp
// slow: quadratic
let sumBad (xs: int list) = [ for i in 0 .. xs.Length - 1 -> xs.[i] ] |> List.sum
// fast
let sumGood xs = List.sum xs
```

## Gotchas
- Generic inline equality on records of primitives is optimised by the compiler in many cases; only worry after profiling.
- Debug builds distort every number.

## Self-check
Benchmark `sprintf "%d" n` vs `string n` in a loop.
