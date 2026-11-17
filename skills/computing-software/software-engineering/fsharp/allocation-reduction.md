---
id: computing-software.software-engineering.fsharp.allocation-reduction
name: allocation-reduction
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, allocation-reduction, fsharp-perf-code, arraypool, allocation-free]
level: advanced
status: draft
description: "Reduce GC pressure in F# using struct tuples, voption, Span, ArrayPool and avoiding intermediate collections."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Allocation reduction
**Goal:** cut garbage in hot paths.

```fsharp
open System.Buffers

// struct tuple + voption instead of tuple + option
let tryParse (s: string) : int voption = ValueNone

// reuse buffers
let process (n: int) =
    let buf = ArrayPool<byte>.Shared.Rent n
    try
        // ... use buf.AsSpan(0, n)
        ()
    finally
        ArrayPool<byte>.Shared.Return buf

// avoid intermediate lists
let sumSquares (xs: int[]) =
    let mutable acc = 0
    for x in xs do acc <- acc + x * x
    acc
```
- Chains such as `xs |> List.map f |> List.filter g` allocate an intermediate list per stage; use arrays, `Seq` fused with care, or a loop in the measured hot path.
- Closures allocate; `inline` and `[<InlineIfLambda>]` remove them.
- `[<Struct>]` records/unions and `ValueOption` avoid heap objects for small values.
- String concatenation in loops: use `StringBuilder` or `String.Create`/spans.
- Prove changes with BenchmarkDotNet's Allocated column.

## Gotchas
- Premature struct use can slow code through copying.
- `Return` buffers exactly once; do not use after return.

## Self-check
Benchmark `sumSquares` against a `List` pipeline and compare allocated bytes.
