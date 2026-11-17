---
id: computing-software.software-engineering.fsharp.array-module
name: array-module
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, array-module, fsharp-lists-arrays, array-slicing, mutable-arrays]
level: practitioner
status: docs-checked
description: "Create and mutate .NET arrays in F# and use slicing and the Array module including parallel variants."
sources:
  - https://fsharp.github.io/fsharp-core-docs/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arrays
**Goal:** use fixed-size mutable arrays for performance.

```fsharp
let a = [| 1; 2; 3; 4; 5 |]
a.[0] <- 10                       // mutable element
let b = Array.zeroCreate<int> 8   // zero-initialised
let c = Array.init 5 (fun i -> i * i)
let slice = a.[1..3]              // [|2;3;4|]
let tail = a.[2..]
let head = a.[..1]
let m = Array2D.init 3 3 (fun i j -> i * j)   // 2D array
let sorted = Array.sort a         // new array
Array.sortInPlace a
let total = a |> Array.sumBy float
Array.blit a 0 b 0 3
a |> Array.iteri (fun i x -> printfn "%d:%d" i x)
```
- `Array.zeroCreate` initialises every element to the zero value for the element type.
- Out-of-range slice bounds produce an empty array rather than an exception (see the Slices page).
- The `Array.Parallel` module holds parallel computations on arrays; it is not available when targeting .NET Framework before 4.
- `Array2D`, `Array3D` and `Array4D` modules handle higher-rank arrays.

## Gotchas
- `Array.sort` copies; `sortInPlace` mutates.

## Self-check
`Array.init 3 id` is `[|0;1;2|]`.

## Checked
2026-11-03. Confirmed against the Arrays language-reference page (zeroCreate, init, Array2D, Array.Parallel module) and the FSharp.Core ArrayModule reference (sort, sortInPlace, blit, iteri, sumBy) and the Slices page (empty slice on out-of-range bounds). Removed: the Array.Parallel.map call, the structural-equality claim, the copy-on-slice claim, the IndexOutOfRangeException claim and the null-element claim.
Method: documentation only; no commands were run.
