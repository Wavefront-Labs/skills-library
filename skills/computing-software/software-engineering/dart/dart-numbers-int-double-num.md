---
id: computing-software.software-engineering.dart.dart-numbers-int-double-num
name: dart-numbers-int-double-num
category: computing-software
field: software-engineering
product: dart
tags: [dart, numbers-int-double-num]
level: practitioner
status: docs-checked
description: "Use Dart int (64-bit native, 53-bit JS), double, num, parsing and toStringAsFixed, and the web number caveat."
sources: ["https://dart.dev/language/built-in-types", "https://dart.dev/language/operators", "https://dart.dev/libraries/dart-core"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numbers
- `int.parse('42')`, `double.parse('0.50')`, `num.parse` (an int if possible, otherwise a double), `int.parse('42', radix: 16) == 66`.
- `123.456.toStringAsFixed(2) == '123.46'` fixes digits after the decimal point; `toStringAsPrecision(2)` sets significant figures (`'1.2e+2'`).
- `/` returns a double, `~/` divides returning an integer, `%` is the remainder of integer division.
- Native `int` is 64-bit (-2^63 to 2^63 - 1); on the web an `int` is a JavaScript number, so values range only from -2^53 to 2^53 - 1. `double` is IEEE 754 64-bit.

Verify: print `5 ~/ 2` (2), `5 / 2` (2.5) and `5 % 2` (1).

## Checked

Checked 2026-11-08 against https://dart.dev/language/built-in-types (read in full), the arithmetic operator table of https://dart.dev/language/operators and the numbers section of https://dart.dev/libraries/dart-core. Removed (not confirmed in pages read): `int.tryParse` returning null, the `%` versus `remainder` comparison and its `-7 % 3` check, `BigInt`, and the claim that native `int` arithmetic wraps on overflow.

Method: documentation only; no commands were run.
