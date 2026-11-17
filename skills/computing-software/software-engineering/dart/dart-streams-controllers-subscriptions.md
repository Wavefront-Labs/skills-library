---
id: computing-software.software-engineering.dart.dart-streams-controllers-subscriptions
name: dart-streams-controllers-subscriptions
category: computing-software
field: software-engineering
product: dart
tags: [dart, streams-controllers-subscriptions]
level: advanced
status: docs-checked
description: "Create and consume Dart Streams: async*, StreamController, listen/await for, broadcast and cancellation."
sources: ["https://dart.dev/libraries/async/creating-streams", "https://dart.dev/libraries/async/using-streams", "https://dart.dev/language/async"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streams
- `Stream<int> count() async* { for (...) yield i; }`; consume with `await for (final x in s)` or `s.listen(onData, onError, onDone, cancelOnError: true)`.
- `StreamController<T>()` single-subscription; `.broadcast()` allows many listeners; always `close()` and `subscription.cancel()` to avoid leaks.
- Transform: `map`, `where`, `asyncMap`, `StreamTransformer`; `Stream.periodic`.
Verify: cancel stops callbacks and onCancel fires.

## Checked

Date: 2026-11-02. Confirmed on the Creating streams, Using streams and Asynchronous programming pages: `async*`, `await for`, `listen` with `onError`, `onDone` and `cancelOnError`, single-subscription vs broadcast, `close()`, `onCancel`, `asyncMap`, `StreamTransformer`, `Stream.periodic`.

Method: documentation only; no commands were run.
