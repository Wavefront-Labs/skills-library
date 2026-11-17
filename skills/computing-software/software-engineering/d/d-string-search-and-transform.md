---
id: computing-software.software-engineering.d.d-string-search-and-transform
name: d-string-search-and-transform
category: computing-software
field: software-engineering
product: d
tags: [d-string-search-and-transform, std-string, indexof, strip, chomp, chop, toupper, tolower, capitalize, leftjustify, translate, tr, wrap, linesplitter, d]
level: intro
status: docs-checked
description: "Search and transform strings with indexOf, lastIndexOf, count, strip/chomp/chop, toLower, toUpper, capitalize, leftJustify, center, translate, tr, and wrap."
sources:
  - https://dlang.org/phobos/std_string.html
  - https://dlang.org/phobos/std_uni.html
  - https://dlang.org/phobos/std_array.html
  - https://dlang.org/phobos/std_ascii.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std.string: indexOf, strip, split, toUpper, replace, format helpers

Goal: everyday text handling.

- Search: `indexOf(s, "x")` returns `ptrdiff_t` (an index in code units; -1 when missing; optional `CaseSensitive.no`), `lastIndexOf`, `indexOfAny`; `count`, `startsWith`, `endsWith`, `canFind` come from std.algorithm.
- Trim: `strip`, `stripLeft`, `stripRight`, `chomp`, `chop`.
- Case: `toLower`, `toUpper` (std.uni, also reachable through std.string), `asUpperCase` (lazy), `capitalize` (first character up, rest lowercased), `icmp`.
- Layout: `leftJustify(s, 10)`, `rightJustify`, `center`, `wrap(s, columns)`, `outdent`, `detab`/`entab`, `lineSplitter` (lazy), `splitLines` (array), `representation`.
- Replace: `replace(s, a, b)` (std.array), `translate`, `tr(str, from, to)`.
- C strings: `toStringz`, `fromStringz`; `isNumeric` checks that a string is a number.
- Character tests: `std.ascii.isDigit`, `isAlpha`; `std.uni.isAlpha` for Unicode.

Gotchas:
- `indexOf` returns code-unit offsets, not code-point counts.

Verify: unittest on strings with ASCII, accents, and empty input.

## Checked

2026-11-03. Confirmed against: std.string, std.uni, std.array and std.ascii reference pages.

Removed because the pages read did not confirm it: `munch` and `removechars` (not on the pages), `center` justify claim kept (appears on page), the 'toUpper allocates' claim, `capitalize` Unicode remark.

Method: documentation only; no commands were run.
