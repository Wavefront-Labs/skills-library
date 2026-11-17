---
id: computing-software.web-development.frontend-development.origin-private-file-system
name: origin-private-file-system
category: computing-software
field: web-development
product: frontend-development
tags: [client-side-storage, opfs, origin-private-file-system, file-system-access, createsyncaccesshandle, sqlite-wasm]
level: practitioner
status: docs-checked
description: "Using the Origin Private File System for fast file-like storage, sync access handles in workers, and running SQLite WASM on OPFS."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system
  - https://web.dev/articles/origin-private-file-system
  - https://sqlite.org/wasm/doc/trunk/persistence.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Origin Private File System (OPFS)

**Goal:** store large binary or database files per origin with file semantics and fast synchronous I/O in a worker.

## 1. What it is
A secure-context storage endpoint private to the page's origin and not visible to the user (MDN). It is subject to browser storage quotas like other origin storage, and is evicted with other origin data unless persistence was granted.

## 2. Async API (main thread or worker)
```js
const root = await navigator.storage.getDirectory();
const dir = await root.getDirectoryHandle('exports', { create: true });
const fh = await dir.getFileHandle('report.json', { create: true });
const w = await fh.createWritable();
await w.write(JSON.stringify(data)); await w.close();      // data visible only after close
const text = await (await fh.getFile()).text();
for await (const [name, handle] of dir.entries()) console.log(name, handle.kind);
await dir.removeEntry('report.json');
```
`createWritable` is typically implemented by writing to a temporary file and replacing the original only when the stream is closed; only one writer can be open at a time (a second throws `NoModificationAllowedError`).

## 3. Sync access handles (workers only) - the fast path
```js
// inside a dedicated worker
const fh = await (await navigator.storage.getDirectory()).getFileHandle('db.bin', { create: true });
const h = await fh.createSyncAccessHandle();
h.write(new Uint8Array([1,2,3]), { at: 0 });
const buf = new Uint8Array(3); h.read(buf, { at: 0 });
h.flush(); h.close();
```
Creating a handle takes an exclusive lock on the file: opening another handle before the first is closed throws `NoModificationAllowedError` (also across tabs). `createSyncAccessHandle()` is usable only inside dedicated workers. Coordinate tabs with Web Locks.

## 4. SQLite in the browser
The official SQLite WASM build has OPFS VFSes; run it in a worker. Per the SQLite WASM persistence docs, the `opfs` VFS needs the COOP and COEP headers (it relies on SharedArrayBuffer) and supports multi-tab concurrency (as does `opfs-wl`); the `opfs-sahpool` VFS does not need COOP/COEP, has the highest OPFS performance of the documented options, and trades away multi-tab concurrency.

## 5. vs. other storage
OPFS for files/blobs and databases; IndexedDB for structured records with indexes; Cache API for HTTP responses. The File System Access picker API (`showOpenFilePicker`) is different: it works on user-visible files and is slower because of security checks; check MDN's compatibility table before relying on it.

## Verify
- [ ] Write/read round-trip in a worker; data survives reload.
- [ ] Two tabs: the second fails gracefully or waits for the lock.
- [ ] `navigator.storage.estimate()` usage grows by the file size.

## Checked

Checked 2026-10-26 against MDN Origin private file system, FileSystemFileHandle.createWritable() and createSyncAccessHandle(), FileSystemSyncAccessHandle (mdn/content main) and the SQLite WASM persistence documentation (sqlite.org/wasm/doc/trunk/persistence.md): secure context, quota, dedicated-worker restriction, exclusive lock and `NoModificationAllowedError`, temporary-file write semantics, and the `opfs` versus `opfs-sahpool` COOP/COEP and concurrency trade-offs. Removed the unconfirmed 'all current engines' and 'Chromium-only' statements.

Method: documentation only; no commands were run.
