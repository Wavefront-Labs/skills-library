---
id: computing-software.software-engineering.dart.dart-null-aware-operators-promotion
name: dart-null-aware-operators-promotion
category: computing-software
field: software-engineering
product: dart
tags: [dart, null-aware-operators-promotion]
level: practitioner
status: docs-checked
description: "Use ?., ??, ??=, ?[], ! and the rules for promoting nullable locals and fields in Dart."
sources: ["https://dart.dev/language/operators", "https://dart.dev/blog/announcing-dart-3-2", "https://dart.dev/null-safety/understanding-null-safety"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Null-aware operators
- `a?.b`, `a ?? d`, `a ??= d`, `list?[0]`, `a!` (throws on null), spread `...?xs`.
- Local variables promote after null checks (`if (x != null) x.length`); fields promote only when they are private and final (Dart 3.2 or newer); otherwise copy the field to a local first.
- Null-check patterns (`x?`) and `required` named parameters avoid `!`.
Verify: a nullable local promotes inside `if (x != null) { ... }`.

## Checked

Date: 2026-11-02. Confirmed on the Operators page: `?.`, `??`, `??=`, `?[]`, `!`, null-aware spread; Dart 3.2 announcement: non-null promotion of private final fields; Understanding null safety: flow analysis promotion of locals. Removed the `unnecessary_non_null_assertion` check.

Method: documentation only; no commands were run.
