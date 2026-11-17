---
id: computing-software.software-engineering.fsharp.numeric-literals
name: numeric-literals
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, numeric-literals, fsharp-basics, int-suffixes, conversion-functions]
level: intro
status: docs-checked
description: "Write F# numeric literals with suffixes and convert explicitly with int, int64, float, decimal."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/tour
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric literals and explicit conversion
**Goal:** pick the right literal type and convert deliberately.

```fsharp
let a = 42          // int (int32)
let b = 42L         // int64
let c = 42u         // uint32
let d = 42uy        // byte
let e = 3.14        // float (double)
let f = 3.14f       // float32
let g = 3.14M       // decimal
let h = 100I        // bigint
let hex = 0xFF      // 255
let bin = 0b1010    // 10
let big = 1_000_000 // underscores allowed
let x = float a + e // explicit: int -> float
let n = int 3.9     // 3 (truncates)
```
- Convert explicitly with the conversion functions `int`, `int64`, `uint32`, `byte`, `float`, `float32`, `decimal`; see the Casting and conversions page.

## Gotchas
- Opening `Microsoft.FSharp.Core.Operators.Checked` replaces the arithmetic operators and conversions with overflow-checking versions (FSharp.Core Operators.Checked reference).

## Self-check
`int 3.9` is 3 and `0xFF` is 255.

## Checked
2026-11-03. Confirmed against the Literals page (suffixes, hex and binary prefixes, underscores), the Casting and conversions page and the FSharp.Core Operators.Checked reference. Removed: the no-implicit-widening and F# 6 method-call claims, silent wraparound and OverflowException naming, integer-division and NaN gotchas.
Method: documentation only; no commands were run.
