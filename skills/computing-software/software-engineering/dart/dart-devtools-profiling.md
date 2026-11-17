---
id: computing-software.software-engineering.dart.dart-devtools-profiling
name: dart-devtools-profiling
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-memory-performance, devtools-profiling]
level: advanced
status: docs-checked
description: "Observe a Dart command-line app with dart run --observe and DevTools; AOT versus JIT output."
sources: ["https://dart.dev/tools/dart-devtools", "https://dart.dev/tools/dart-compile", "https://dart.dev/tools/dart-tool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DevTools profiling
- `dart run --observe main.dart` prints a DevTools URL; open it in Chrome to use the debugger and profiler, and view the timeline, memory and performance of the running app. `dart devtools` also opens DevTools.
- Web apps cannot use the timeline, memory and performance views; use browser tools such as Chrome DevTools.
- `dart run` uses the VM's JIT compiler; `dart compile` produces AOT output (for example `aot-snapshot`). Measure the mode you will ship, and compare before and after on the same machine.
Verify: record before and after numbers in the same mode.

## Checked
2026-11-03. Confirmed against dart.dev tools/dart-devtools (`--observe`, views, web limits), tools/dart-tool (`dart devtools`) and tools/dart-compile (JIT versus AOT, `aot-snapshot`). Removed: `package:benchmark_harness`, the list of micro-optimisations and the leak list (not on the pages read).
Method: documentation only; no commands were run.
