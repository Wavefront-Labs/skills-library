---
id: computing-software.software-engineering.dart.dart-debug-logging
name: dart-debug-logging
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-debugging, debug-logging]
level: practitioner
status: docs-checked
description: "Debug with DevTools, use assert in development and avoid print in production Dart code."
sources: ["https://dart.dev/language/error-handling", "https://dart.dev/tools/linter-rules/avoid_print", "https://dart.dev/tools/dart-devtools"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugger, assert and logging
- Dart DevTools: the debugger and the logging view are the only parts available to all app types; web apps use browser tools such as Chrome DevTools for the rest.
- `print` calls should be avoided in production code (lint `avoid_print`, enabled under `linter > rules` in `analysis_options.yaml`); use a logging framework, or in Flutter `debugPrint` or a `kDebugMode` check.
- `assert(x > 0, 'message')` disrupts execution during development; a failure throws `AssertionError`. Assertions are enabled in Flutter debug mode and by dev tools such as `webdev serve`, and `dart run` and `dart compile js` take `--enable-asserts`. In production they are ignored and their arguments are not evaluated.
- `catch (e, s)` binds the stack trace as a `StackTrace` object in `s`.

Verify: reproduce with a breakpoint in DevTools or the IDE and confirm variable values.

## Checked

Checked 2026-11-08 against https://dart.dev/language/error-handling (assert and catch sections), the avoid_print linter rule page and https://dart.dev/tools/dart-devtools (availability table, read partially). Removed (not confirmed): `debugger()` from `dart:developer`, `package:logging` API details, `StackTrace.current`, and the IDE launch behaviour.

Method: documentation only; no commands were run.
