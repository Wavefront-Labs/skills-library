---
id: computing-software.software-engineering.dart.dart-enhanced-enums-members
name: dart-enhanced-enums-members
category: computing-software
field: software-engineering
product: dart
tags: [dart, enhanced-enums-members]
level: practitioner
status: docs-checked
description: "Declare Dart enums with fields, const constructors, methods, interfaces and generics."
sources: ["https://dart.dev/language/enums", "https://dart.dev/blog/announcing-dart-2-15"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enhanced enums
- `enum Plan { free(0), pro(10); final int price; const Plan(this.price); }`.
- Use `.name`, `.index`, `Plan.values`, `byName('pro')`, `values.asNameMap()`.
- Enums can implement interfaces and mix in mixins but cannot extend classes.
- Exhaustive `switch` on enums needs no default.
Verify: `Plan.pro.price` is 10.

## Checked

Date: 2026-11-02. Confirmed on the Enums page: fields, const constructors, interfaces and mixins, no other class can be extended, `.index`, `.name`, `values`, exhaustive switch; `byName` and `asNameMap` on the Dart 2.15 announcement. Removed the claim that `byName` throws when absent (not stated).

Method: documentation only; no commands were run.
