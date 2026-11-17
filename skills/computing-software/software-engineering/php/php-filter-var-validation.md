---
id: computing-software.software-engineering.php.php-filter-var-validation
name: php-filter-var-validation
category: computing-software
field: software-engineering
product: php
tags: [php, filter-var-validation, validation]
level: practitioner
status: docs-checked
description: "Validate input with filter_var and filter_input: FILTER_VALIDATE_* filters, false or null on failure, and the limits of built-in checks."
sources: ["https://www.php.net/manual/en/book.filter.php", "https://www.php.net/manual/en/function.filter-var.php", "https://www.php.net/manual/en/function.filter-input.php", "https://www.php.net/manual/en/function.filter-var-array.php", "https://www.php.net/manual/en/filter.constants.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Input validation with filter_var

```php
filter_var($v, FILTER_VALIDATE_INT, ['options' => ['min_range' => 1, 'max_range' => 100]]); // int|false
filter_var($v, FILTER_VALIDATE_BOOLEAN, FILTER_NULL_ON_FAILURE);  // true|false|null
filter_var($v, FILTER_VALIDATE_EMAIL);
filter_var($v, FILTER_VALIDATE_URL, FILTER_FLAG_PATH_REQUIRED);
filter_var_array($_POST, ['age' => FILTER_VALIDATE_INT, 'tags' => ['filter' => FILTER_DEFAULT, 'flags' => FILTER_REQUIRE_ARRAY]]);
filter_input(INPUT_GET, 'priority', FILTER_VALIDATE_INT, ['options' => ['default' => 5, 'min_range' => 0, 'max_range' => 9]]);
```
`filter_var()` returns the filtered data, or `false` on failure, or `null` when `FILTER_NULL_ON_FAILURE` is set. `filter_input()` returns `null` if the variable is not set (with `FILTER_NULL_ON_FAILURE` it returns `false` for an unset variable and `null` on failure). The default filter `FILTER_DEFAULT` is an alias of `FILTER_UNSAFE_RAW`, which validates nothing: always pass a `FILTER_VALIDATE_*` filter. `FILTER_NULL_ON_FAILURE` and `FILTER_THROW_ON_FAILURE` should not be used together.

## Gotchas
- Compare results with `=== false`; a valid integer `0` is falsy.
- `FILTER_SANITIZE_STRING` is deprecated as of PHP 8.1.0; do not rely on string "sanitising" as a security control.
- Validation is not authorisation. A syntactically valid URL still needs an allowlist before you fetch or redirect to it.

Verify: unit-test boundary values (`"0"`, `" 5"`, `"1e3"`, `""`) and assert on `=== false`.

## Checked
2026-11-03. Confirmed on the filter book page, filter_var, filter_input, filter_var_array and filter constants manual pages. The per-filter validate page (`filter.filters.validate`) returned 404, so removed: IP flags, regexp filter, float/locale claim, URL scheme claim, email-limits claim.
Method: documentation only; no commands were run.
