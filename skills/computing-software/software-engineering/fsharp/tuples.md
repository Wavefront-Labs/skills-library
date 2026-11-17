---
id: computing-software.software-engineering.fsharp.tuples
name: tuples
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, tuples, fsharp-tuples-records, struct-tuples, fst-snd]
level: intro
status: docs-checked
description: "Create, destructure and compare F# tuples, and use struct tuples to avoid allocation."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/tuples
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/value-options
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Tuples
**Goal:** return and pass several values without a named type.

```fsharp
let pair = (1, "one")
let a, b = pair                  // destructure
let first = fst pair             // fst/snd work on reference 2-tuples only
let triple = 1, 2.0, "x"
let (x, _, z) = triple
let st = struct (1, 2)           // struct tuple (System.ValueTuple)
let struct (p, q) = st
let divmod a b = a / b, a % b
let q, r = divmod 17 5

// interop: a TryParse-style call returns its out value as a tuple
let ok, n = System.Int32.TryParse "42"
```
- Tuples are reference tuples or struct tuples; struct tuples compile to `System.ValueTuple` and interoperate with C#.
- `fst` and `snd` work only on reference tuples.
- Struct tuples and reference tuples are not implicitly convertible; pattern match on one and construct the other.

## Self-check
`divmod 17 5 = (3, 2)`.

## Checked
2026-11-02. Confirmed against Learn "Tuples": reference and struct tuples, fst and snd on reference tuples only, struct tuples compiled to System.ValueTuple and interoperating with C#. The TryParse out-value tuple pattern is shown on the Value Options page. Removed: the structural equality and comparison claim, the 7-item Rest-nesting gotcha and a vague conversion bullet (not on the page).
Method: documentation only; no commands were run.
