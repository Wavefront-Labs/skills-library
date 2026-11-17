---
id: computing-software.software-engineering.fsharp.slicing-ranges
name: slicing-ranges
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, slicing-ranges, fsharp-lists-arrays, range-expressions, string-slicing]
level: practitioner
status: docs-checked
description: "Use range expressions, indexer slicing on strings, lists and arrays, and custom GetSlice members."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ranges and slicing
**Goal:** slice collections and strings safely.

```fsharp
let s = "hello world"
s.[0..4]                 // "hello"
s.[6..]                  // "world"
s.[..4]                  // "hello"
let xs = [ 10; 20; 30; 40 ]
xs.[1..2]                // [20;30]
[ 1 .. 10 ]
[ 10 .. -2 .. 0 ]        // descending
[ 'a' .. 'e' ]
[ 1.0 .. 0.5 .. 3.0 ]
seq { 1 .. 1000000 } |> Seq.sum

type Grid() =
    member _.GetSlice(lo: int option, hi: int option) =
        defaultArg lo 0, defaultArg hi 0
```
- Custom types support slicing by defining a `GetSlice` method (see the Slices page).

## Gotchas
- A slice whose bounds cannot produce elements yields an empty collection rather than throwing; the Slices page explains this design.

## Self-check
`s.[0..4]` on `"hello world"` is `"hello"`.

## Checked
2026-11-03. Confirmed against the Slices language-reference page (slice syntax on lists, arrays and strings, empty slices, GetSlice) and the Sequences page for ranges. Removed: the inclusive-bounds, `xs[1..2]` version claim, float rounding, O(n) list slicing and array-copy claims.
Method: documentation only; no commands were run.
