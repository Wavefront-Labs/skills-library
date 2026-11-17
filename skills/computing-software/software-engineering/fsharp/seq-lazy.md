---
id: computing-software.software-engineering.fsharp.seq-lazy
name: seq-lazy
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, seq-lazy, fsharp-sequences-maps, seq-expression, lazy-sequences]
level: practitioner
status: docs-checked
description: "Use seq for lazy, possibly infinite pipelines, understand re-evaluation and cache or materialise when needed."
sources:
  - https://fsharp.github.io/fsharp-core-docs/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sequences
**Goal:** stream data lazily.

```fsharp
let nats = Seq.initInfinite id
let firstTen = nats |> Seq.filter (fun n -> n % 3 = 0) |> Seq.truncate 10 |> Seq.toList

let fib =
    Seq.unfold (fun (a, b) -> Some (a, (b, a + b))) (0I, 1I)

let s = seq { for i in 1 .. 3 do yield i * i }
let pairs = seq { for x in 1..2 do for y in 1..2 -> (x, y) }

let cached = nats |> Seq.take 5 |> Seq.cache         // evaluate once
Seq.chunkBySize 2 [1;2;3;4;5]
Seq.windowed 2 [1;2;3]
Seq.pairwise [1;2;3]
```
- `seq<'T>` is an alias for `IEnumerable<'T>` and is evaluated lazily.
- `Seq.toList` and `Seq.toArray` force evaluation; `Seq.cache` caches the elements.
- `Seq.take n` throws if the sequence has fewer than n elements; `Seq.truncate` does not.

## Gotchas
- `Seq.length` and `Seq.sort` consume the whole sequence; do not call them on infinite sequences.

## Self-check
`Seq.initInfinite id |> Seq.take 3 |> Seq.toList` is `[0;1;2]`.

## Checked
2026-11-03. Confirmed against the Sequences language-reference page (lazy evaluation, Seq.take throwing versus truncate, Seq.cache) and the FSharp.Core SeqModule reference (initInfinite, unfold, truncate, chunkBySize, windowed, pairwise, toList). Removed: the File.ReadLines example and its leak gotcha, and the re-enumeration claim.
Method: documentation only; no commands were run.
