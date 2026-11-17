---
id: computing-software.software-engineering.fsharp.voption-valueoption
name: voption-valueoption
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, voption-valueoption, fsharp-option-result, voption, struct-option]
level: advanced
status: docs-checked
description: "Use voption and ValueSome in hot paths to avoid option allocations, and know when it is not worth it."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/value-options
  - https://github.com/dotnet/fsharp/blob/main/src/FSharp.Core/option.fsi
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ValueOption
**Goal:** allocation-free optional values.

```fsharp
let tryDiv a b : int voption = if b = 0 then ValueNone else ValueSome (a / b)
match tryDiv 10 2 with
| ValueSome q -> printfn "%d" q
| ValueNone -> ()
let o = Some 1 |> Option.toValueOption      // conversion from option
```
- `ValueOption<'T>` is a struct discriminated union with `ValueSome` and `ValueNone`; it has structural equality and comparison.
- The `ValueOption` module offers functionality equivalent to the `Option` module, with a few name differences (for example `defaultValueArg`).
- A struct adds the cost of copying; weigh that against the performance benefit in your scenario.

## Self-check
`tryDiv 10 0` returns `ValueNone`.

## Checked
2026-11-02. Confirmed against Learn "Value Options": struct discriminated union, ValueSome and ValueNone, structural equality and comparison, the defaultValueArg name difference, the TryParse-style conversion and the copy-cost trade-off. Option.toValueOption confirmed in FSharp.Core option.fsi. Removed: the small-payload and mixed-pipeline advice, the ValueOption module function names (voption.fsi was not readable at the path tried), the struct active pattern example and the BenchmarkDotNet self-check.
Method: documentation only; no commands were run.
