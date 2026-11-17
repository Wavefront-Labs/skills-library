---
id: computing-software.software-engineering.php.php-loose-comparison
name: php-loose-comparison
category: computing-software
field: software-engineering
product: php
tags: [php, php-types, loose-comparison]
level: practitioner
status: docs-checked
description: "Avoid == surprises: use strict comparison, know the PHP 8 string-to-number change, and use strict mode in in_array and array_search."
sources: ["https://www.php.net/manual/en/language.operators.comparison.php", "https://www.php.net/manual/en/function.in-array.php", "https://www.php.net/manual/en/function.array-search.php", "https://www.php.net/manual/en/control-structures.match.php", "https://www.php.net/manual/en/control-structures.switch.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loose vs strict comparison and type juggling
- Prefer `===` by default.
- `in_array($needle, $haystack, true)` and `array_search($needle, $haystack, true)` compare types too (objects must be the same instance). Without the third argument both use loose comparison, which can still match values of different types; the manual says to pass `strict` unless all types are known with certainty.
- As of PHP 8.0.0, a non-numeric string no longer loosely matches `0` in `in_array()`: the number is converted to a string and the two are compared as strings, so only a numeric string of the same value still matches. The switch manual page shows the same change (`switch(0)` no longer matches a non-numeric string case in PHP 8).
- `match` arms compare strictly (`===`); `switch` compares loosely.
- The spaceship operator `$a <=> $b` returns an int less than, equal to, or greater than zero (the manual examples print -1, 0, 1).
- `isset()` does not return true for array keys holding `null`; `array_key_exists()` does. `??` is the null coalescing operator for nested lookups.

Verify: test the edge values `0`, `"0"`, `""`, `null`, `"abc"` against your comparisons.

## Checked
2026-11-03. Confirmed on the comparison operators, in_array, array_search, match, switch and array_key_exists manual pages. Removed (not confirmed on the pages read): the `"1e3" == "1000"` example, `??=`, Elvis operator, nullsafe details.
Method: documentation only; no commands were run.
