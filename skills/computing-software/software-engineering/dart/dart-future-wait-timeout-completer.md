---
id: computing-software.software-engineering.dart.dart-future-wait-timeout-completer
name: dart-future-wait-timeout-completer
category: computing-software
field: software-engineering
product: dart
tags: [dart, future-wait-timeout-completer]
level: advanced
status: docs-checked
description: "Coordinate Dart futures: Future.wait, iterable and record wait, ParallelWaitError, and unawaited."
sources: ["https://dart.dev/libraries/dart-async", "https://dart.dev/tools/linter-rules/unawaited_futures"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Futures
- `await Future.wait([a(), b(), c()])` starts nothing itself but waits for futures you already started (they run concurrently) and completes with their results, or with an error if any provided future fails.
- `await [a(), b()].wait` (iterable) and `await (a(), b()).wait` (record, so the futures may have different types and you destructure the result) also handle errors: if any future fails, `wait` completes with a `ParallelWaitError` whose `values` hold successful results (null for failures) and `errors` hold the `AsyncError`s (null for successes).
- Install error handlers before a future completes; for `then().catchError()` chains an error skips later `then` callbacks and reaches `catchError`; `whenComplete` is the `finally` equivalent.
- Fire-and-forget: the `unawaited_futures` lint requires future results in async function bodies to be awaited or wrapped in `unawaited()` from `dart:async`; `// ignore: unawaited_futures` also works. Enable it under `linter > rules` in `analysis_options.yaml`.

Verify: a failing future inside the iterable `.wait` surfaces a `ParallelWaitError`.

## Checked

Checked 2026-11-08 against https://dart.dev/libraries/dart-async (waiting for multiple futures and error-handling sections), the Futures and Error Handling page, and the unawaited_futures linter rule page. Removed (not confirmed in any page read): the `timeout(..., onTimeout:)` non-cancellation claim, the `Completer` once-only claim, the claim that unawaited futures swallow errors, and the Dart 3 version note for record wait.

Method: documentation only; no commands were run.
