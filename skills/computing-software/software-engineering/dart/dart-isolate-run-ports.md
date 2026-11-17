---
id: computing-software.software-engineering.dart.dart-isolate-run-ports
name: dart-isolate-run-ports
category: computing-software
field: software-engineering
product: dart
tags: [dart, isolate-run-ports]
level: advanced
status: docs-checked
description: "Offload CPU work with Isolate.run, spawn long-lived isolates with SendPort/ReceivePort, and know what can be sent."
sources: ["https://dart.dev/language/isolates", "https://dart.dev/language/concurrency"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Isolates
- `final r = await Isolate.run(() => heavy(data));` spawns a worker, runs the function (a named function or a closure), captures and rethrows exceptions in the main isolate, returns the result as a `Future`, and shuts the worker down. The result's memory is transferred rather than copied, after a verification pass that the objects may be transferred. In Flutter, `compute` is the equivalent.
- Short-lived isolates cost spawn time and object copying; for repeated work keep a long-lived isolate using `Isolate.spawn()`, `Isolate.exit()`, `ReceivePort` and `SendPort`.
- Ports are the only way isolates communicate. A `SendPort` belongs to exactly one `ReceivePort`; one `ReceivePort` can have many `SendPort`s; receive ports implement `Stream`. Two-way handshake: main creates a `ReceivePort` and passes its `sendPort` to `Isolate.spawn`; the worker creates its own `ReceivePort` and sends its `sendPort` back as the first message.
- Isolates have their own memory and event loop and cannot see each other's memory. A spawned isolate only knows what it receives through the `Isolate.spawn` call.
- With several in-flight requests, responses return in completion order, so tag requests with an id mapped to a `Completer`.

Verify: a UI-style loop stays responsive while the isolate computes.

## Checked

Checked 2026-11-08 against https://dart.dev/language/isolates (sections on Isolate.run, closures, long-lived isolates, ports, worker examples; read the cited sections, not every code listing) and https://dart.dev/language/concurrency (isolate memory and event loop). Removed (not confirmed): the claim that closures must not capture non-sendable objects, TransferableTypedData transfer semantics, the claim about sockets/ports/native objects being unsendable, and "no global state".

Method: documentation only; no commands were run.
