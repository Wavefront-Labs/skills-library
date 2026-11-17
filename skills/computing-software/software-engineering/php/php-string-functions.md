---
id: computing-software.software-engineering.php.php-string-functions
name: php-string-functions
category: computing-software
field: software-engineering
product: php
tags: [php, php-strings, string-functions]
level: intro
status: docs-checked
description: "Use str_contains, str_starts_with and str_ends_with, sprintf with positional arguments, and heredoc/nowdoc."
sources: ["https://www.php.net/manual/en/function.str-contains.php", "https://www.php.net/manual/en/function.str-starts-with.php", "https://www.php.net/manual/en/function.str-ends-with.php", "https://www.php.net/manual/en/function.sprintf.php", "https://www.php.net/manual/en/function.number-format.php", "https://www.php.net/manual/en/language.types.string.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String helpers: str_contains, sprintf and heredoc
- `str_contains($haystack, $needle)`, `str_starts_with()` and `str_ends_with()` are PHP 8 functions; `str_contains` does a case-sensitive check and returns `bool`.
- `sprintf()` supports positional arguments such as `%1$s` (see the sprintf page for the full format table); `number_format()` formats a number for display.
- Heredoc interpolates variables; nowdoc does not. As of PHP 7.3.0 the closing identifier may be indented, and that indentation is removed from every line of the body; indenting the closing identifier further than any body line throws a `ParseError`.

Verify: unit-test formatting under a different locale and with edge inputs (empty needle, empty string).

## Checked
2026-11-03. Confirmed on the str_contains, sprintf, number_format and string-type manual pages. Removed (not confirmed in fetched text): the `strpos` migration remark, a sample `sprintf('%05.2f ...')` format, money/bcmath advice.
Method: documentation only; no commands were run.
