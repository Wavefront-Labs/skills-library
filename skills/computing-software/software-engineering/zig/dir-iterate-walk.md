---
id: computing-software.software-engineering.zig.dir-iterate-walk
name: dir-iterate-walk
category: computing-software
field: software-engineering
product: zig
tags: [zig, dir-iterate-walk, zig-std-fs, dir-iterate, walker, std-fs-path, makepath]
level: practitioner
status: docs-checked
description: "Iterate and recursively walk directories in Zig with openDir iterate and walk, and manipulate paths with std.fs.path."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/fs/Dir.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/fs.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/fs/path.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/fs/get_app_data_dir.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/testing.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Directory iteration, walking and path handling
**Goal:** list, walk and build paths portably.

```zig
var dir = try std.fs.cwd().openDir("src", .{ .iterate = true });
defer dir.close();
var it = dir.iterate();
while (try it.next()) |entry| {              // entry.name, entry.kind
    if (entry.kind == .file) std.debug.print("{s}\n", .{entry.name});
}
var walker = try dir.walk(alloc);
defer walker.deinit();
while (try walker.next()) |e| std.debug.print("{s}\n", .{e.path});   // relative path
```
- `.iterate = true` (an `OpenOptions` field) is required to list entries; `dupe` any name you keep beyond the loop.
- `makeDir`, `makePath` (recursive), `deleteTree`, `rename`, `copyFile`, `symLink`, `realpathAlloc`, `access`.
- `std.fs.path.join(alloc, &.{ "a", "b", "c.txt" })`, `basename`, `dirname`, `extension`, `stem`, `isAbsolute`, `resolve`.
- `std.fs.selfExePathAlloc`, `std.fs.getAppDataDir(alloc, "app")` for per-user config dirs.
- `std.fs.Dir.openDir(.{ .no_follow = true })` for symlink safety.

## Gotchas
- Windows long paths and drive letters: treat paths as opaque.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `Dir.iterate`, `walk` (`Walker.Entry.path`), `openDir` with `iterate` and `no_follow`, `makeDir`, `makePath`, `deleteTree`, `rename`, `copyFile`, `symLink`, `access`, `realpathAlloc`, `fs.path.join/basename/dirname/extension/stem/isAbsolute/resolve`, `fs.selfExePathAlloc`, `getAppDataDir`, `testing.tmpDir`. Removed: unverifiable symlink and delete-while-iterating remarks.

Method: documentation only; no commands were run.

## Self-check
Walk a temp dir you created with `std.testing.tmpDir(.{})` and count files.
