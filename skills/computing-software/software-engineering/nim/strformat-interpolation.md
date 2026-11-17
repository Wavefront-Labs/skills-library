---
id: computing-software.software-engineering.nim.strformat-interpolation
name: strformat-interpolation
category: computing-software
field: software-engineering
product: nim
tags: [strformat-interpolation, string-formatting, strformat, fmt, string-interpolation, format-spec, alignment, precision, nim]
level: intro
status: docs-checked
description: "Interpolate expressions with fmt and & literals, apply format specs for width, precision, alignment and bases."
sources:
  - https://nim-lang.org/docs/strformat.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fmt and &: string interpolation

Goal: format output readably.

- `import std/strformat`. `&"x = {x}"` and `fmt"x = {x}"` interpolate arbitrary expressions in braces; `fmt` is a raw string literal so backslashes are literal, and `&` processes escapes (`&"a\n{b}"`).
- Format spec after a colon: `{x:5}` width, `{x:<8}` left, `{x:>8}` right, `{x:^8}` center, `{x:08.3f}` zero-pad float, `{n:x}` hex, `{n:b}` binary, `{s:*^20}` fill char (the fill must be followed by an alignment flag), `{n:#x}` for a `0x` prefix.
- Debug form: `{x=}` prints `x=value`.
- Literal braces: `{{` and `}}`; use `fmt"{{x}}"`.
- To format custom types add `proc formatValue(result: var string, value: T, specifier: string)`.

Gotchas:
- Inside a `{...}` expression, braces must be escaped with a backslash; use triple-quoted strings (`fmt"""..."""`) when the expression contains quotes.
- `fmt"{msg}\n"` keeps a literal backslash-n because the literal is raw; use `&` or `{'\n'}`.

Verify: `fmt"{3.14159:.2f}"` gives 3.14.

## Checked

2026-11-03. Confirmed against the strformat page: `&` versus `fmt` (raw literal), the standard format spec grammar `[[fill]align][sign][#][0][minimumwidth][.precision][type]`, align flags, type letters b d o x X, `{x=}` debug form, `{{` escape, formatValue signature, `.2f` precision. Removed: the unsupported `{n:,}` item, the compile-time speed claim, the `$` requirement and the ffDecimal gotcha (none are on the page).

Method: documentation only; no commands were run.
