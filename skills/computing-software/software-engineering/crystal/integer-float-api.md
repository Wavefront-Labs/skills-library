---
id: computing-software.software-engineering.crystal.integer-float-api
name: integer-float-api
category: computing-software
field: software-engineering
product: crystal
tags: [integer-float-api, stdlib-strings-numbers, int32, int64, uint8, float64, number-conversion, overflow, wrapping-arithmetic, round, floor-division, math, to-i, bigint, bigdecimal, crystal]
level: practitioner
status: docs-checked
description: "Choose Int8..Int128 and Float32/64, convert with to_i32 and to_u8, handle overflow, rounding, division and Math functions."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Int, Float and number conversion

Goal: avoid numeric surprises.

- Types: `Int8/16/32/64/128`, `UInt8..128`, `Float32/64`; literals suffix `_i64`, `_u8`, `_f32`.
- Convert: `x.to_i64`, `x.to_u8` (raises OverflowError if out of range), `x.to_u8!` (wraps/unchecked), `x.to_f`, `"12".to_i`, `Int32.new(x)`.
- Arithmetic overflow raises `OverflowError` for `+ - *`; wrapping ops `&+ &- &*`.
- `/` on two ints returns Float64 (`7 / 2 == 3.5`); `//` is floored division (`7 // 2 == 3`, `-7 // 2 == -4`); `tdiv` truncates toward zero; `%` is floored modulo (sign of the divisor); `remainder` takes the sign of the dividend.
- `x.round`, `round(2)`, `floor`, `ceil`, `abs`, `divmod`, `Math.sqrt`, `**` for powers, `Math::PI`, `Float64::INFINITY`, `nan?`.
- Big: `require "big"` for BigInt, BigFloat, BigDecimal, BigRational.

Gotchas:
- Float compare with `==` is exact; use `(a - b).abs < eps`.
- Mixed Int/Float arithmetic yields Float.
- Autocasting of expressions to a wider type is off when the compiler flag `no_number_autocast` is passed (see the autocasting page of the language reference).

Verify: `crystal eval 'p -7 // 2'` prints -4 and `p 7 / 2` prints 3.5.

## Checked

Date 2026-11-03. Confirmed in the Int and Number source that Int / Int returns Float64 (Number.expand_div), // is floored division, % is floored modulo, tdiv and remainder truncate, divmod, fdiv, abs, round, floor, ceil, ** (OverflowError on overflow, ArgumentError on negative exponent), Float64::INFINITY and nan?, and in the language reference that no_number_autocast disables expression autocasting. Fixed the real error that claimed / floors on ints (7 / 2 is 3.5; use //) and removed the '(confirm)' hedge.

Method: documentation only; no commands were run.
