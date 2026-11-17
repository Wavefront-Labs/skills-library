---
id: computing-software.web-development.node-express.fs-promises-and-path-handling
name: fs-promises-and-path-handling
category: computing-software
field: web-development
product: node-express
tags: [node, fs-promises, path, atomic-writes, import-meta-dirname, file-system, path-traversal, web-development]
level: practitioner
status: verified
description: "Working with files in Node via fs/promises and path: absolute paths from import.meta, atomic writes, recursive mkdir/rm, directory walking, error codes and traversal checks."
sources:
  - https://nodejs.org/api/fs.html#promises-api
  - https://nodejs.org/api/path.html
  - https://nodejs.org/api/esm.html#importmetadirname
  - https://nodejs.org/api/errors.html#common-system-errors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fs/promises and path handling

**Goal:** file code that works regardless of cwd and OS, never corrupts files on crash, and can't be tricked into escaping its directory.

## 1. Imports and base paths
```js
import { readFile, writeFile, mkdir, rm, rename, stat, opendir } from "node:fs/promises";
import path from "node:path";
const dataDir = path.join(import.meta.dirname, "data");     // ESM, Node 20.11+; CJS: __dirname
```
Relative paths in `fs` calls resolve against `process.cwd()`, which changes with how the process is started.

## 2. Reading and writing
```js
const cfg = JSON.parse(await readFile(path.join(dataDir, "config.json"), "utf8"));
await mkdir(path.join(dataDir, "out"), { recursive: true });                 // no error if exists
await writeFile(file, data, { flag: "wx" });                                 // fail if exists (EEXIST)
await rm(tmpDir, { recursive: true, force: true });                          // rimraf replacement
```
Avoid the `exists()` then act pattern (race); just try and handle the error code.

## 3. Atomic writes
```js
async function writeAtomic(file, data) {
  const tmp = `${file}.${process.pid}.${Date.now()}.tmp`;
  await writeFile(tmp, data);
  await rename(tmp, file);           // atomic on the same filesystem
}
```
A crash mid-`writeFile` leaves a truncated file; rename never does. For durability across power loss, `fsync` via a `FileHandle` before renaming.

## 4. Error codes
```js
try { await stat(p); } catch (e) { if (e.code === "ENOENT") return null; throw e; }
```
Common: `ENOENT` missing, `EEXIST`, `EACCES`/`EPERM` permissions, `EISDIR`, `EMFILE` too many open files (use streams/limits), `EBUSY` (Windows locks).

## 5. Walking directories
```js
for await (const d of await opendir(root, { recursive: true })) { if (d.isFile()) ... }   // recursive since 20.1
for await (const f of glob("src/**/*.ts")) { ... }       // import { glob } from "node:fs/promises", Node 22+
```
`readdir(dir, { withFileTypes: true })` avoids an extra `stat` per entry.

## 6. path pitfalls
- `path.join("a", "/b")` -> `a/b`; `path.resolve("a", "/b")` -> `/b` (absolute resets).
- Use `path.posix` for URLs/zip entries; `path` follows the host OS.
- `fileURLToPath(new URL("./x", import.meta.url))` for URL-based resolution.

## 7. Traversal guard for user input
```js
const base = path.resolve(uploadsDir);
const target = path.resolve(base, userName);
if (!target.startsWith(base + path.sep)) throw new Error("invalid path");
```
Also reject NUL bytes; consider `realpath` if symlinks may exist inside the base.

## Verify
- [ ] Running the app from a different cwd still finds its files.
- [ ] Killing the process during a write never leaves a half-written target.
- [ ] `../../etc/passwd` style input is rejected.

## Checked
- Node 24.22.0 and 20.20.2 on Windows: `import.meta.dirname` is a string on both; `mkdir` with `recursive` twice is fine; `writeFile` with `flag: "wx"` fails the second time with `EEXIST`; `stat` on a missing file gives `ENOENT`, reading a directory `EISDIR`; `rm` with `force` ignores a missing path and without it throws `ENOENT`; the atomic temp-file rename leaves no `.tmp`; `opendir` with `recursive` lists nested files on 20 and 24 (20.1 per the docs); `fs.promises.glob` exists on 24 and not on 20 (22+); `readdir` with `withFileTypes`; `path.join("a", "/b")` joins while `path.resolve("a", "/b")` resets (and `path.posix` behaves the same way on any OS); the `startsWith(base + sep)` guard rejects `../`, `..`, `.`, a sibling `uploads2`, absolute and drive paths, but accepts a string with a NUL byte, which `fs` then rejects with `ERR_INVALID_ARG_VALUE`, so check NUL explicitly. `fsync` before rename and symlink escapes were not exercised.
