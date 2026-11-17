---
id: computing-software.software-engineering.fsharp.active-patterns
name: active-patterns
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, active-patterns, fsharp-matching, partial-active-pattern, multi-case-active-pattern]
level: advanced
status: docs-checked
description: "Define complete, partial and parameterised F# active patterns to give matches custom decomposition."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active patterns
**Goal:** put domain parsing in the pattern itself.

```fsharp
let (|Even|Odd|) n = if n % 2 = 0 then Even else Odd          // complete

let (|Integer|_|) (str: string) =                               // partial: returns option
    let mutable intvalue = 0
    if System.Int32.TryParse(str, &intvalue) then Some(intvalue)
    else None

[<return: Struct>]
let (|Int|_|) str =                                            // struct partial pattern
    match System.Int32.TryParse(str) with
    | (true, n) -> ValueSome n
    | _ -> ValueNone
```
- Complete patterns name up to seven partitions (the choice type is limited to n <= 7).
- Partial patterns end with `|_|` and can return `option`, `voption` or `bool`.
- By default a partial pattern returning `option` allocates; use `[<return: Struct>]` with `ValueSome`/`ValueNone` to avoid it.
- Parameterised active patterns take extra arguments before the matched value to specialise a general pattern.

## Gotchas
- Complete patterns are limited to seven cases.

## Self-check
`match "12" with Integer n -> n | _ -> 0` returns 12.
## Checked
2026-11-02. Confirmed against Microsoft Learn "Active Patterns": seven-case limit, partial patterns, voption/Struct form, parameterised patterns, and the two code shapes. Removed: the exhaustiveness and cost notes, the `Prefix` pattern and the F# 6 version tag.
Method: documentation only; no commands were run.
