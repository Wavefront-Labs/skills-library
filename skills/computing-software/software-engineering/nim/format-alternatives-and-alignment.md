---
id: computing-software.software-engineering.nim.format-alternatives-and-alignment
name: format-alternatives-and-alignment
category: computing-software
field: software-engineering
product: nim
tags: [format-alternatives-and-alignment, string-formatting, format, formatfloat, align, columns, percent-format, formatsize, table-output, nim]
level: practitioner
status: docs-checked
description: "Align columns with align/alignLeft/formatFloat and understand strutils.format and % for older code."
sources:
  - https://nim-lang.org/docs/strutils.html
  - https://nim-lang.org/docs/strformat.html
  - https://nim-lang.org/docs/terminal.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table-style output and legacy format

Goal: produce aligned tables and read old code.

- `import std/strutils`: `align("7", 5)`, `alignLeft("ab", 6)`, `formatFloat(x, ffDecimal, 2)`, `insertSep(n.intToStr, ',')` for thousands separators (signature `insertSep(s, sep = '_', digits = 3)`), `intToStr(n, 4)` pads zeros, `toHex`, `toBin`.
- `formatSize(bytes)` (std/strutils) gives "1.5MiB"; `formatEng` for engineering notation.
- Legacy: `"$1 is $2" % [a, b]` and `format("$name", ...)`; found in older code, still valid.
- For tables compute column widths first via `max` of lengths, then `alignLeft` each cell, or use `fmt` alignment flags such as `{name:<12}`.
- Terminal colours: `std/terminal`'s `styledEcho`, `setForegroundColor`.

Gotchas:
- `formatSize(bytes)` takes an `int64` and by default uses IEC prefixes (`bpIEC`).

Verify: columns line up with mixed-length names.

## Checked

2026-11-03. Confirmed against the strutils, strformat and terminal pages: align, alignLeft, formatFloat, insertSep(s, sep, digits), intToStr, formatSize(bytes, decimalSep, prefix = bpIEC, includeSpace), formatEng, toHex, toBin, `%` and format, styledEcho, setForegroundColor, fmt alignment flags. Removed: the nested-width `{name:<{w}}` form (not in the strformat grammar), float round-trip and Unicode-width claims.

Method: documentation only; no commands were run.
