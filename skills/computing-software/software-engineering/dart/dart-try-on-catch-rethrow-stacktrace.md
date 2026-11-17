---
id: computing-software.software-engineering.dart.dart-try-on-catch-rethrow-stacktrace
name: dart-try-on-catch-rethrow-stacktrace
category: computing-software
field: software-engineering
product: dart
tags: [dart, try-on-catch-rethrow-stacktrace]
level: practitioner
status: docs-checked
description: "Handle Dart errors: on Type catch, StackTrace, rethrow, finally, and when to throw Error vs Exception."
sources: ["https://dart.dev/language/error-handling", "https://dart.dev/effective-dart/usage", "https://dart.dev/libraries/async/zones"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exceptions
- `try {...} on FormatException catch (e, st) {...} catch (e) {...} finally {...}`; `rethrow` keeps the original stack, `throw e` resets it.
- `Exception` is for recoverable conditions; `Error` (e.g. `StateError`, `ArgumentError`, `UnimplementedError`) for programmer mistakes that should not be caught.
- Zones' `runZonedGuarded` catches uncaught errors.
Verify: a rethrown error preserves the original frames.

## Checked

Date: 2026-11-02. Confirmed on the Error handling page: `on` and `catch` with stack trace, `rethrow`, `finally`; Effective Dart usage: `rethrow` vs `throw` stack trace; Zones page: `runZonedGuarded`. Removed `Error.throwWithStackTrace` and `FlutterError.onError` (not stated).

Method: documentation only; no commands were run.
