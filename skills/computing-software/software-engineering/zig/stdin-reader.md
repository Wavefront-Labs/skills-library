---
id: computing-software.software-engineering.zig.stdin-reader
name: stdin-reader
category: computing-software
field: software-engineering
product: zig
tags: [zig, stdin-reader, zig-std-io, stdin, readuntildelimiter, readline, bufferedreader]
level: practitioner
status: docs-checked
description: "Read lines and tokens from stdin or a file in Zig using readUntilDelimiter, takeDelimiter and allocation limits across 0.14 and 0.15."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Io/Reader.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/fs/File.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Io.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading stdin and lines
**Goal:** read input without unbounded allocation.

Older API (pre-0.15; `std.io.getStdIn` is not in 0.15.1):
```zig
const stdin = std.io.getStdIn().reader();
var buf: [1024]u8 = undefined;
while (try stdin.readUntilDelimiterOrEof(&buf, '\n')) |line| {
    const t = std.mem.trimRight(u8, line, "\r");
    ...
}
const all = try stdin.readAllAlloc(alloc, 1 << 20);   // max size guard
```
0.15.1 API: `var r = std.fs.File.stdin().reader(&buf); const line = try r.interface.takeDelimiterExclusive('\n');`. The slice excludes the delimiter; `error.EndOfStream` is returned at end of input when nothing remains, and `error.StreamTooLong` when the delimiter is not found within the reader's buffer capacity.
- Always pass a maximum size to `readAllAlloc`/`readFileAlloc`.
- Windows lines end in `\r\n`: trim the `\r`.
- `error.StreamTooLong` means the line exceeded your buffer.
- Wrap files in a buffered reader for many small reads.

## Gotchas
- Reading a line into a stack buffer then storing the slice stores a dangling slice; `dupe` it.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `File.stdin()`, `File.reader(buffer)`, `Reader.takeDelimiterExclusive` (doc comment: excludes delimiter, `EndOfStream`, `StreamTooLong`), and the absence of `getStdIn` in Io.zig. Removed: the mixed-buffering claim.

Method: documentation only; no commands were run.

## Self-check
Feed a 3-line pipe and an input with a 5000-byte line; confirm the long line errors instead of overflowing.
