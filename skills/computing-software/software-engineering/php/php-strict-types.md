---
id: computing-software.software-engineering.php.php-strict-types
name: php-strict-types
category: computing-software
field: software-engineering
product: php
tags: [php, php-types, strict-types]
level: intro
status: docs-checked
description: "Enable declare(strict_types=1) and know which caller's mode applies, plus the version history of nullable, mixed, never, intersection and DNF types."
sources: ["https://www.php.net/manual/en/language.types.declarations.php", "https://www.php.net/manual/en/language.oop5.magic.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# strict_types and type declarations
- Enable strict mode per file with `declare(strict_types=1);`. The mode is decided by the file making the call: when a strict-typing caller invokes a function defined in a file without it, or the reverse, the caller's preference applies (a non-strict caller gets coercion). Calls made from inside internal functions are not affected by `strict_types`.
- Without strict mode, scalar arguments are coerced to the declared type where possible (the manual's coercive-typing example shows this).
- A `Stringable` object is not accepted by a `string` parameter under strict typing; declare `string|Stringable`.
- Version history from the manual: nullable types and `void` and `iterable` 7.1.0; `mixed` 8.0.0; intersection types and `never` (return only) 8.1.0; DNF types and standalone `null` / `false` 8.2.0. `?T` is identical to `T|null`.

Verify: pass a numeric string to an `int` parameter with and without `strict_types` and compare the outcomes.

## Checked
2026-11-03. Confirmed on the type declarations and magic-methods manual pages. Corrected: the original listed standalone `true` as 8.2; the type-declarations page lists only `null` and `false` for 8.2.0. Removed: "must be the first statement", int-to-float exception and TypeError-for-non-numeric claims (not found in the fetched text).
Method: documentation only; no commands were run.
