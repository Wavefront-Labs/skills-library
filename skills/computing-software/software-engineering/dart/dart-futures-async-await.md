---
id: computing-software.software-engineering.dart.dart-futures-async-await
name: dart-futures-async-await
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-async, futures-async-await]
level: practitioner
status: docs-checked
description: "Write correct async code with await, Future.wait, timeouts and error propagation."
sources: ["https://dart.dev/language/async", "https://dart.dev/libraries/async/async-await", "https://dart.dev/libraries/async/futures-error-handling", "https://dart.dev/libraries/dart-async"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Future, async/await and error handling
- `Future<int> f() async => 1;` an `async` function always returns a Future; the `unawaited_futures` linter rule flags futures that are not awaited.
- `await Future.wait([a(), b()])` waits for all the futures to complete before continuing.
- `try { await f(); } on TimeoutException catch (e) {} catch (e, st) {}`.
- Each isolate runs its own event loop (see the Concurrency page).
Verify: an `await Future.wait([...])` result list has one value per future.

## Checked

Date: 2026-11-02. Confirmed on the Asynchronous programming, Async and await and dart:async pages: async functions return Futures, `unawaited_futures` lint, `Future.wait`, try/on/catch with stack trace; Concurrency page: per-isolate event loop. Removed as not stated: `eagerError`, the records `.wait` form, `future.timeout`, microtask ordering, `fake_async` and the blocking advice.

Method: documentation only; no commands were run.
