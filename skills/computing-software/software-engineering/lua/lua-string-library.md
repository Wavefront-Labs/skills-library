---
id: computing-software.software-engineering.lua.lua-string-library
name: lua-string-library
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-strings, string-library]
level: practitioner
status: docs-checked
description: "Use the string library with 1-based indices, negative indices and byte-oriented behaviour."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# string.format, sub, find, rep and byte semantics
- Strings are immutable sequences of bytes and may contain embedded zeros; `#s` is the byte length. `string.sub(s, i, j)` takes negative indices from the end: `s:sub(-3)` is the last three bytes.
- `string.format` follows C `sprintf` with the extra `%q`; `%s` converts a non-string argument like `tostring`; `%q` writes a value as a valid Lua constant. Width and precision are limited to two digits.
- Repeated `a = a .. x` builds a new string each time; collect pieces in a table and call `table.concat(t, ", ")` once.
- `s:rep(3, "-")`, `s:upper()`, `s:byte(1, -1)`, `string.char(72, 105)`.
- The `utf8` library provides `utf8.len`, `utf8.char`, `utf8.codepoint`, `utf8.codes` and `utf8.offset`.
Verify: `#"é"` is 2 in a UTF-8 source file.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: section 2.1 (immutable byte strings, embedded zeros), string.sub (negative indices), string.format, string.rep, string.byte, string.char, table.concat, utf8 library. Removed: the O(n^2) cost claim for concatenation loops (the manual does not state it; the copying advice is kept as practice).
Method: documentation only; no commands were run.
