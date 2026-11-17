---
id: computing-software.software-engineering.lua.lua-numbers-integers-floats
name: lua-numbers-integers-floats
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-types-values, numbers-integers-floats]
level: practitioner
status: docs-checked
description: "Handle Lua 5.3+ integer/float subtypes, division, overflow and number-to-string conversion."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integer and float subtypes
- Standard Lua 5.4 uses 64-bit integers and 64-bit floats (it can be compiled with 32-bit numbers); `math.type(x)` returns `"integer"`, `"float"`, or fail for non-numbers.
- `/` and `^` always convert operands to floats; `//` is floor division (rounds toward minus infinity) and `%` is the matching modulo; integer overflow wraps around (two's complement).
- Mixed integer/float arithmetic converts the integer to float. Comparison is by mathematical value regardless of subtype, so `3 == 3.0` is true.
- Float to integer conversion succeeds only for an integral value in range; `math.tointeger(x)` returns fail otherwise, and `%d` in `string.format` needs an integer-representable value.
- A decimal integer literal that overflows is read as a float (5.4); use hexadecimal to get wrap-around.
Verify: `print(math.type(10 // 3), math.type(10 / 2))`.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: section 2.1 (number subtypes, wrap-around), section 3.4.1 (/, //, %), section 3.4.3 (conversions), section 3.4.4 (equality), math.type, math.tointeger, section 8.1 (overflowing literals). Removed: the claim that integral float keys are normalised, the `tostring(1e15)` output, and the statement about Lua 5.1/5.2/LuaJIT having only doubles.
Method: documentation only; no commands were run.
