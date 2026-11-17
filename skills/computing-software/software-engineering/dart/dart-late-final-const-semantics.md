---
id: computing-software.software-engineering.dart.dart-late-final-const-semantics
name: dart-late-final-const-semantics
category: computing-software
field: software-engineering
product: dart
tags: [dart, late-final-const-semantics]
level: practitioner
status: docs-checked
description: "Pick between var, final, const and late in Dart: compile-time vs runtime constants, lazy initialisation and canonicalised const values."
sources: ["https://dart.dev/language/variables", "https://dart.dev/language/classes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# final, const, late
- `final` is assigned once at runtime; `const` is a compile-time constant and deeply immutable,; const instances are canonical (see the Classes page).
- `late final x = expensive();` computes on first access; reading a `late` variable that was never initialised is a runtime error.
- `const` constructors need all instance variables `final`.
Verify: reading an unassigned `late` variable fails at runtime.

## Checked

Date: 2026-11-02. Confirmed on the Variables page: `final`, `const`, `late` (runtime error if never initialised, lazy initialiser runs at first use); Classes page: canonical const instances; Constructors page: const constructors need final instance variables. Removed the `LateInitializationError` name, the `identical` example and the widget-rebuild claim (not stated).

Method: documentation only; no commands were run.
