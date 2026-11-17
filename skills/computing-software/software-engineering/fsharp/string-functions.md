---
id: computing-software.software-engineering.fsharp.string-functions
name: string-functions
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, string-functions, fsharp-formatting, string-module, split-join]
level: intro
status: draft
description: "Process text using the String module and System.String methods: split, join, trim, replace, contains, and culture-safe comparisons."
sources:
  - https://fsharp.github.io/fsharp-core-docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# String functions
**Goal:** manipulate strings with the right culture semantics.

```fsharp
String.concat ", " ["a";"b"]               // "a, b"
String.length "abc"
"a,b,,c".Split(',')                        // [|"a";"b";"";"c"|]
"a,b,,c".Split([|','|], System.StringSplitOptions.RemoveEmptyEntries)
"  hi ".Trim()
"abc".Contains "b"
"Hello".Replace("l", "L")
String.replicate 3 "ab"
"abc" |> Seq.rev |> System.String.Concat   // "cba"
System.String.IsNullOrWhiteSpace "  "
"abc".StartsWith("A", System.StringComparison.OrdinalIgnoreCase)
"straße".ToUpperInvariant()
"x".PadLeft(3, '0')
let parts = "k=v".Split('=') |> Array.map (fun s -> s.Trim())
String.forall System.Char.IsDigit "123"
```
- FSharp.Core String module: `concat`, `length`, `replicate`, `collect`, `map`, `filter`, `exists`, `forall`, `init`, `iter`. Newer versions (8+) add `String.isNullOrEmpty`/`isNullOrWhiteSpace` (unconfirmed exact version).
- Prefer ordinal or invariant comparisons for identifiers; pass `StringComparison` explicitly.
- Build large strings with `System.Text.StringBuilder`, not repeated `+`.

## Gotchas
- `s.Split(",")` with a string overload is available on .NET Core 2.0+; framework builds need char arrays.
- Culture-sensitive methods (`ToUpper()`) behave differently under Turkish culture.

## Self-check
`"a,,b".Split(',').Length` is 3.
