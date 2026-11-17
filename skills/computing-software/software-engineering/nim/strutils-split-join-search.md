---
id: computing-software.software-engineering.nim.strutils-split-join-search
name: strutils-split-join-search
category: computing-software
field: software-engineering
product: nim
tags: [strutils-split-join-search, stdlib-strutils-text, strutils, split, join, strip, replace, find, startswith, contains, parseint, nim]
level: intro
status: docs-checked
description: "Manipulate text with split, join, strip, find, replace, startsWith, contains, toLower and parse functions."
sources:
  - https://nim-lang.org/docs/strutils.html
  - https://nim-lang.org/docs/parseutils.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# strutils: split, join, strip, search and replace

Goal: everyday string processing.

- `import std/strutils`. Split: `"a,b".split(',')`, `splitWhitespace`, `splitLines`, `rsplit`, `split(sep, maxsplit)`.
- Join: `@["a","b"].join(", ")`. Trim: `strip()`, `strip(chars={'x'})`, `strip(leading=false)` (parameters `leading`, `trailing`, `chars`; default strips whitespace).
- Search: `find`, `rfind`, `contains`, `startsWith`, `endsWith`, `count`, `s.replace("a","b")`, `multiReplace`.
- Case/shape: `toLowerAscii`, `toUpperAscii`, `capitalizeAscii`, `align`, `alignLeft`, `repeat`, `indent`, `dedent`, `center`.
- Parse: `parseInt`, `parseFloat`, `parseBool`, `parseHexInt`, `parseEnum[T]` (raise `ValueError` for invalid input); `std/parseutils` has `parseInt(s, var n)` style procs that return the number of characters consumed. `parseBool` accepts `y, yes, true, 1, on` and `n, no, false, 0, off`; `parseEnum` compares style-insensitively (first letter case-sensitive).
- For string interpolation the docs point to the `strformat` module.

Gotchas:
- `"a,,b".split(',')` yields three items, including the empty field.

Verify: `"  x ".strip()` is "x".

## Checked

2026-11-02. Confirmed against lib/pure/strutils.nim (every listed proc exists; `strip` signature; `ValueError` on `parseFloat`, `parseHexInt`, `parseEnum`; `parseBool` words) and lib/pure/parseutils.nim. Removed: the `%`-is-legacy claim, `-Ascii` unicode gotcha, `tryParse` helpers (not found).
Method: documentation only; no commands were run.
