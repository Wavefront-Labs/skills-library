---
id: computing-software.software-engineering.zig.bitcast-ptrcast
name: bitcast-ptrcast
category: computing-software
field: software-engineering
product: zig
tags: [zig, bitcast-ptrcast, zig-casting, bitcast, ptrcast, std-mem-asbytes, bytesasslice]
level: advanced
status: gated
description: "Reinterpret Zig data with @bitCast, @ptrCast, @alignCast and std.mem.bytesAsSlice, with endianness and aliasing caveats."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://ziglang.org/documentation/0.15.2/std/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @bitCast, @ptrCast and @alignCast
**Goal:** reinterpret memory without undefined behaviour.

```zig
const f: f32 = 1.0;
const bits: u32 = @bitCast(f);                 // 0x3f800000, same size required
const bytes = std.mem.asBytes(&f);              // *const [4]u8
const words = std.mem.bytesAsSlice(u16, buf);   // buf len multiple of 2, aligned
const p: *u32 = @ptrCast(@alignCast(raw_ptr));  // from *anyopaque / [*]u8
const v = std.mem.readInt(u32, buf[0..4], .little);   // safe, any alignment
std.mem.writeInt(u32, buf[0..4], v, .big);
```
- `@bitCast` requires identical bit size; works between ints, floats, packed structs and vectors.
- `@ptrCast` changes pointee type with no check; `@alignCast` asserts alignment (checked in safe modes).
- For parsing wire formats prefer `readInt`/`writeInt` and `std.mem.bytesToValue` (newer) over pointer casts: they handle alignment and endianness.
- `@byteSwap`, `std.mem.nativeToBig`, `bigToNative` for endianness. (gated: unconfirmed, source is paywalled or blocked)

## Gotchas
- Type punning via `@ptrCast` of a stack variable of a different size reads out of bounds.
- Zig does not guarantee C strict-aliasing assumptions either way; `[]u8` reinterpretation is the sanctioned route.
- Layout of default structs is unspecified; only `extern`/`packed` are safe to cast.

## Self-check
`@bitCast` `1.0` to u32 and assert 0x3f800000; `readInt` a big-endian u16 and compare.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: @bitCast, @ptrCast, @alignCast, @byteSwap semantics (language reference).
- Removed or changed: nothing.
- Gated: library (std) names not covered by the language reference stay marked in the text.
Method: documentation only; no commands were run.
