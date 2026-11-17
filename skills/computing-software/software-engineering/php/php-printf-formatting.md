---
id: computing-software.software-engineering.php.php-printf-formatting
name: php-printf-formatting
category: computing-software
field: software-engineering
product: php
tags: [php, printf-formatting, formatting]
level: intro
status: docs-checked
description: "Format strings and numbers in PHP with sprintf, number_format and NumberFormatter, avoiding locale and argument-count traps."
sources: ["https://www.php.net/manual/en/function.sprintf.php", "https://www.php.net/manual/en/function.printf.php", "https://www.php.net/manual/en/function.number-format.php", "https://www.php.net/manual/en/function.vsprintf.php", "https://www.php.net/manual/en/class.numberformatter.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# printf, sprintf and number formatting

```php
sprintf('%2$s %1$s', 'world', 'hello');      // positional args: %[argnum$][flags][width][.precision]specifier
number_format(1234567.891, 2);               // thousands grouping, decimals, rounding half up
number_format(1234567.891, 2, ',', '.');     // custom decimal and thousands separators
vsprintf('%s-%s', ['a', 'b']);               // arguments from an array
```
The `NumberFormatter` class (ext-intl) is the locale-aware alternative; see its manual page for styles. `printf` outputs and returns the length of the outputted string; `sprintf` returns the string.

## Gotchas
- The `%f` specifier is locale aware; `%F` is not. Use `%F` for machine output such as CSV or SQL.
- As of PHP 8.0.0, fewer arguments than the format needs throws `ArgumentCountError` (previously `false` and a warning). Keep format strings constant rather than user-controlled.
- `number_format()` rounds using the half up rule; since PHP 8.3.0 a negative `decimals` rounds significant digits before the decimal point.
- `sprintf` does no escaping; never build SQL, HTML or shell commands from untrusted data with it.

Verify: compare `%f` and `%F` under a `setlocale()` that uses a comma decimal separator, and assert `ArgumentCountError` for a missing argument.

## Checked
2026-11-03. Confirmed on the sprintf, printf, number_format and NumberFormatter manual pages. Removed (not confirmed): sample output strings, `%d` truncation claims, float-drift/bcmath/brick-money advice, large-value precision claim.
Method: documentation only; no commands were run.
