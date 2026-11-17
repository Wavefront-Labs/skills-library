---
id: computing-software.software-engineering.zig.number-literals
name: number-literals
category: computing-software
field: software-engineering
product: zig
tags: [zig, number-literals, zig-lexical, comptime-int, hex-literal, multiline-string]
level: intro
status: docs-checked
description: "Write Zig integer, float, character and multiline string literals, including underscores, radix prefixes and escapes, and know their comptime types."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integer, float and string literals
**Goal:** write literals with the right type and syntax.

```zig
const a = 1_000_000;        // comptime_int, underscores allowed
const b = 0xff;             // hex; also 0o17 octal, 0b1010 binary
const c = 1.5e3;            // comptime_float
const d = 0x1.8p1;          // hex float
const e: u8 = 'A';          // char literal is a comptime_int code point
const s = "hi\n";           // *const [3:0]u8, null terminated
const m =
    \\line one
    \\line two
;                           // multiline string; no escapes processed
```
## Key facts
- Untyped number literals are `comptime_int` / `comptime_float` with arbitrary precision; they coerce to any type that can represent the value, else compile error ("type 'u8' cannot represent integer value 300").
- No implicit int<->float conversion at runtime: use `@floatFromInt`, `@intFromFloat`.
- `'\u{1F600}'` is a code point literal; strings are UTF-8 bytes. `"\x41"` byte escape.
- Multiline string lines start with `\\`; the trailing newline of the last line is not included, and `\\` lines contain no escapes.
- String literal type is a pointer to a null-terminated array, so `s.len` is the byte length without the sentinel and `s.ptr` is C-compatible.

## Gotchas
- `var x = 5;` is a compile error because comptime_int cannot be a runtime var: write `var x: i32 = 5;` or `var x = @as(i32, 5);`.
- Division of two comptime_ints with a remainder needs `@divTrunc`/`@divFloor`.

## Self-check
Compile `const x: u8 = 256;` and read the error; then `var y = 3;` and read the error; fix both with explicit types.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: literal forms, comptime_int, multiline strings, string literal type (language reference).
- Removed or changed: nothing.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
