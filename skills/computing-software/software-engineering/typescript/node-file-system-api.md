---
id: computing-software.software-engineering.typescript.node-file-system-api
name: node-file-system-api
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, node-fs, fs-promises, file-watching, atomic-write, nodejs, file-streams]
level: practitioner
status: verified
description: "Use Node's fs module well: fs/promises vs sync vs callbacks, reading and writing safely, recursive mkdir/rm/readdir/glob, file handles, atomic writes, watching and path pitfalls."
sources: ["https://nodejs.org/api/fs.html", "https://nodejs.org/api/path.html", "https://nodejs.org/api/fs.html#fspromisesglobpattern-options"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node file system API

**Goal:** file I/O that doesn't block the event loop, doesn't leak handles and doesn't
corrupt files on crash.

## Which API
```ts
import { readFile, writeFile, mkdir, rm, readdir, rename, stat } from "node:fs/promises";
import { readFileSync } from "node:fs";
```
- `fs/promises` in servers and anything concurrent.
- Sync APIs are fine in CLIs and at startup (config load), never in request handlers.
- Large files: streams (`createReadStream` + `pipeline`), not `readFile` (whole file in memory,
  `fs.readFile` rejects files over 2 GiB with `ERR_FS_FILE_TOO_LARGE`; that is an I/O limit, not a Buffer limit, per the Node errors docs; `buffer.constants.MAX_LENGTH` is 2^53-1 on 64-bit since Node 22).

## Common operations
```ts
const text = await readFile(path, "utf8");
await mkdir(dir, { recursive: true });                    // no error if it exists
await rm(dir, { recursive: true, force: true });
const entries = await readdir(dir, { withFileTypes: true, recursive: true });   // Node 20+
for await (const f of glob("src/**/*.ts")) { ... }        // fs/promises glob, Node 22+; add glob to the import above (tested on 24, absent on Node 20)
const exists = await stat(p).then(() => true, (e) => (e.code === "ENOENT" ? false : Promise.reject(e)));
```
Avoid check-then-act (`existsSync` then `writeFile`): race-prone. Just attempt the operation
and handle `ENOENT`/`EEXIST` (`writeFile(p, d, { flag: "wx" })` fails if it exists).

## Atomic writes
```ts
import { randomUUID } from "node:crypto";
async function writeAtomic(p: string, data: string) {
  const tmp = `${p}.${randomUUID()}.tmp`;
  await writeFile(tmp, data);
  await rename(tmp, p);          // atomic on the same filesystem (POSIX); Windows replaces too
}
```
For durability, write the temp file through a writable handle and `sync()` it before the rename:
```ts
{ await using fh = await open(tmp, "w"); await fh.writeFile(data); await fh.sync(); }
await rename(tmp, p);
```
Tested: `fh.sync()` on a handle opened with `"r"` fails with `EPERM` on Windows, so do not sync a read-only handle.

## File handles
```ts
import { open } from "node:fs/promises";
await using fh = await open(p, "r");          // explicit resource management (TS 5.2 / Node 24; tested: Node 20 gives a SyntaxError)
// or: const fh = await open(p); try { ... } finally { await fh.close(); }
```
Leaking handles -> `EMFILE: too many open files` under load.

## Paths
- ESM has no `__dirname`: use `import.meta.dirname` (Node 20.11+) or
  `fileURLToPath(new URL(".", import.meta.url))`.
- Build paths with `path.join`/`path.resolve`, never string concatenation; resolve user input
  and check it stays under a root (`path.relative(root, p).startsWith("..")` -> reject).

## Watching
`fs.watch` (OS events; recursive on macOS/Windows and Linux in Node 20+) fires duplicate and
platform-specific events; debounce. `chokidar` smooths cross-platform differences; for dev
reloads use `node --watch`.

## Verify
- [ ] No `*Sync` fs calls in request paths (lint rule `n/no-sync` or grep).
- [ ] Path traversal test: `../../etc/passwd` input is rejected.
