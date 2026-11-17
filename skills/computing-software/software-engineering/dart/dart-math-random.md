---
id: computing-software.software-engineering.dart.dart-math-random
name: dart-math-random
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-numerics-math, math-random]
level: practitioner
status: docs-checked
description: "Use dart:math functions and constants, Random with a seed, Random.secure for security, and web integer limits."
sources: ["https://dart.dev/libraries/dart-math", "https://dart.dev/language/built-in-types"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dart:math, Random.secure and number formatting
- `import 'dart:math';` gives `sin`, `cos`, `min`, `max`, `pi`, `e` and `sqrt2`. Trigonometric functions take radians, not degrees.
- `Random()` accepts an optional seed. The default `Random` is pseudorandom and unsuitable for cryptography; use `Random.secure()` for tokens and keys.
- On native platforms `int` ranges from -2^63 to 2^63 - 1; on the web integers are JavaScript numbers and range from -2^53 to 2^53 - 1.
- `num` provides `abs()`, `ceil()` and `floor()`; `3.14159.toStringAsFixed(2)` formats to two decimals; use `isNaN` to test for NaN.
Verify: with a fixed seed, two `Random` instances produce the same sequence.

## Checked
2026-11-03. Confirmed against dart.dev libraries/dart-math (import, trigonometry in radians, min/max, constants, Random seed, Random.secure) and language/built-in-types (int ranges, num methods, toStringAsFixed, isNaN). Removed: `pow`, `atan2`, `BigInt.parse`, `round`, `toInt` and the `double.nan != double.nan` statement (not on the pages read).
Method: documentation only; no commands were run.
