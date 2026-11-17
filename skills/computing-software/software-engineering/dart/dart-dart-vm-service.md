---
id: computing-software.software-engineering.dart.dart-dart-vm-service
name: dart-dart-vm-service
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-hot-reload-vm, dart-vm-service]
level: advanced
status: docs-checked
description: "Debug command-line Dart apps with dart run --observe, --pause-isolates-on-start, --enable-asserts and DevTools."
sources: ["https://dart.dev/tools/dart-run", "https://dart.dev/tools/dart-devtools"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dart run debugging flags and DevTools
- `dart run --observe main.dart` enables debugging and performance analysis through Dart DevTools and prints a DevTools URL.
- Add `--pause-isolates-on-start` to break execution at the start of the script: `dart run --pause-isolates-on-start --observe main.dart`.
- `dart run --enable-asserts` turns on `assert` statements.
- The printed URL contains a security token and changes on every run; open it in Chrome to use the debugger and profiler. Treat the URL as a credential and do not share it.
Verify: restart the app, copy the new URL and confirm DevTools connects.

## Checked
2026-11-03. Confirmed against dart.dev tools/dart-run (`--enable-asserts`, `--observe`) and tools/dart-devtools (`--pause-isolates-on-start`, token in URL, new URL each run). Removed: `--enable-vm-service`, `--disable-service-auth-codes`, `package:hotreloader`, the hot reload and remote code execution claims (not on the pages read).
Method: documentation only; no commands were run.
