---
id: computing-software.software-engineering.dart.dart-file-process-io
name: dart-file-process-io
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-json-io, file-process-io]
level: practitioner
status: docs-checked
description: "Read and write files and list directories with dart:io, and prefer async APIs."
sources: ["https://dart.dev/libraries/dart-io"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File and Directory with dart:io
- `dart:io` favours asynchronous APIs: most operations return a `Future` or `Stream`, and synchronous methods can block the application.
- `await file.readAsString()` reads a UTF-8 text file whole; `readAsLines()` returns the lines. Both return a `Future`.
- `file.openWrite()` returns an `IOSink`; the default `FileMode.write` overwrites the file, `openWrite(mode: FileMode.append)` appends.
- `Directory.list()` returns a `Stream` that emits each file or directory found.
- Do not use `dart:io` `HttpClient` directly for HTTP requests; the page recommends a higher-level library such as `package:http`.
Verify: tests write to a temporary directory and read the result back.

## Checked
2026-11-03. Confirmed against dart.dev libraries/dart-io (async-first design, readAsString, readAsLines, openWrite and modes, Directory.list, HttpClient advice). Removed: `Process.run`, `Process.start`, `runInShell`, stdin/stdout, `exit`, `Platform.environment`, `createSync(recursive:)`, `package:path` and `Directory.systemTemp` claims (not on the page read).
Method: documentation only; no commands were run.
