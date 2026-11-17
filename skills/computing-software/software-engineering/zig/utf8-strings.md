---
id: computing-software.software-engineering.zig.utf8-strings
name: utf8-strings
category: computing-software
field: software-engineering
product: zig
tags: [zig, utf8-strings, zig-strings, utf8view, unicode-codepoints, string-as-bytes]
level: practitioner
status: docs-checked
description: "Handle Zig strings as []const u8, iterate code points with std.unicode, validate UTF-8 and compare or search with std.mem."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/unicode.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/ascii.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/meta.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strings as byte slices and UTF-8 iteration
**Goal:** treat text correctly without a string type.

- A string is `[]const u8` (no encoding enforced). Literals are UTF-8.
- `s.len` is bytes; `s[i]` is a byte.
```zig
const s = "héllo";
std.debug.assert(std.unicode.utf8ValidateSlice(s));
var it = (try std.unicode.Utf8View.init(s)).iterator();
while (it.nextCodepoint()) |cp| std.debug.print("U+{X}\n", .{cp});
const n = try std.unicode.utf8CountCodepoints(s);
```
- Compare: `std.mem.eql(u8, a, b)`; ordering `std.mem.order(u8, a, b)`; ASCII case-insensitive `std.ascii.eqlIgnoreCase`, `std.ascii.lowerString`, `upperString`.
- Search: `std.mem.indexOf(u8, hay, needle)`, `startsWith`, `endsWith`, `containsAtLeast`.
- Switching on strings: `std.meta.stringToEnum` or if/else with `eql`.

## Gotchas
- Compare slices with `std.mem.eql`, not `==`.
- Slicing by byte index may split a code point; validate or iterate code points.
- Printing with `{s}` expects bytes; use `{u}` for a single code point.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `utf8ValidateSlice`, `utf8CountCodepoints`, `Utf8View.init`, `nextCodepoint` in unicode.zig; `eqlIgnoreCase`, `lowerString`, `upperString` in ascii.zig; `containsAtLeast`, `order`; `meta.stringToEnum`; the `{u}` specifier in the `Writer.print` doc. Removed: the unverifiable third-party Unicode package claim.

Method: documentation only; no commands were run.

## Self-check
Count code points of "héllo" (5) versus bytes (6).
