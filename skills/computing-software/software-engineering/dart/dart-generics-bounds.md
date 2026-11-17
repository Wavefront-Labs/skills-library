---
id: computing-software.software-engineering.dart.dart-generics-bounds
name: dart-generics-bounds
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-generics, generics-bounds]
level: practitioner
status: docs-checked
description: "Write generic types with extends bounds, use covariance rules and avoid reified-type surprises."
sources: ["https://dart.dev/language/generics", "https://dart.dev/language/type-system"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic classes, methods and bounds
- `class Box<T extends num>`; generic methods `T first<T>(List<T> xs) => xs.first;`.
- Dart generics are reified: `List<int>` is a real runtime type, `x is List<String>` works.
- Collections are covariant (a `List<int>` is a `List<num>`). The `covariant` keyword relaxes an overriding parameter type.
- `dynamic` turns off checks; prefer `Object?`.
Verify: `dart analyze --fatal-infos` with `strict-casts` enabled.

## Checked

Date: 2026-11-02. Confirmed on the Generics page: reified generic types, `extends` bounds; Type system page: `List<Animal> animals = <Dog>[Dog()]` is allowed, `covariant` keyword for overriding parameters, `strict-casts`. Removed the write-failure claim (not stated).

Method: documentation only; no commands were run.
