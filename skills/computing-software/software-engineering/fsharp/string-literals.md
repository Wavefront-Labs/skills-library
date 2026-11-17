---
id: computing-software.software-engineering.fsharp.string-literals
name: string-literals
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, string-literals, fsharp-basics, interpolated-strings, verbatim-strings]
level: intro
status: docs-checked
description: "Choose between regular, verbatim, triple-quoted and interpolated F# strings and format values inside them."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/tour
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String literals and interpolation
**Goal:** write strings without escape pain.

```fsharp
let regular  = "line1\nline2 \"quoted\""
let verbatim = @"dir\sub\file.txt" // backslashes literal; "" for a quote
let triple   = """He said "hi" """         // quotes need no escaping
let name = "Ada"
let age = 36
let s1 = $"Hello {name}, age {age}"
let s2 = $"Pi is {System.Math.PI:N4}"      // .NET format specifier after colon
let s3 = $"{age,5}|{name,-6}|"             // alignment
let s4 = $"%d{age} years"                  // printf-style typed hole
let s5 = $"literal {{braces}}"             // doubled braces
```
- Interpolated strings accept .NET format strings after `:` (for example `{x:N3}`) and printf-style typed holes such as `%d{x}`.
- Verbatim `@"..."` strings ignore escape sequences except `""` for a quote; `$@"..."` combines interpolation and verbatim.
- Beginning with F# 8, `$$"""..."""` extended interpolation lets text contain literal `{` `}` without escaping; the number of `$` is the number of braces that open a hole.

## Gotchas
- Single braces cannot appear literally in a `$"..."` string; double them (`{{` `}}`).

## Self-check
`$"{1+1}"` is `"2"`; `$"A pair of braces: {{}}"` gives `A pair of braces: {}`.

## Checked
2026-11-03. Confirmed against the Interpolated strings page (typed holes, {{ }} escaping, N format specifier, alignment with a comma, verbatim and triple-quote forms, F# 8 extended interpolation) and the Strings page. Removed: the F2 specifier example (page shows N3/N4), the colon-parentheses gotcha, the F# 5 version claim and the indexing/slicing claim.
Method: documentation only; no commands were run.
