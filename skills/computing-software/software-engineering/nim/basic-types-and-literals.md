---
id: computing-software.software-engineering.nim.basic-types-and-literals
name: basic-types-and-literals
category: computing-software
field: software-engineering
product: nim
tags: [basic-types-and-literals, tutorial-basics, int, float, bool, char, string, conversion, literal, overflow, nim]
level: intro
status: docs-checked
description: "Use Nim int, uint, float, char and string types, their literal forms, explicit conversions and overflow behaviour."
sources:
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Basic types, literals and conversions

Goal: pick and convert primitive types safely.

- Built-in integer types: `int int8 int16 int32 int64 uint uint8 uint16 uint32 uint64`. `int` is the default and has the same size as a pointer. Floats: `float float32 float64`; `float` is always 64-bit.
- Literals: `0xFF` hex, `0b` binary, `0o` octal (a leading zero alone is not octal), `1_000_000` with underscores, `1.0e9` floats, `'a'` chars, `"text"` strings, raw `r"a\b"`, and `"""..."""` long strings that span lines and treat `\` literally.
- Type suffixes pick a non-default type: `0'i8`, `0'u`, `0.0'f32`.
- Conversion between numeric types is by type-call: `int32(1)`, `int8('a')`, `int(2.5)` (the tutorial notes it rounds down to 2). Integers and floats never convert automatically in either direction; use `toInt` and `toFloat`, or the type call.
- Different integer types in one expression are converted automatically when lossless; if information would be lost, `RangeDefect` is raised (when not detectable at compile time).
- `+ - * div mod` and comparisons work on integers; `and or xor not` are bitwise on integers; `shl` and `shr` shift and always treat arguments as unsigned. Unsigned operations wrap around and cannot overflow.
- `inc`, `dec`, `succ` and `pred` can raise `RangeDefect` or `OverflowDefect` when compiled with the matching runtime checks.
- `$` turns a basic value into a string, and `cast[T](x)` reinterprets a value (unsafe).

Gotchas:
- `char` is always one byte, so it cannot hold most UTF-8 characters; chars cannot be mixed with integers (use `ord` and `chr`).
- Strings are by convention UTF-8 but this is not enforced; `s[i]` is the i-th byte-sized char, not a Unicode character.
- `-d:danger` is the switch the tutorial recommends for comparing speed with unsafe languages, because checks are otherwise active.

## Checked

2026-11-08. Searched the full text of the Nim tutorial (tut1) for each claim in the Strings, Integers, Floats, Type Conversion and literal sections: type lists, int pointer size, float 64-bit, literal prefixes and suffixes, long strings, shl/shr, unsigned wrap, lossless auto conversion and RangeDefect, no int/float auto conversion, char size, UTF-8 note.

Removed as unconfirmed on those pages: the claim that `-d:danger` makes overflow wrap, the claim that `/` always yields a float with a worked example, and the cstring/bool type details. Dropped the manual and library index sources as not used.

Method: documentation only; no commands were run.
