---
id: computing-software.software-engineering.zig.fmt-parse-custom
name: fmt-parse-custom
category: computing-software
field: software-engineering
product: zig
tags: [zig, fmt-parse-custom, zig-std-fmt, parseint, parsefloat, bufprint, custom-format-method]
level: practitioner
status: docs-checked
description: "Parse text into numbers with std.fmt.parseInt and parseFloat, format into buffers, and add a custom format method to a Zig type."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/fmt.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Io/Writer.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parsing numbers and custom format methods
**Goal:** round-trip text and numbers safely.

```zig
const n = try std.fmt.parseInt(u16, "8080", 10);        // errors: InvalidCharacter, Overflow
const h = try std.fmt.parseInt(u32, "ff", 16);
const auto = try std.fmt.parseInt(i64, "0x1F", 0);      // base 0 detects 0b / 0o / 0x prefixes
const f = try std.fmt.parseFloat(f64, "3.5e2");
const u = try std.fmt.parseUnsigned(u8, "200", 10);
var buf: [32]u8 = undefined;
const s = try std.fmt.bufPrint(&buf, "{d:0>4}", .{n});   // [fill][alignment][width]
const hex = std.fmt.bytesToHex(digest, .lower);          // [input.len * 2]u8 array
```
- `parseInt` with base 0 examines the prefix (`0b` base 2, `0o` base 8, `0x` base 16, otherwise base 10) and ignores `_` characters. `ParseIntError` is `Overflow` or `InvalidCharacter` (empty input counts as `InvalidCharacter`).
- Format placeholders have the form `{[argument][specifier]:[fill][alignment][width].[precision]}`; fill is a single byte.
- `std.fmt.hexToBytes(out, "dead")` decodes hex into `out`.
- `std.fmt.allocPrint(gpa, fmt, args)` allocates the result; `std.fmt.count(fmt, args)` returns its length.
- Custom formatting in 0.15.1: a type declares `pub fn format(self: @This(), writer: *std.Io.Writer) std.Io.Writer.Error!void` and is printed with the `{f}` specifier:
```zig
const P = struct {
    x: i32, y: i32,
    pub fn format(self: P, w: *std.Io.Writer) std.Io.Writer.Error!void {
        try w.print("({d}, {d})", .{ self.x, self.y });
    }
};
// try w.print("{f}", .{p});
```
- The compiler rejects an ambiguous format string: it asks you to specify `{f}` to call the format method or `{any}` to skip it. The old `(self, comptime fmt, options, writer: anytype)` signature is not the 0.15.1 form.

## Self-check
Parse "65536" into `u16` and expect `error.Overflow` using `std.testing.expectError`.

## Checked
2026-11-02. Confirmed in 0.15.1 `lib/std/fmt.zig` (`parseInt`, `ParseIntError`, `parseUnsigned`, `parseFloat`, `bytesToHex`, `hexToBytes`, `bufPrint`, `allocPrint`, `count`, `{f}` examples) and `lib/std/Io/Writer.zig` (placeholder grammar, `{f}`/`{any}` compile error).
Fixed: the pre-0.15 `format(self, fmt, opts, writer)` signature was shown as current and the `{f}` hedge is now confirmed. Removed: `allocPrintZ`, "rejects whitespace/multiple signs" claim, `{}`-prints-fields claim.
Method: documentation only; no commands were run.
