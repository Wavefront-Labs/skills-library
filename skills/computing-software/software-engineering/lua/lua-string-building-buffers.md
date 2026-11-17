---
id: computing-software.software-engineering.lua.lua-string-building-buffers
name: lua-string-building-buffers
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-bit-strings, string-building-buffers]
level: practitioner
status: docs-checked
description: "Build large strings efficiently without quadratic copying."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# table.concat buffers, string.rep and performance
- Collect pieces in `local buf = {}` and join them with `table.concat(buf, sep, i, j)` (all elements strings or numbers) instead of repeated `s = s .. x` in a loop.
- `string.rep(s, n, sep)` concatenates n copies of s separated by sep; it returns the empty string if n is not positive, so `("x"):rep(0)` is empty. A large n can exhaust memory.
- `string.format` gives complete control over how numbers are converted.
Verify: time building 100000 pieces by both methods.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 6.4 (string.rep, string.format) and 6.6 (table.concat), 6.1 (tostring). Removed: the O(n^2) and string interning claims (including the 40-byte threshold), not on the page.
Method: documentation only; no commands were run.
