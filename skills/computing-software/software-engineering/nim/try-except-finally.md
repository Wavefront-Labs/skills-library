---
id: computing-software.software-engineering.nim.try-except-finally
name: try-except-finally
category: computing-software
field: software-engineering
product: nim
tags: [try-except-finally, exceptions, try, except, finally, raise, exception, getcurrentexception, error-handling, nim]
level: practitioner
status: docs-checked
description: "Catch and raise Nim exceptions with try/except/finally, re-raise, and read the current exception and its message."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# try, except, finally and raise

Goal: handle errors predictably.

```nim
try:
  let n = parseInt(s)
except ValueError as e:
  echo "bad number: ", e.msg
finally:
  cleanup()
```
- Raise with `raise newException(IOError, "IO failed")`. A bare `raise` with no exception name re-raises the current exception; `ReraiseDefect` is raised if there is none.
- One `except` clause may list several types: `except ValueError, IOError:`.
- Inside a handler, `except IOError as e:` gives `e.msg`. `getCurrentException()` always returns a `ref Exception` (cast with `(ref IOError)(getCurrentException())` for the exact type), and `getCurrentExceptionMsg()` returns just the message.
- `try` is an expression: the try branch type must fit the except branches, and the `finally` branch must be void. After a `(` it must be written as a one liner.
- `finally` is always executed after the exception handlers. An unhandled exception propagates through the call stack.
- Custom exceptions are types: `type LoadError* = object of Exception`; ending the name with `Error` is recommended.
- `defer` is an alternative to `try ... finally` that avoids nesting.

Gotchas:
- The tree is `Exception`, with `CatchableError` (IOError, OSError, ValueError, KeyError, ...) and `Defect` (programming bugs such as IndexDefect, RangeDefect, OverflowDefect). Defects are strictly speaking not catchable, so catch `CatchableError` rather than `Exception`.

Verify: parseInt("x") is caught and the finally block still executes.

## Checked

2026-11-08. Read the Nim manual sections Try statement, Try expression, Except clauses, Custom exceptions, Defer statement, Raise statement and Exception hierarchy in full; the bullets above match them.

Removed as unconfirmed on the manual: `e.getStackTrace()` and the debug-build trace claim, the ARC remark about freeing exceptions, and the claim that `finally` runs on `return` (the manual says only that it runs after handlers). Dropped the tutorial and lib index sources (not used).

Method: documentation only; no commands were run.
