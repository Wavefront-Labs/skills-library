---
id: computing-software.software-engineering.fsharp.printf-format
name: printf-format
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, printf-format, fsharp-formatting, sprintf, format-specifiers]
level: intro
status: docs-checked
description: "Print and format values with printf, printfn, sprintf and failwithf using typed format specifiers including %A."
sources:
  - https://fsharp.github.io/fsharp-core-docs/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# printf family
**Goal:** format output with compile-time type checking.

```fsharp
printfn "Hello %s, you are %d" "Ada" 36
let s = sprintf "%5.2f|%-8s|%08d|%x|%b" 3.14159 "ab" 42 255 true
eprintfn "error: %s" "oops"
printfn "%A" [ 1; 2; 3 ]                      // pretty print structured values
printfn "%O" (System.DateTime.UtcNow)         // calls ToString()
printfn "%c %i %u %e %g" 'x' 5 5u 1234.5 0.0001
let n = 3
printfn $"interpolated {n}"
```
- Placeholders have the form `%[flags][width][.precision][type]`.
- Types: `%s` string, `%d`/`%i` ints, `%u` unsigned, `%f` floats, `%e`, `%g`, `%x`/`%X` hex, `%o` octal, `%B` binary, `%b` bool, `%c` char, `%O` ToString, `%A` structured text, `%M` decimal, `%%` literal percent.
- Flags: `0` zero pad, `-` left justify, `+` plus sign, space for a sign column; a width of `*` takes the width from an extra argument; the `#` flag is a compile error.
- Values are formatted with invariant culture.

## Gotchas
- Mismatched argument types are compile errors, for example `sprintf "Hello %s" (2+2)`.
- `%A` default print width is 80.

## Self-check
`sprintf "%05.1f" 3.14159` is `"003.1"`.

## Checked
2026-11-03. Confirmed against the Plain text formatting page (specifier table, flags, width *, invariant culture, # flag error, %A width 80, type mismatch error) and the Interpolated strings page. Removed: the StringWriter/fprintf example, the anonymous-record %A example, Printf.StringFormat, the partial-application claim, the float-with-%d claim and the %A slowness claim.
Method: documentation only; no commands were run.
