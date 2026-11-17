---
id: computing-software.software-engineering.dart.dart-bounded-generics-variance
name: dart-bounded-generics-variance
category: computing-software
field: software-engineering
product: dart
tags: [dart, bounded-generics-variance]
level: advanced
status: docs-checked
description: "Constrain Dart type parameters with extends and understand covariance of generics and covariant overrides."
sources: ["https://dart.dev/language/generics", "https://dart.dev/language/type-system"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generics
- `class Box<T extends num>`; generic methods `T first<T>(List<T> xs)`.
- Generics are reified at runtime (`List<int>` differs from `List<String>`) and covariant: a `List<int>` is a `List<num>`.
- `covariant` keyword relaxes a parameter type in overrides.
Verify: `List<Animal> animals = <Dog>[Dog()];` compiles.

## Checked

Date: 2026-11-02. Confirmed on the Generics page: reified types, `extends` bounds; Type system page: covariant list assignment and the `covariant` keyword for overriding parameters. Removed the write-failure claim and its check (not stated).

Method: documentation only; no commands were run.
