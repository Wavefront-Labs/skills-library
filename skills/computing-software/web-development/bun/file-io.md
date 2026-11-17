---
id: computing-software.web-development.bun.file-io
name: file-io
category: computing-software
field: web-development
product: bun
tags: [bun-file, bun-write, file-sink, node-fs-directories]
level: intro
status: docs-checked
description: "Read and write files with Bun.file, Bun.write and incremental FileSink writers; handle missing files, stdin and stdout, deletion and directory work via node:fs."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/file-io.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
const f = Bun.file("foo.txt");        // lazy; nothing read yet
f.size; f.type;
await f.text(); await f.json(); await f.bytes(); f.stream(); await f.arrayBuffer();

await Bun.write("output.txt", "text");        // returns bytes written
await Bun.write("copy.txt", Bun.file("foo.txt"));
await Bun.write("index.html", response);      // fetch body to disk
await Bun.write(Bun.stdout, Bun.file(path));

const w = Bun.file("output.txt").writer({ highWaterMark: 1024 * 1024 });
w.write("chunk\n"); w.flush(); w.end();

await Bun.file("logs.json").delete();
```

Directories use `node:fs`:

```ts
import { readdir, mkdir } from "node:fs/promises";
await mkdir("path/to/dir", { recursive: true });
```

Gotchas:
- A `BunFile` for a missing path has `size` 0 and `exists()` resolves false.
- Default `type` is `text/plain;charset=utf-8` unless you pass `{ type }`.
- A `FileSink` keeps the process alive until `.end()` unless `unref()`; data stays buffered until `flush()`, the high water mark, or `end()`.
- `Bun.stdin` is readonly. Relative paths resolve against the current working directory.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/file-io: lazy Bun.file, Blob-style readers, missing-file size 0 and exists() false, default type text/plain;charset=utf-8 with the type override, readonly Bun.stdin, delete(), Bun.write destinations and inputs returning a byte count, copy and stdout and Response examples, FileSink write/flush/end/ref/unref with highWaterMark auto-flush, process staying alive until end(), and directory work via node:fs readdir and mkdir with recursive. Nothing removed.
Method: documentation only; no commands were run.
