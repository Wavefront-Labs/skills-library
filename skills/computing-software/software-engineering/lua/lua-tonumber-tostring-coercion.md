---
id: computing-software.software-engineering.lua.lua-tonumber-tostring-coercion
name: lua-tonumber-tostring-coercion
category: computing-software
field: software-engineering
product: lua
tags: [lua, tonumber-tostring-coercion]
level: practitioner
status: docs-checked
description: "Convert between strings and numbers in Lua: tonumber bases, tostring, and where string-number coercion happens."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tonumber, tostring and coercion
- `tonumber(e)` returns a number or fail (nil); the string may have leading and trailing spaces and a sign, so `tonumber("  12  ")` is 12, `tonumber("0x10")` is 16. With a base (2 to 36) `e` must be a string: `tonumber("10", 2)` is 2.
- In 5.4 the string library sets metamethods that coerce strings to numbers in arithmetic (not bitwise) operations, so `"10" + 1` is 11 and `"1" + "2"` is an integer; `"abc" + 1` raises an error. Concatenation accepts numbers: `10 .. 1` is `"101"`.
- Comparisons never coerce: `"1" == 1` is false and `"1" < 1` raises an error.
- `tostring` calls `__tostring` if present, otherwise it may use a string `__name`; for control over number formatting use `string.format`.
Verify: `print(tonumber("  12  "), tonumber("1e2"), tonumber("12a"))` gives 12, 100.0, nil.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: tonumber, tostring, sections 3.4.3, 3.4.4 and 8.1 (string coercion via string metamethods, no bitwise coercion). Removed: the claim that floats print as `1.0` since 5.3 (not stated in the manual).
Method: documentation only; no commands were run.
