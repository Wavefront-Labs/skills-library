---
id: computing-software.software-engineering.v-lang.v-string-interpolation-and-formatting
name: v-string-interpolation-and-formatting
category: computing-software
field: software-engineering
product: v-lang
tags: [v-string-interpolation-and-formatting, strings, string interpolation, format, printf, padding, precision, str method, v-lang]
level: practitioner
status: docs-checked
description: "Embed values with ${expr} and format specifiers such as width, precision, sign, hex and binary; call str() or interpolate custom types."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String interpolation and format specifiers

Goal: format output without printf.

- Use `${` before a variable and `}` after: `'Hello, ${name}!'`. Fields and expressions work: `'age = ${user.age}'`, `'can register = ${user.age > 13}'`.
- Specifier pattern: `${varname:[flags][width][.precision][type]}`. Flags: `-` left-align, `0` zero padding, `+` show sign. `'` and `#` are not supported.
- Width is the minimum field width; runtime widths use parentheses, `${name:(width)}`; runtime precision `${value:(width).(precision)f}`.
- Precision applies to floats: `.2` drops insignificant trailing zeros (`10.0000` gives `10`), `.2f` keeps them (`10.00`).
- Types: `f F`, `e E`, `g G`, `d`, `x X`, `o`, `b`, `s`. Floats default to `g`, integers to `d`; leave the type off in most cases. Hex, octal and binary need an integer.
- Examples with `x := 123.4567`: `${x:.2}` gives `123.46`, `${x:10}` gives `   123.457`, `${int(x):-10}` left-aligns, `${int(x):010}` gives `0000000123`, `${int(x):+05}` gives `+0123`, `${int(x):b}` gives `1111011`, `${int(x):X}` gives `7B`.
- `r` and `R` repeat a string: `${'abc':3r}` gives `abcabcabc`, `3R` gives uppercase.
- `age.str()` also converts a number to a string.

Verify: `assert '${123.4567:.2}' == '123.46'`.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "String interpolation" and "String operators"). Removed as not stated there: the old `$name` form and `\$` escaping, `'${3.14159:.2f}'` as written (`.2f` keeps zeros per the docs), the custom `str()` auto-generated multi-line struct form, alternate-quote advice for nested quotes, and the `'$x.y'` behaviour.

Method: documentation only; no commands were run.
