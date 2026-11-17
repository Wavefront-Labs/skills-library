---
id: computing-software.software-engineering.dart.dart-iterable-operations
name: dart-iterable-operations
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-collections, iterable-operations]
level: practitioner
status: docs-checked
description: "Chain where, map and whereType lazily and force evaluation with toList when needed."
sources: ["https://dart.dev/libraries/dart-core", "https://dart.dev/effective-dart/usage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Iterable, where, map and lazy evaluation
- `List` and `Set` implement `Iterable`, which provides the shared methods. `map()` returns a lazily evaluated `Iterable`: your function is not called until an item is requested. Force it immediately with `map(...).toList()` or `.toSet()`, and do that once when the results are reused.
- `where()` selects matching items; `any()` and `every()` test whether some or all items match a condition.
- Use `whereType<T>()` instead of `where((e) => e is T).cast<T>()`: it is concise, produces an `Iterable<T>` and avoids extra wrapping and redundant runtime checks (lint `prefer_iterable_whereType`).
- `cast()` returns a lazy collection that checks element types on every operation, so its overhead can outweigh the benefit; Effective Dart says to avoid `cast()` when a nearby transformation or an eager `List.from()` can fix the type.

Verify: add a print in the mapped function and observe repeated calls when iterating the result twice.

## Checked

Checked 2026-11-08 against the collections and Iterable sections of https://dart.dev/libraries/dart-core and the collections guidelines of https://dart.dev/effective-dart/usage (whereType and cast sections read; the page is large and was not read end to end). Removed (not confirmed in pages read): `fold`, `reduce`, `firstWhere(orElse:)`, `singleWhere`, `expand`, `take`, `skip` laziness details and the `package:collection` helper list.

Method: documentation only; no commands were run.
