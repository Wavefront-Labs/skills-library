---
id: computing-software.software-engineering.dart.dart-null-safety-operators
name: dart-null-safety-operators
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-null-safety, null-safety-operators]
level: practitioner
status: docs-checked
description: "Write null-safe code with ?, ??, ?., ??=, the bang operator and type promotion."
sources: ["https://dart.dev/null-safety/understanding-null-safety", "https://dart.dev/language/operators"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nullable types, ?., ??, ! and flow analysis
- `String? s;` nullable; `s?.length` evaluates to null when `s` is null; `s ?? 'x'` defaults; `s ??= 'x'` assigns only if null; `s!` casts to non-nullable and throws at runtime if null.
- Flow analysis promotes local variables, parameters and private final fields (Dart 3.2) after a null check; public or non-final fields and top-level variables are not promoted, so copy to a local first.
- `late` defers the non-null guarantee to runtime; `required` makes a named parameter mandatory independent of nullability.
- Soundness is guaranteed only for fully null-safe programs.
Verify: `dart analyze` on a promotion example.

## Checked

Date: 2026-11-02. Confirmed on Dart 'Understanding null safety' and Operators pages (?., ??, ??=, !, promotion rules, late, required, soundness). Removed as not confirmed: the Dart 2.12 and Dart 3 version statements and the analyzer-lint claim.

Method: documentation only; no commands were run.
