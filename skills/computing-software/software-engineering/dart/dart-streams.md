---
id: computing-software.software-engineering.dart.dart-streams
name: dart-streams
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-async, streams]
level: practitioner
status: docs-checked
description: "Produce and consume streams with async*, StreamController, listen and await for, and choose single versus broadcast streams."
sources: ["https://dart.dev/libraries/async/creating-streams", "https://dart.dev/libraries/async/using-streams", "https://dart.dev/language/async"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streams, StreamController and async*
- `Stream<int> count() async* { for (var i = 0; i < 3; i++) yield i; }`; consume with `await for (final v in s)` or `s.listen(onData, onError:, onDone:)`.
- A single-subscription stream can be listened to once; broadcast streams allow more than one listener at a time.
- Always `cancel()` subscriptions and `close()` controllers to avoid leaks.
- Transform with `map`, `where`, `asyncMap`, `StreamTransformer`.
Verify: a test that cancels the subscription and checks the controller `onCancel`.

## Checked

Date: 2026-11-02. Confirmed on the Creating streams and Using streams pages: `async*` with `yield`, `await for`, `listen` with `cancelOnError`, single-subscription streams listened to once, broadcast streams with several listeners, `asyncMap`, `StreamTransformer`, `onCancel`, `close()`. Removed as not stated: `asBroadcastStream()`, `package:rxdart` and the lost-events detail for broadcast streams.

Method: documentation only; no commands were run.
