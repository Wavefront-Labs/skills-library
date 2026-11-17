---
id: computing-software.software-engineering.d.d-enforce-collectexception-and-result-patterns
name: d-enforce-collectexception-and-result-patterns
category: computing-software
field: software-engineering
product: d
tags: [d-enforce-collectexception-and-result-patterns, error-handling, enforce, collectexception, errnoexception, nullable, result-type, error-values, ifthrown, handle, d]
level: practitioner
status: docs-checked
description: "Validate input with std.exception enforce/ErrnoException, collect exceptions with collectException, and supply fallbacks with ifThrown and handle."
sources:
  - https://dlang.org/phobos/std_exception.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# enforce, collectException, ifThrown and handle

Goal: choose an error style.

- `enforce(cond, "message")` throws `Exception` when `cond` is false and returns `cond`'s value otherwise (`enforce(malloc(n), "malloc failed")`); `enforce!MyError(cond, "msg")` picks the type; a lazy `Throwable` or a delegate returning the message are also accepted. The message is lazy, so it is only built on failure.
- `enforce` is for error handling, not program logic: use `assert` for that, and never use `enforce` inside contracts (`in`, `out`, invariants), which are compiled out with `-release`.
- `errnoEnforce(value, msg)` throws `ErrnoException` (`errno`, `errnoMsg`), assuming the failed call set `errno`.
- `collectException(expr)` returns the caught exception or null; `collectException(expr, result)` also stores the result; `collectExceptionMsg(expr)` returns the message (`emptyExceptionMsg` for an empty one). Avoid collecting non-`Exception` throwables.
- `expr.ifThrown(default)` and `ifThrown!E(expr, e => ...)` give fallback values; calls can be chained and the expression and handler need a common type. `handle!(E, RangePrimitive.front, (e, r) => 0)` substitutes values for exceptions thrown by range primitives.
- `mixin basicExceptionCtors;` writes the standard constructors for a trivial `Exception` subclass (they cannot be overloaded with other custom constructors).
- `assumeWontThrow(expr)` lets a `nothrow` function call throwing code; an actual throw becomes an `AssertError`.

Gotchas:
- `to!int` throws `ConvException`; catch or `ifThrown!ConvException` narrowly.
- The condition passed to `enforce` always runs; only the message is lazy.

Verify: unittest feeds invalid input and checks the `ifThrown` fallback, `assertThrown!MyError(...)`.

## Checked

2026-11-08. Confirmed against the std.exception page: `enforce` overloads and the assert/contract note, `errnoEnforce`, `ErrnoException`, `collectException`, `collectExceptionMsg`, `emptyExceptionMsg`, `ifThrown`, `handle`, `RangePrimitive`, `basicExceptionCtors`, `assumeWontThrow`, `assertThrown`.

Removed because the page does not cover it: Nullable and SumType result-type advice, the exceptions-versus-return-values guidance, the nothrow boundary catch pattern, and scope(exit) cleanup advice. The description was narrowed to match. Replaced landing-page sources with the std.exception page.

Method: documentation only; no commands were run.
