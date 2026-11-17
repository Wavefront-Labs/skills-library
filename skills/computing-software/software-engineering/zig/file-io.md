---
id: computing-software.software-engineering.zig.file-io
name: file-io
category: computing-software
field: software-engineering
product: zig
tags: [zig, file-io, zig-std-fs, std-fs, openfile, createfile, readfilealloc]
level: practitioner
status: docs-checked
description: "Open, read and write files in Zig with std.fs.cwd, openFile, createFile, readFileAlloc and defer close, handling common errors."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/fs/Dir.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/fs/File.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/fs.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Opening, reading and writing files
**Goal:** read and write whole files and streams.

```zig
const cwd = std.fs.cwd();
const data = try cwd.readFileAlloc(alloc, "in.txt", 10 * 1024 * 1024);   // (allocator, path, max_bytes: usize)
defer alloc.free(data);

const f = try cwd.createFile("out.txt", .{ .truncate = true });
defer f.close();
try f.writeAll("hello\n");

const g = cwd.openFile("in.txt", .{}) catch |e| switch (e) {
    error.FileNotFound => return,          // handle expected errors explicitly
    else => return e,
};
defer g.close();
const stat = try g.stat();                 // .size, .kind, .mtime
```
- `std.fs.cwd()` returns a `Dir`; absolute paths via `std.fs.openFileAbsolute`.
- `file.writer(&buffer)` and `file.reader(&buffer)` take an explicit buffer slice in 0.15.1.
- Atomic replace: `cwd.atomicFile("out.txt", .{})` returns an `AtomicFile` (see `Dir.atomicFile`; its `dest_path` must stay valid until `finish`).
- `std.fs.File.stdin()` and `std.fs.File.stdout()` return the standard streams in 0.15.1.

## Gotchas
- In 0.15.1 `File.reader(buffer)`/`File.writer(buffer)` take an explicit buffer; `file.deprecatedReader()`/`deprecatedWriter()` give the old style.
- Windows path separators: use `std.fs.path.join`, never hand-built strings.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `Dir.readFileAlloc(allocator, path, max_bytes)`, `createFile` (`truncate` defaults to true), `openFile`, `deleteFile`, `atomicFile`, `File.stat` (`size`, `kind`, `mtime`), `File.stdin/stdout`, `File.reader/writer(buffer)`, `fs.openFileAbsolute`. Removed: `posix.mmap` and `error.IsDir` claims.

Method: documentation only; no commands were run.

## Self-check
Write a file, read it back with a size limit, compare contents, delete with `cwd.deleteFile`.
