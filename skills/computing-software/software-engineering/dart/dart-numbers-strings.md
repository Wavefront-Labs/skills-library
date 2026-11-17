---
id: computing-software.software-engineering.dart.dart-numbers-strings
name: dart-numbers-strings
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-variables-types, numbers-strings]
level: intro
status: docs-checked
description: "Handle int and double semantics, parsing and string interpolation, including web int limits."
sources: ["https://dart.dev/language/built-in-types", "https://dart.dev/language/operators", "https://dart.dev/libraries/dart-core"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# num, int, double, String and interpolation
- `int` is 64-bit on native platforms (-2^63 to 2^63 - 1) but on the web integers are JavaScript numbers, limited to -2^53 to 2^53 - 1. `double` is IEEE 754 64-bit. `/` gives a double (`5 / 2 == 2.5`); `~/` gives an integer result (`5 ~/ 2 == 2`); `%` is the remainder.
- `int.parse('42')`, `double.parse('0.50')`, `num.parse` (int if possible, else double); `int.parse('42', radix: 16)` parses in a given radix.
- Interpolation `'$x ${a + b}'` calls `toString()`; `$id` needs no braces for a plain identifier. Raw strings `r'\n'`; adjacent literals concatenate (so does `+`); multiline `'''...'''`.
- `StringBuffer` builds strings without creating a new `String` until `toString()`. `String.codeUnits` are UTF-16 code units; `runes` expose code points; the `characters` package handles user-perceived characters (grapheme clusters).

Verify: print results of `7 ~/ 2` and `7 / 2`.

## Checked

Checked 2026-11-08 against https://dart.dev/language/built-in-types (read in full), the arithmetic operator table of https://dart.dev/language/operators, and the strings and numbers sections of https://dart.dev/libraries/dart-core. Removed (not confirmed in pages read): the `FormatException` on bad input and `int.tryParse` returning null.

Method: documentation only; no commands were run.
