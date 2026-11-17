---
id: computing-software.software-engineering.fsharp.match-expressions
name: match-expressions
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, match-expressions, fsharp-matching, pattern-guards, as-patterns]
level: intro
status: docs-checked
description: "Use F# match with constant, tuple, list, record, or and as patterns plus when guards, and keep matches exhaustive."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/match-expressions
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/pattern-matching
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# match expressions
**Goal:** express branching by shape.

```fsharp
let describe xs =
    match xs with
    | []                -> "empty"
    | [ x ]             -> $"one: {x}"
    | [ x; y ]          -> $"two: {x},{y}"
    | head :: _ when head > 100 -> "big head"
    | all & (_ :: _ :: _ as rest) -> $"many, tail {rest.Length}"   // & and as patterns
    | _                 -> "other"

let classify (a, b) =
    match a, b with
    | 0, _ | _, 0 -> "has zero"          // or-pattern
    | x, y when x = y -> "equal"
    | _ -> "different"

let isNum = function :? int | :? float -> true | _ -> false   // type tests on obj
```
- Patterns include constants, identifiers, wildcards, tuples, lists, `::`, records, union cases, type tests (`:?`), `as`, OR (`|`) and AND (`&`) patterns.
- Rules are tried from top to bottom, and patterns apply left to right.
- A constant pattern can use a defined literal identifier.
- A lowercase identifier in a pattern is a variable binding, not a comparison with an outer value.

## Self-check
`describe [1;2]` returns `"two: 1,2"`.

## Checked
2026-11-02. Confirmed against Learn "Pattern matching" (the supported patterns table: constant, literal identifier, OR, AND, as, tuple, list, record, type test, variable and wildcard, applied in order from top to bottom; the wildcard `_` matches any previously unmatched input) and "Match expressions". Removed: MatchFailureException, the FS0025 instruction and the claim that when guards are ignored for exhaustiveness (not on the pages read).
Method: documentation only; no commands were run.
