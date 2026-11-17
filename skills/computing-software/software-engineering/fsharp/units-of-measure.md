---
id: computing-software.software-engineering.fsharp.units-of-measure
name: units-of-measure
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, units-of-measure, fsharp-generics, measure-types, dimensional-analysis]
level: advanced
status: docs-checked
description: "Annotate numeric values with compile-time units, define derived units and conversion constants."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/units-of-measure
  - https://github.com/dotnet/fsharp/blob/main/src/FSharp.Core/prim-types.fsi
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Units of measure
**Goal:** catch dimension errors at compile time with zero runtime cost.

```fsharp
[<Measure>] type m
[<Measure>] type s
[<Measure>] type km

let distance = 100.0<m>
let time = 9.58<s>
let speed = distance / time               // float<m/s>
// let bad = distance + time              // compile error

let kmToM (x: float<km>) = x * 1000.0<m/km>
let strip = float distance                // erase unit: float
let withU = LanguagePrimitives.FloatWithMeasure<m> 5.0

type Money<[<Measure>] 'u> = { Value: decimal<'u> }
```
- Units apply to floating point, signed integer and decimal types, and are erased at compile time.
- Generic over units with `[<Measure>] 'u` parameters.
- Use `float x` to drop units; `LanguagePrimitives.FloatWithMeasure` adds them to a runtime value.
- Units are lost at run time: `printf` expects dimensionless values, and a `ToString` cannot print the unit.
- Pass dimensioned values to functions that expect plain floats by cancelling the units or converting with `float`.

## Self-check
`distance / time` has type `float<m/s>`; adding it to `distance` fails to compile.

## Checked
2026-11-02. Confirmed against Learn "Units of measure": measure declarations, derived units, float, signed integer and decimal support, generic units, erasure at run time, printf needing dimensionless values and the float conversion. LanguagePrimitives.FloatWithMeasure confirmed in FSharp.Core prim-types.fsi. Removed: the reflection and serialisation claim and the .NET API compatibility claim (not on the page).
Method: documentation only; no commands were run.
