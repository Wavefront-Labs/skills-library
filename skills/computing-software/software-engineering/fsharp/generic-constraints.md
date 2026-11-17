---
id: computing-software.software-engineering.fsharp.generic-constraints
name: generic-constraints
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, generic-constraints, fsharp-generics, automatic-generalization, type-constraints]
level: practitioner
status: docs-checked
description: "Write generic F# code with automatic generalisation, explicit type parameters and where constraints."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generics and constraints
**Goal:** write reusable typed code.

```fsharp
let swap (a, b) = (b, a)                    // automatically generic: 'a * 'b -> 'b * 'a
let idf<'T> (x: 'T) : 'T = x               // explicit type parameter
let maxOf<'T when 'T : comparison> (a: 'T) b = if a > b then a else b
let makeNew<'T when 'T : (new : unit -> 'T)> () = new 'T()
let print<'T when 'T :> System.IComparable> (x: 'T) = x.CompareTo x
let isNull2<'T when 'T : null> (x: 'T) = isNull x
let hashAll<'T when 'T : equality> (xs: 'T list) = xs |> List.distinct

type Stack<'T>() =
    let items = System.Collections.Generic.List<'T>()
    member _.Push x = items.Add x
    member _.Pop() = let v = items.[items.Count-1] in items.RemoveAt(items.Count-1); v

let s = Stack<int>()
let wild = System.Collections.Generic.List<_>()   // _ lets inference fill the argument
```
- Constraints: `equality`, `comparison`, `struct`, `not struct`, `null`, `:> Type`, `(new : unit -> 'T)`, `unmanaged`, `enum<_>`, `delegate<_,_>`.
- F# generalises automatically when the code does not depend on a concrete type; the two arguments of a function like `max` must have the same type.
- Flexible types written `#Type` accept subtypes (see the Flexible Types page).

## Gotchas
- Value restriction: only complete function definitions and simple immutable values are generalised. Fix it with a type annotation, by making the value a function with an extra unit parameter, or with explicit type parameters (`let arrayOf10Lists<'T> = Array.create 10 ([]: 'T list)`).

## Self-check
`maxOf 1 2` and `maxOf "a" "b"` both compile.

## Checked
2026-11-03. Confirmed against the Automatic Generalization page (generic max, same-type requirement, value restriction fixes), the Generics page and the Flexible Types page, and the Constraints page. Removed: the FS0030 code, the higher-kinded-type claim and the annotation advice.
Method: documentation only; no commands were run.
