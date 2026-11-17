---
id: computing-software.software-engineering.dart.dart-dart-define-config
name: dart-dart-define-config
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-environment, dart-define-config]
level: practitioner
status: docs-checked
description: "Define compile-time environment declarations with -D and read them with the fromEnvironment constructors."
sources: ["https://dart.dev/tools/dart-compile", "https://dart.dev/tools/dart-run"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment declarations (-D) and fromEnvironment
- `dart compile` accepts `-D<key>=<value>`, which defines an environment declaration readable with `String.fromEnvironment`, `int.fromEnvironment`, `bool.fromEnvironment` or `bool.hasEnvironment`.
- Example: `const url = String.fromEnvironment('API_URL', defaultValue: 'http://localhost');` and compile with `-DAPI_URL=<value>`.
- Declarations are fixed when the program is compiled and live in the output, so they are not a place for secrets.
- Check the `dart run` options reference for how your SDK passes declarations to `dart run`.
Verify: print the value from two builds compiled with different `-D` values.

## Checked
2026-11-03. Confirmed against dart.dev tools/dart-compile (`-D<key>=<value>`, the four fromEnvironment readers). Removed: `dart run --define=`, `Platform.environment['PORT']` and `.env` loaders (not on the pages read), and the claim that the constructors "must be const" (not stated on those pages).
Method: documentation only; no commands were run.
