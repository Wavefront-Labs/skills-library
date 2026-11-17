---
id: computing-software.software-engineering.dart.dart-exceptions-errors
name: dart-exceptions-errors
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-exceptions, exceptions-errors]
level: practitioner
status: docs-checked
description: "Throw and catch appropriately, distinguishing recoverable Exceptions from programmer Errors."
sources: ["https://dart.dev/language/error-handling", "https://dart.dev/effective-dart/usage", "https://dart.dev/libraries/async/zones"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exception versus Error, rethrow and custom exceptions
- `Exception` for recoverable conditions, `Error` (ArgumentError, StateError, RangeError) for programming bugs; do not catch `Error` to continue.
- `try {} on FormatException catch (e, s) {} finally {}`; `rethrow` preserves the stack trace, `throw e` resets it.
- Custom: `class AppException implements Exception { final String msg; ... }`.
- Avoid catching without `on` unless at a top-level boundary; `runZonedGuarded` handles uncaught errors in a zone (see the Zones page).
- `assert` is enabled with the `--enable-asserts` flag (see the Error handling page).
Verify: `rethrow` keeps the original stack trace; `throw e` resets it.

## Checked

Date: 2026-11-02. Confirmed on the Error handling page: Exception and Error, `on`/`catch` with stack trace, `rethrow`, `--enable-asserts`; Effective Dart usage: `rethrow` preserves the stack trace, `throw` resets it; Zones page: `runZonedGuarded`. Removed `PlatformDispatcher.onError` and the `throwsA` check (not stated).

Method: documentation only; no commands were run.
