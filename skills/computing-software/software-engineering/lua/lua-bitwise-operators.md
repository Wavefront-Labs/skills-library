---
id: computing-software.software-engineering.lua.lua-bitwise-operators
name: lua-bitwise-operators
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-integer-bitops, bitwise-operators]
level: advanced
status: docs-checked
description: "Use native bitwise operators in 5.3 and 5.4 and bit libraries for 5.1 and LuaJIT."
sources: ["https://www.lua.org/manual/5.4/manual.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bitwise operators and 5.1 compatibility
- Operators `& | ~ << >> ~` (binary xor and unary not) work on integers in Lua 5.3+; floats with exact integer values are converted, others raise an error.
- Shifts are logical (vacated bits fill with zeros); a shift by 64 or more bits gives 0; a negative shift goes the other way.
- Lua 5.3 deprecates the `bit32` library in favour of native operators (5.3 manual, section 8.2); LuaJIT and 5.1 use the `bit` library.
- Integers are 64-bit; `string.pack` / `string.unpack` (5.3+) handle binary layouts.
Verify: `0xFF & 0x0F` equals 15.

## Checked

Date: 2026-11-02. Confirmed on Lua 5.4 manual sections 3.4.2-3.4.3 (operators, float conversion, logical shifts, shift by 64 or more) and the 5.3 manual section 8.2 (bit32 deprecated). Fixed: bit32 was said to be removed in 5.3; it is deprecated there. Removed unconfirmed: bit library function names, 64-bit signed wording, sign test.

Method: documentation only; no commands were run.
