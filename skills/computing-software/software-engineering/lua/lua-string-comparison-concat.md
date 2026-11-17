---
id: computing-software.software-engineering.lua.lua-string-comparison-concat
name: lua-string-comparison-concat
category: computing-software
field: software-engineering
product: lua
tags: [lua, string-comparison-concat]
level: practitioner
status: docs-checked
description: "Compare and join Lua strings: locale-dependent < ordering, interned equality, and why repeated .. in a loop is quadratic."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comparison and concatenation
- `==` compares strings by byte content and never coerces: `"0" == 0` is false. Order comparison of two strings uses the current locale.
- Each `a = a .. x` produces a new string; in loops collect pieces in a table and call `table.concat` once.
- `..` is right associative and has higher precedence than the comparison operators but lower than `+`/`-`; numbers are converted to strings in an unspecified format (use `string.format` for a specific one).
- `#s` is the byte length, not the character count (see the utf8 library).
Verify: time 1e5 appends with `..` against `table.concat`.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: section 3.4.4 (string equality by bytes, locale ordering, no coercion in ==), section 3.4.6 and 3.4.3 (concatenation, number-to-string format), section 3.4.8 (precedence table, right associativity). Removed: interning of short strings, the `strcoll` implementation detail and the `1 .. 2` malformed-number remark.
Method: documentation only; no commands were run.
