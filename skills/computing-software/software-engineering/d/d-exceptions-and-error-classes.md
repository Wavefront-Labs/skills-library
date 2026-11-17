---
id: computing-software.software-engineering.d.d-exceptions-and-error-classes
name: d-exceptions-and-error-classes
category: computing-software
field: software-engineering
product: d
tags: [d-exceptions-and-error-classes, error-handling, exception, throwable, error, throw, catch, custom-exception, exception-chaining, finally, d]
level: practitioner
status: draft
description: "Throw and catch D exceptions, know Throwable/Exception/Error, define custom exceptions, chaining via next, finally/scope, and rethrow with context."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Exceptions vs Errors: throw, catch, Throwable hierarchy

Goal: use exceptions idiomatically.

- `Throwable` base; `Exception` is recoverable (I/O, parse); `Error` signals programmer bugs or fatal runtime states (AssertError, RangeError, OutOfMemoryError) and should rarely be caught.
- Custom: `class ConfigError : Exception { this(string msg, string file = __FILE__, size_t line = __LINE__) { super(msg, file, line); } }`.
- Catch order specific to general; `catch (Exception e) { writeln(e.msg); }`; rethrow `throw e;` (keeps trace) or `throw new Wrapper("ctx", e)` (the second argument chains `next`).
- Info: `e.toString()` prints trace, `e.file`, `e.line`, `e.info`.
- `nothrow` functions cannot throw `Exception`.
- Combine with `scope(failure)` and `finally` for cleanup.
- Exception allocation uses the GC: not allowed in `@nogc`.

Gotchas:
- Catching `Throwable` swallows assertion failures; if you must at a thread boundary, log and abort.
- Exceptions across `extern(C)` frames are unsafe (may skip C cleanup).

Verify: unittest with `assertThrown!ConfigError(parse("bad"))`.
