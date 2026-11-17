---
id: computing-software.software-engineering.dart.dart-typedefs-callable
name: dart-typedefs-callable
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-callable-typedef, typedefs-callable]
level: practitioner
status: docs-checked
description: "Name function types with typedefs and make objects callable with call()."
sources: ["https://dart.dev/language/typedefs", "https://dart.dev/language/callable-objects", "https://dart.dev/blog/announcing-dart-2-15"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# typedef, function types and callable classes
- `typedef Predicate<T> = bool Function(T);` uses the function type syntax; Dart 2.13 or newer also allows typedefs for non-function types: `typedef Json = Map<String, Object?>;`.
- A class with `call()` can be invoked like a function and passed where a function type is expected.
- Tear-offs of constructors: `List.generate(3, Point.new)` (Dart 2.15 or newer).
- Use `void Function()?` for an optional callback and call it with `cb?.call()`.
Verify: pass a callable object to `map`.

## Checked

Date: 2026-11-02. Confirmed on the Typedefs page: typedefs for non-function types need language version 2.13 (before 2.13 only function types); Callable objects page: `call()`; Dart 2.15 announcement: constructor tear-offs; Core libraries page: null-aware `?.call`.

Method: documentation only; no commands were run.
