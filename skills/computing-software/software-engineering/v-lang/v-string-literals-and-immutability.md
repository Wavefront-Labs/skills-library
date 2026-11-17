---
id: computing-software.software-engineering.v-lang.v-string-literals-and-immutability
name: v-string-literals-and-immutability
category: computing-software
field: software-engineering
product: v-lang
tags: [v-string-literals-and-immutability, strings, string, string literal, raw string, immutable, utf-8, escape, v-lang]
level: intro
status: docs-checked
description: "Use single or double quoted and raw r'' strings; V strings are immutable UTF-8 byte sequences with len in bytes, indexing gives u8."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String literals, raw strings and immutability

Goal: understand V's string model.

- Strings are UTF-8 and immutable by default. Single and double quotes both work; `vfmt` converts double quotes to single quotes unless the string contains a single quote.
- Raw strings: `r'hello\nworld'` keeps the backslash-n as two characters.
- Escapes work like C: `'\r\n'`, hex `'\x61'`, octal `'\141'`, Unicode `'★'`.
- `s.len` is the byte length (`'hello 🌎'.len == 10`); indexing gives a `u8` (`name[0] == u8(66)`), convert it with `.ascii_str()`.
- Assigning `s[0] = `H`` fails: "cannot assign to `s[i]` since V strings are immutable".
- `s.runes()` returns an array of the characters (`'hello 🌎'.runes().len == 7`).
- `+` concatenates and `+=` appends; both sides must be strings, so use `age.str()` or interpolation instead of `'age = ' + age`.
- `s.bytes()` gives `[]u8` and `arr.bytestr()` converts back.
- `'42'.int()` parses; see vlib/strconv for advanced conversions.

Verify: `assert 'hello 🌎'.len == 10` and `assert 'hello 🌎'.runes().len == 7`.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Strings", "String operators", "Runes"). Removed as not stated there: that multi-line strings keep indentation, the `.repeat(3)` method, `<` ordering of strings, `strings.Builder` as the way to build, the quadratic `+=` remark, and the claim that a slice may split a multibyte character.

Method: documentation only; no commands were run.
