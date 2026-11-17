---
id: computing-software.software-engineering.dart.dart-enhanced-enums
name: dart-enhanced-enums
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-enums, enhanced-enums]
level: practitioner
status: docs-checked
description: "Declare enums with fields, constructors, methods and interfaces and switch exhaustively."
sources: ["https://dart.dev/language/enums", "https://api.dart.dev/stable/latest/dart-core/EnumByName.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enhanced enums with fields and methods
- `enum Level { low(1), high(3); final int w; const Level(this.w); }`; `Level.values`, `.name`, `.index` (zero-based); `Level.values.byName('low')` finds a value by name (extension `EnumByName`).
- Enhanced enums need language version 2.17 or newer, can implement interfaces and use mixins; all generative constructors must be `const` and instance fields `final`.
- The analyzer reports a switch over an enum that does not handle every value unless it has a default.
Verify: remove a case from a switch and read the analyzer diagnostic.

## Checked

Date: 2026-11-02. Confirmed on Dart Enums page (enhanced syntax, 2.17, interfaces, mixins, const constructors, values/name/index) and API EnumByName. Removed as not confirmed: the ArgumentError claim for unknown names.

Method: documentation only; no commands were run.
