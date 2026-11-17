---
id: computing-software.software-engineering.v-lang.v-strconv-parsing-and-formatting
name: v-strconv-parsing-and-formatting
category: computing-software
field: software-engineering
product: v-lang
tags: [v-strconv-parsing-and-formatting, arrays-math-strconv, strconv, atoi, parse_int, parse_uint, atof64, format, v_sprintf, string to int, number parsing, v-lang]
level: practitioner
status: docs-checked
description: "Parse ints and floats with strconv.atoi, parse_int, parse_uint, atof64 with error handling, and format numbers with format_int and interpolation."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# strconv: parsing and formatting numbers

Goal: convert text to numbers with validation.

- `import strconv`.
- `n := strconv.atoi('42')!` (error on garbage); `strconv.parse_int('ff', 16, 64)!`; `strconv.parse_uint('7', 10, 32)!`; floats `strconv.atof64('3.5')!`.
- Forgiving built-ins: `'42'.int()`, `'3.5'.f64()`, `'9'.i64()` return 0 when parsing fails; use them only when failure is acceptable.
- Format: `strconv.format_int(n, 2)` (binary); `strconv.v_sprintf(fmt, args...)` takes `...voidptr` arguments, so prefer string interpolation such as `'${n:02}'`.
- Quote: `strconv.quote(s)`.
- Check a numeric string: `s.is_int()`, `s.is_hex()`, `s.is_bin()`.

Gotchas:
- `atoi` rejects values outside the i32 range with an error; use `strconv.parse_int(s, 10, 64)!` for larger numbers.

Verify: `assert strconv.atoi('x') or { -1 } == -1`.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: strconv.atoi (rejects outside i32), parse_int, parse_uint, atof64, format_int, v_sprintf(str, ...voidptr), quote (vlib/strconv), string.int()/i64()/f64() fall back to 0, is_int/is_hex/is_bin (vlib/builtin/string.v), `${t.month:02}` padding in vlib/time/format.v.
Removed or corrected: '(confirm)' markers, `v_sprintf('%05d', 42)` as written (arguments must be voidptr), 'locale is ignored', and the overflow wording for atoi.
Method: documentation only; no commands were run.
