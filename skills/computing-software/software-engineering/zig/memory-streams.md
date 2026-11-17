---
id: computing-software.software-engineering.zig.memory-streams
name: memory-streams
category: computing-software
field: software-engineering
product: zig
tags: [zig, memory-streams, zig-std-io, fixedbufferstream, arraylist-writer, countingwriter, std-io-reader]
level: practitioner
status: docs-checked
description: "Read and write bytes in memory in Zig with fixedBufferStream, ArrayList writers, counting writers and Allocating writers."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Io.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Io/Writer.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Io/Reader.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Io/fixed_buffer_stream.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# In-memory streams and writers over buffers
**Goal:** unit-test and compose IO without files.

```zig
var buf: [128]u8 = undefined;
var w: std.Io.Writer = .fixed(&buf);               // 0.15.1
try w.print("x={d}", .{5});
const written = w.buffered();                      // "x=5"

var aw: std.Io.Writer.Allocating = .init(alloc);   // growable sink
defer aw.deinit();
try aw.writer.print("{s}", .{"abc"});
const bytes = aw.written();                        // or aw.toOwnedSlice()

var r: std.Io.Reader = .fixed("line1\nline2\n");
const l = try r.takeDelimiterExclusive('\n');      // "line1"
```
- In 0.15.1 `std.Io.Writer` and `std.Io.Reader` are concrete types; `Writer.fixed(buffer: []u8)` and `Reader.fixed(buffer: []const u8)` wrap a buffer, and `Writer.Allocating` owns a growing buffer.
- `std.io.fixedBufferStream` is still exported in 0.15.1 (its `reader()`/`writer()` give the older generic adapters, e.g. `readUntilDelimiter` in DeprecatedReader.zig).
- `std.io.null_writer` is deprecated in favor of `Writer.Discarding`.
- Endian-aware: `writer.writeInt(u32, v, .big)` exists on `std.Io.Writer`.

## Gotchas
- `fixedBufferStream` writers report `error.NoSpaceLeft` when full; the new `std.Io.Writer` reports `error.WriteFailed`.
- Reader and writer APIs changed in 0.15; code written for earlier releases (`.writer()`, `anytype` writers) needs porting.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: `Writer.fixed`, `Writer.buffered`, `Writer.print`, `Writer.writeInt`, `Writer.Allocating` (`init`, `deinit`, `written`, `toOwnedSlice`), `Reader.fixed`, `Reader.takeDelimiterExclusive`, `fixedBufferStream`, `null_writer` deprecation and `NoSpaceLeft`/`WriteFailed` in the 0.15.1 source. Fixed: the examples used `ArrayList(u8).init` and `countingWriter`, which are not in 0.15.1; the 'unconfirmed' 0.15 API is now confirmed.

Method: documentation only; no commands were run.

## Self-check
Format into a fixed buffer and assert `buffered()` equals the expected string.
