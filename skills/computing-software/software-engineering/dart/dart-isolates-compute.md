---
id: computing-software.software-engineering.dart.dart-isolates-compute
name: dart-isolates-compute
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-isolates, isolates-compute]
level: advanced
status: docs-checked
description: "Offload CPU-bound work with Isolate.run, communicate by ports and know the web and sharing limits."
sources: ["https://dart.dev/language/concurrency", "https://dart.dev/language/isolates"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Isolate.run, ports and worker isolates
- All Dart code runs in isolates. Each isolate has its own memory, its own global fields and a single thread running an event loop; isolates communicate only by message passing, so there are no data races on shared state (race conditions are still possible).
- `final r = await Isolate.run(() => heavy(data));` spawns a worker, runs the function, returns the result or rethrows the error, and shuts the worker down. The result's memory is transferred rather than copied after a check that the objects may be transferred. Flutter's `compute` is the equivalent.
- Passing messages between isolates copies the data; repeatedly spawning short-lived isolates adds spawn and copy cost, so for repeated work use a long-lived worker: `Isolate.spawn(entry, sendPort)` with a `ReceivePort`/`SendPort` handshake.
- `async`/`await`, `Future` and `Stream` give non-blocking interleaving on one isolate's event loop, not extra cores.
- The Dart web platform does not support isolates; use web workers, which copy data between threads and cannot be started like `Isolate.spawn`.

Verify: compare wall-clock time with and without the isolate on a CPU-heavy task.

## Checked

Checked 2026-11-08 against https://dart.dev/language/concurrency (isolates and "Concurrency on the web" sections read) and https://dart.dev/language/isolates (Isolate.run and long-lived worker sections). Removed (not confirmed): the Dart 2.19 version gate, the message type allow-list, and `TransferableTypedData`.

Method: documentation only; no commands were run.
