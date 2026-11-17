---
id: computing-software.software-engineering.php.php-exception-hierarchy
name: php-exception-hierarchy
category: computing-software
field: software-engineering
product: php
tags: [php, php-errors, exception-hierarchy]
level: practitioner
status: docs-checked
description: "Catch the right Throwable and know where TypeError, ValueError, ArithmeticError and the SPL exceptions sit in the hierarchy."
sources: ["https://www.php.net/manual/en/class.throwable.php", "https://www.php.net/manual/en/class.error.php", "https://www.php.net/manual/en/class.exception.php", "https://www.php.net/manual/en/class.typeerror.php", "https://www.php.net/manual/en/class.valueerror.php", "https://www.php.net/manual/en/spl.exceptions.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Throwable, Error and Exception hierarchy
- `Throwable` is implemented by two base classes: `Error` (engine errors) and `Exception` (user and library exceptions). `class Error implements Throwable` and `class Exception implements Throwable` are siblings, so `catch (Exception $e)` does not catch an `Error`; catch `Throwable` to get both.
- Under `Error`: `TypeError` (and its subclass `ArgumentCountError`), `ValueError`, `ArithmeticError` and its subclass `DivisionByZeroError`.
- Under `Exception`: SPL exceptions such as `LogicException` (parent of `InvalidArgumentException`) and `RuntimeException`. Custom exceptions normally extend `Exception` or one of these.
- Chain causes through the `$previous` constructor argument (`__construct(string $message = "", int $code = 0, ?Throwable $previous = null)`) and read it with `getPrevious()`.

Verify: in a test, assert the exception class and `getPrevious()`.

## Checked
2026-11-03. Confirmed on the Throwable, Error, Exception, TypeError, ValueError and SPL exceptions manual pages (class declarations, hierarchy lists, constructor signature). Removed (the language.exceptions manual page was not retrievable): multi-catch and variable-less catch syntax, `finally` wording.
Method: documentation only; no commands were run.
