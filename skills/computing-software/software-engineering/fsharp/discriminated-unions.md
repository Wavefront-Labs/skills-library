---
id: computing-software.software-engineering.fsharp.discriminated-unions
name: discriminated-unions
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, discriminated-unions, fsharp-unions, sum-types, make-illegal-states-unrepresentable]
level: intro
status: docs-checked
description: "Model alternatives with F# discriminated unions, with fields, recursion and exhaustive matching."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/discriminated-unions
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/pattern-matching
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Discriminated unions
**Goal:** encode "one of several shapes" so illegal states cannot be built.

```fsharp
type Shape =
    | Circle of radius: float
    | Rectangle of width: float * height: float
    | Point

let area = function
    | Circle r -> System.Math.PI * r * r
    | Rectangle (w, h) -> w * h
    | Point -> 0.0

type Tree<'a> =
    | Leaf
    | Node of Tree<'a> * 'a * Tree<'a>

let rec size = function Leaf -> 0 | Node (l, _, r) -> size l + 1 + size r
```
- Cases take named or unnamed fields; construct with `Circle 2.0`.
- The patterns in a `match` should cover all possible values; a `_` wildcard pattern matches any input not matched earlier.
- Often a simpler alternative to a small object hierarchy.
- Mutually recursive unions link with `and`.

## Gotchas
- Adding a case leaves any `match` that omits it incomplete; add a rule for it.

## Self-check
Add a case and check that every `match` has a rule for it.

## Checked
2026-11-02. Confirmed against Learn "Discriminated unions" and "Pattern matching": named and unnamed fields, construction, recursive unions (Tree example), mutually recursive unions with `and`, and the union as an alternative to small object hierarchies. Removed: structural equality (not on the pages), the incomplete-match wildcard advice (pages say only that patterns should cover all matches and `_` catches unmatched input), warning code FS0025, the --warnaserror advice and the tail-recursion gotcha (not on the pages read).
Method: documentation only; no commands were run.
