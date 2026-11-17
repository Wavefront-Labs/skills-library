---
id: computing-software.software-engineering.fsharp.span-byref
name: span-byref
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, span-byref, fsharp-struct-memory, byref-returns, span-t]
level: advanced
status: draft
description: "Use Span, ReadOnlySpan and inref/outref/byref parameters in F# for allocation-free slicing and in-place updates."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Span and byrefs
**Goal:** work on memory without copying.

```fsharp
let sumSpan (s: System.ReadOnlySpan<int>) =
    let mutable acc = 0
    for i in 0 .. s.Length - 1 do acc <- acc + s.[i]
    acc

let arr = [| 1; 2; 3; 4 |]
let total = sumSpan (System.ReadOnlySpan(arr, 1, 3))
let sl = System.Span<int>(arr).Slice(0, 2)

let incr (x: byref<int>) = x <- x + 1
let mutable n = 1
incr &n                                   // pass address

let read (x: inref<int>) = x              // readonly byref
let tryGet (d: System.Collections.Generic.Dictionary<int,int>) k =
    let mutable v = 0
    if d.TryGetValue(k, &v) then Some v else None
```
- Span-like types are `IsByRefLike`: they cannot be captured in closures, stored in fields of normal types, or used across `async`/`task` boundaries.
- `&x` takes the address of a mutable local; `outref` pairs with .NET `out` parameters.
- Pattern `d.TryGetValue k` returning a tuple is the idiomatic shortcut.

## Gotchas
- Closure capture of a Span gives a compile error; hoist work into a non-lambda function.
- Mutable captured locals cannot be passed by address inside lambdas either.

## Self-check
Slice an array via ReadOnlySpan and confirm no allocation using MemoryDiagnoser.
