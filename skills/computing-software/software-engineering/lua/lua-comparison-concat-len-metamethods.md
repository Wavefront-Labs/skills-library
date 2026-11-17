---
id: computing-software.software-engineering.lua.lua-comparison-concat-len-metamethods
name: lua-comparison-concat-len-metamethods
category: computing-software
field: software-engineering
product: lua
tags: [lua, comparison-concat-len-metamethods]
level: advanced
status: docs-checked
description: "Overload comparison, concatenation, length and unary minus in Lua with the matching metamethods, and what 5.4 removed."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# More metamethods
- `__lt` and `__le` serve `<` and `<=`; `a > b` is translated to `b < a` and `a >= b` to `b <= a`. In 5.4 `__lt` is no longer used to emulate `__le`.
- `__eq` is tried only when both operands are tables or both full userdata and they are not primitively equal.
- `__concat` is tried when an operand is neither a string nor a number; `__len` is tried for `#` unless the operand is a string (the result is adjusted to one value); `__unm` is unary minus.
- `__idiv`, `__band`, `__bor`, `__bxor`, `__bnot`, `__shl` and `__shr` cover floor division and the bitwise operators.
- `__call` makes a value callable; `__tostring` and `__name` affect `tostring`.
Verify: define a vector type and test `a < b`, `#a`, `-a`, `a .. "x"`.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: section 2.4 (__concat, __len, __eq, __lt, __le, __idiv and bitwise events, __call, __name), section 3.4.4 (a > b is b < a), section 8.1 (__le emulation removed), tostring. Removed: the claim that the bitwise and integer-division metamethods exist since 5.3 (the manual covers 5.4 only).
Method: documentation only; no commands were run.
