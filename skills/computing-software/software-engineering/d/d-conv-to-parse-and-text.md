---
id: computing-software.software-engineering.d.d-conv-to-parse-and-text
name: d-conv-to-parse-and-text
category: computing-software
field: software-engineering
product: d
tags: [d-conv-to-parse-and-text, std-conv, to, parse, text, convexception, convoverflowexception, radix, string-to-int, toimpl, octal, hexstring, d]
level: intro
status: docs-checked
description: "Convert with to!int/to!string/to!double, parse prefixes with parse!T and radix, text/wtext/dtext, enum and array conversions, and ConvException/ConvOverflowException handling."
sources:
  - https://dlang.org/phobos/std_conv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# to!T conversions, parse, text and safe numeric casts

Goal: convert types safely.

```d
import std.conv;
int a = "123".to!int;          // ConvException on bad input
double d = to!double("1e3");
string s = 42.to!string;       // "42"
ubyte b = 300.to!ubyte;        // ConvOverflowException
int h = "ff".to!int(16);       // 255
string bin = 10.to!string(2);  // "1010"
```
- `to!T(value)` is checked: it throws `ConvOverflowException` when the value does not fit (`to!int(4.2e10)`), and skips the check when none is needed (`to!double(42)`).
- It handles numbers, strings, enums (string to enum by member name, case-sensitive), arrays and associative arrays element-wise (`to!(double[])(split(str))`), and class downcasts (throws `ConvException` when the source is non-null and the target is null).
- `parse!T(ref s)` takes the input by reference (no string literals), consumes a prefix, advances the input, and does not throw when only part of the input converted. `parse!int(s, 16)` takes a radix; `Yes.doCount` also returns the number of consumed characters.
- String to number conversion does not accept D literal prefixes (`0x`), digit-group underscores or type suffixes; pass a radix instead.
- `text(a, " ", b)` joins the string forms of its arguments; `wtext`, `dtext` give wide strings. `writeText` writes to an output range.
- `octal!177` or `octal!"177"` is a compile-time octal literal (same as `0177` in C); `hexString!"DEADBEEF"` converts hex digit pairs to a string at compile time.
- `signed(x)` and `unsigned(x)` change signedness without rewriting a cast when the type of `x` changes.
- A radix for integer to string must be from 2 to 36; `toChars` is the lightweight alternative (radix 2, 8, 10 or 16).

Gotchas:
- String to number conversion does not allow whitespace, so `to!int("12 ")` throws; `strip` first.
- Floating point to integer truncates toward zero (`to!uint(3.99)` is 3); use `roundTo!int` to round.

Verify: unittest with `assertThrown!ConvException("x".to!int)`.

## Checked

2026-11-08. Confirmed against std.conv: `to` (overflow checking, whitespace, radix, enum, array, class and truncation behaviour), `parse` (by-reference input, advancing, doCount, radix), `text`/`wtext`/`dtext`, `writeText`, `octal`, `hexString`, `signed`/`unsigned`, `roundTo`, `toChars`, `ConvException`, `ConvOverflowException`.

Removed because the page did not confirm it: `octal!0755` form, conversion of ranges via `to!(char[])(range)`, `lrint` for rounding, pointer conversion detail. Replaced landing-page sources with the std.conv page.

Method: documentation only; no commands were run.
