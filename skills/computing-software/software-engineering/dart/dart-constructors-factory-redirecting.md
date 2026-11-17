---
id: computing-software.software-engineering.dart.dart-constructors-factory-redirecting
name: dart-constructors-factory-redirecting
category: computing-software
field: software-engineering
product: dart
tags: [dart, constructors-factory-redirecting]
level: practitioner
status: docs-checked
description: "Use Dart named, factory, redirecting and const constructors, initializer lists and initializing formals."
sources: ["https://dart.dev/language/constructors", "https://dart.dev/language/primary-constructors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constructors
- `Point(this.x, this.y);` initialising formals; `Point.origin() : x = 0, y = 0;` initializer list runs before the body (and assert: `: assert(x >= 0)`).
- `factory Logger(String n) => _cache.putIfAbsent(n, () => Logger._(n));` may return existing instances or subtypes.
- Redirecting: `Point.unit() : this(1, 1);`; `const` constructor needs final fields.
- Primary constructors (class-header parameters) exist now but need a language version of at least 3.13; see the Primary constructors page.
Verify: two `Logger('a')` calls return identical instances.

## Checked

Date: 2026-11-02. Confirmed on the Constructors page: initialising formals, initializer list with `assert`, factory constructors, redirecting constructors, const constructors need final fields. Fixed: the skill said primary constructors were unavailable; the Primary constructors page documents them (language version 3.13).

Method: documentation only; no commands were run.
