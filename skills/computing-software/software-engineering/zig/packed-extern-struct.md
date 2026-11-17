---
id: computing-software.software-engineering.zig.packed-extern-struct
name: packed-extern-struct
category: computing-software
field: software-engineering
product: zig
tags: [zig, packed-extern-struct, zig-structs, packed-struct, extern-struct, tuples, bitfields]
level: advanced
status: gated
description: "Choose between Zig default, extern and packed structs for layout control, and use anonymous structs and tuples."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# packed, extern structs and tuples
**Goal:** control memory layout when it matters.

- `struct`: layout unspecified.
- `extern struct`: C ABI layout, only extern-compatible fields.
- `packed struct(u32)`: fields laid out as bits from least significant, total bit size must equal the backing int:
```zig
const Flags = packed struct(u8) {
    read: bool, write: bool, exec: bool,
    _pad: u5 = 0,
};
const f: Flags = @bitCast(@as(u8, 0b101));
```
- Bit-pointers: taking `&f.read` produces a pointer that records a bit offset; it cannot be passed where an ABI-aligned pointer is expected.
- `@sizeOf`, `@bitSizeOf`, `@offsetOf(T, "field")`, `@alignOf` to verify layouts; `comptime assert(@sizeOf(Header) == 16)`.
- Tuples: anonymous struct with unnamed fields, `.{ 1, "a", true }`; access `t[0]` or `t.@"0"`; `.len` works; used for format args `std.debug.print("{} {}", .{a, b})`. `inline for` iterates a tuple.

## Gotchas
- Packed struct field restrictions vary by release; see the packed struct section of the language reference for your version.
- Endianness: packed layout follows target endianness; serialise with `std.mem.writeInt` for wire formats. (gated: unconfirmed, source is paywalled or blocked)

## Self-check
`comptime { std.debug.assert(@sizeOf(Flags) == 1); }` and cast a byte to `Flags` and back.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: packed struct backing integer, bit offsets, @offsetOf/@bitOffsetOf/@sizeOf (language reference).
- Removed or changed: the unsupported packed-struct restriction list.
- Gated: library (std) names not covered by the language reference stay marked in the text.
Method: documentation only; no commands were run.
