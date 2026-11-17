---
id: computing-software.software-engineering.dart.dart-constructors
name: dart-constructors
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-classes, constructors]
level: practitioner
status: docs-checked
description: "Use initialising formals, named and factory constructors, initializer lists and super parameters."
sources: ["https://dart.dev/language/constructors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generative, named, factory, const and redirecting constructors
- `Point(this.x, this.y);` initialising formals; named `Point.origin() : x = 0, y = 0;`; initializer lists run before the body and can use `assert`.
- `factory` constructors can return cached or subtype instances; redirecting `Point.a() : this(0, 0);`.
- Super parameters (Dart 2.17 or newer): `Child(super.x, {super.key})`.
- `const` constructors need all-final fields; the class can then be used in const expressions.
Verify: a `const` constructor on a class with a non-final field is rejected by the analyzer.

## Checked

Date: 2026-11-02. Confirmed on the Constructors page: initialising formals, named, factory and redirecting constructors, initializer lists with `assert`, super parameters need language version 2.17, const constructors need all instance variables `final`. Replaced the canonicalisation check (not stated there).

Method: documentation only; no commands were run.
