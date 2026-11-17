---
id: computing-software.software-engineering.php.php-nullsafe-coalescing
name: php-nullsafe-coalescing
category: computing-software
field: software-engineering
product: php
tags: [php, php-types, nullsafe-coalescing]
level: intro
status: docs-checked
description: "Use ?? to read missing array keys without isset boilerplate, and know how isset and array_key_exists treat null."
sources: ["https://www.php.net/manual/en/function.array-key-exists.php", "https://www.php.net/manual/en/function.isset.php", "https://www.php.net/manual/en/language.operators.comparison.php", "https://www.php.net/manual/en/functions.first_class_callable_syntax.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Null coalescing and null checks
- The array_key_exists manual page recommends the null coalescing operator `??` to check a value in a multidimensional array with a fixed number of dimensions, for example `array_key_exists($key3, $arr[$key1][$key2] ?? [])`.
- `isset()` determines whether a variable is declared and different than null, so it does not return true for array keys holding `null`; `array_key_exists()` does.
- The nullsafe operator `?->` exists in PHP 8; the first-class callable page notes it cannot be combined with `(...)` (compile-time error). Its short-circuit rules are not on the pages used here, so check the language manual before relying on chained forms.

Verify: unit-test with `null`, an empty string and `0` values.

## Checked
2026-11-03. Confirmed on the array_key_exists, isset and first-class callable manual pages. Removed (not confirmed on pages read): `??=` semantics, `?->` chain short-circuiting, Elvis operator falsiness, PHP version numbers for each operator.
Method: documentation only; no commands were run.
