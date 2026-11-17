---
id: computing-software.software-engineering.zig.enum-types
name: enum-types
category: computing-software
field: software-engineering
product: zig
tags: [zig, enum-types, zig-enums-unions, enum-tag-type, tagname, stringtoenum, non-exhaustive-enum]
level: practitioner
status: gated
description: "Declare Zig enums with explicit tag integers, methods, @tagName, std.meta.stringToEnum and non-exhaustive enums."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enums, tag types and non-exhaustive enums
**Goal:** model closed sets with checked switches.

```zig
const Color = enum(u8) {
    red = 1, green, blue,            // green = 2, blue = 3
    pub fn isWarm(c: Color) bool { return c == .red; }
};
const c: Color = .green;
const n = @intFromEnum(c);          // 2
const back: Color = @enumFromInt(3);      // safety-checked
const name = @tagName(c);           // "green"
const parsed = std.meta.stringToEnum(Color, "blue") orelse return error.Bad;
const Open = enum(u8) { a, b, _ };  // non-exhaustive: any u8 allowed, switch needs `else` or a `_` prong
```
- `@enumFromInt` panics for values with no tag (exhaustive enums) in safe modes.
- Enum literals `.red` infer their type from context.
- `std.enums.EnumArray`, `EnumSet`, `EnumMap` give array-backed collections keyed by enum. (gated: unconfirmed, source is paywalled or blocked)
- `std.meta.fields(Color)` / `std.enums.values(Color)` iterate members.

## Gotchas
- Pre-0.11 names `@enumToInt`/`@intToEnum` appear in old tutorials; current names are `@intFromEnum`/`@enumFromInt`.
- `@tagName` on a non-exhaustive value without a tag is illegal behavior.

## Self-check
Round-trip every member through `@tagName` and `stringToEnum` in a loop over `std.enums.values`.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: enum(u8) tags, @intFromEnum/@enumFromInt safety, @tagName, non-exhaustive enums and the `_` prong (language reference enums section).
- Removed or changed: nothing; the non-exhaustive switch rule now names the `_` prong.
- Gated: library (std) names not covered by the language reference stay marked in the text.
Method: documentation only; no commands were run.
