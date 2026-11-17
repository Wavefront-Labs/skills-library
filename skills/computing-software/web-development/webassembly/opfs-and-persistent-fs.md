---
id: computing-software.web-development.webassembly.opfs-and-persistent-fs
name: opfs-and-persistent-fs
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, origin-private-file-system, idbfs, sqlite-wasm, wasm-opfs, indexeddb-wasm, wasm-file-system, wasm]
level: practitioner
status: docs-checked
description: "Persist data from Wasm using the Origin Private File System: synchronous access handles in dedicated workers and their exclusive lock."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/FileSystemFileHandle/createSyncAccessHandle
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OPFS and persistent filesystems

Goal: persist data from Wasm.
- `FileSystemFileHandle.createSyncAccessHandle()` returns a `FileSystemSyncAccessHandle` for synchronous read and write of a file. It is only usable inside dedicated Web Workers, for files in the origin private file system, and requires a secure context. The synchronous nature brings performance advantages, which suits Wasm code that expects blocking file I/O.
- Creating the handle takes an exclusive lock on the file: no further sync access handles or `FileSystemWritableFileStream`s can be created for it until the handle is closed. With the default `"readwrite"` mode, a second simultaneous handle throws.
- Run the Wasm module in the worker that owns the handle, and message the main thread with `postMessage`.
Verify: data survives reload.

## Checked
Read the first sections (intro, parameters, exceptions, worker example) of the MDN createSyncAccessHandle page on 2026-11-08; the main-thread demo was only skimmed. Confirmed the dedicated-worker restriction, OPFS scope, secure context, exclusive lock behaviour and default mode. Removed: Emscripten IDBFS, SQLite Wasm OPFS VFS, and quota and eviction claims (no cited page read for them), and the generic spec, component-model and WASI sources.
Method: docs-only read of cited pages, 2026-11-08
