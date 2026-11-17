---
id: computing-software.software-engineering.dart.dart-final-const-late
name: dart-final-const-late
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-variables-types, final-const-late]
level: intro
status: docs-checked
description: "Choose var, final, const and late correctly and know compile-time constant rules."
sources: ["https://dart.dev/language/variables"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# var, final, const and late
- `var x = 1;` infers the type; a `final` variable is set only once; a `const` variable is a compile-time constant (and implicitly final).
- A `late` variable used before it is initialised causes a runtime error; a `late` variable with an initialiser runs it lazily on first use.
Verify: `dart analyze` and a small program that reads a late variable too early.

## Checked

Date: 2026-11-02. Confirmed on Dart Variables page (var inference, final versus const, late runtime error, lazy late initialiser). Removed as not confirmed: LateInitializationError name, `late final`, const canonicalisation example, prefer_final_locals lint.

Method: documentation only; no commands were run.
