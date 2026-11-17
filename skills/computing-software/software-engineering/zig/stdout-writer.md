---
id: computing-software.software-engineering.zig.stdout-writer
name: stdout-writer
category: computing-software
field: software-engineering
product: zig
tags: [zig, stdout-writer, zig-std-io, stdout, bufferedwriter, std-io-writer, flush]
level: practitioner
status: docs-checked
description: "Write program output in Zig using a buffered stdout writer, stderr via std.debug.print, and the 0.15 std.Io.Writer change."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/fs/File.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Io/Writer.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/debug.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing to stdout and stderr with buffering
**Goal:** emit output correctly with the 0.15 writer interface.

```zig
var buf: [4096]u8 = undefined;
var stdout_writer = std.fs.File.stdout().writer(&buf);
const w = &stdout_writer.interface;
try w.print("n={d}\n", .{5});
try w.flush();
```
- `std.fs.File.stdout()` returns a `File`; `File.writer(buffer)` returns a `File.Writer` whose `interface` field is the `std.Io.Writer`. The buffer is supplied by the caller.
- `std.Io.Writer` has `print(fmt, args)` and `flush()`; flush the buffer before exit.
- `std.debug.print(fmt, args)` writes to stderr for diagnostics.
- The language reference's hello world is `try std.fs.File.stdout().writeAll("Hello, World!\n");`.
- `std.io.getStdOut()` and `std.io.bufferedWriter` do not appear anywhere in the 0.15.1 standard library source; `std.io` is an alias of `std.Io`, which holds `Reader`, `Writer` and a deprecated writer.

## Gotchas
- Posts and code written before 0.15 may not compile; check `zig version`.

## Self-check
Print many lines through the buffered writer, call `flush`, and confirm the output is complete.

## Checked
2026-11-02. Confirmed in 0.15.1 `lib/std/fs/File.zig` (`stdout`, `writer`, `Writer.interface`), `lib/std/Io/Writer.zig` (`print`, `flush`), `lib/std/debug.zig` (`print`) and `doc/langref/hello.zig`.
Removed: the pre-0.15 code block, "one syscall per write" performance claim, `std.log` remark, timing self-check.
Method: documentation only; no commands were run.
