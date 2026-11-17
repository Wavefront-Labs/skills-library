---
id: computing-software.software-engineering.dart.dart-sync-star-generators
name: dart-sync-star-generators
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-generators, sync-star-generators]
level: practitioner
status: docs-checked
description: "Write lazy sequences with sync* and yield*, and know when to use Iterable versus List."
sources: ["https://dart.dev/language/functions", "https://dart.dev/libraries/async/creating-streams", "https://dart.dev/libraries/dart-core"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sync* and async* generator functions
- `Iterable<int> naturals() sync* { var i = 0; while (true) yield i++; }` is lazy and re-runs on each iteration.
- `yield*` delegates to another iterable; recursive generators work but each level adds overhead.
- Implement `Iterable` via `IterableBase` for custom collections; return `Iterable<T>` from APIs that don't need list semantics.
Verify: add a side effect inside the generator and count executions.

## Checked

Date: 2026-11-02. Confirmed on the Functions page (Generators section): `sync*` returns a lazily produced Iterable, `yield`, `yield*` to improve recursive generators; Core libraries and Effective Dart pages: `IterableBase`. Removed the `take`/`toList` claim (not stated).

Method: documentation only; no commands were run.
