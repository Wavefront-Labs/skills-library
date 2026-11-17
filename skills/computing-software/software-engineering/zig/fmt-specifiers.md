---
id: computing-software.software-engineering.zig.fmt-specifiers
name: fmt-specifiers
category: computing-software
field: software-engineering
product: zig
tags: [zig, fmt-specifiers, zig-std-fmt, std-fmt, format-specifiers, debug-print, width-precision]
level: practitioner
status: docs-checked
description: "Format values in Zig with {d}, {s}, {x}, {any}, {} width, precision and alignment, and understand std.debug.print vs stdout."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Io/Writer.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/fmt.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Format strings and specifiers
**Goal:** print what you mean.

```zig
std.debug.print("{d} {s} {x} {c} {e}\n", .{ 42, "text", 255, 'A', 1.5 });
std.debug.print("[{d:>5}] [{d:<5}] [{d:0>5}] [{x:0>2}]\n", .{ 7, 7, 7, 10 });
std.debug.print("{d:.2} {any} {?} {*}\n", .{ 3.14159, .{ 1, 2 }, @as(?u8, null), &x });
std.debug.print("{{literal braces}} {s}\n", .{@tagName(color)});
```
- `{d}` decimal ints/floats, `{s}` strings/byte slices, `{x}/{X}` hex, `{b}` binary, `{o}` octal, `{c}` byte as char, `{u}` code point, `{e}` scientific, `{any}` debug format of anything, `{t}` tag name of an enum or error, `{}` default per type.
- Fill/align/width: `{[fill][align][width]}` e.g. `{d:*^9}` (fill `*`, center, width 9); precision `.3` for floats.
- Positional/named: `{0s} {0s}` reuses argument 0; `{[name]s}` with struct arg.
- Arguments are always a tuple: `.{}` for none, `.{x}` for one.
- `std.debug.print` writes to stderr, takes the stderr lock and silently ignores write failures; use a stdout writer for program output.
- Custom formatting in 0.15.1: define `pub fn format(self: @This(), writer: *std.Io.Writer) std.Io.Writer.Error!void` on the type and print it with `{f}`. The older `format(self, comptime fmt, options, writer)` signature is not used by `{f}`.

## Gotchas
- Count of `{}` must equal the tuple length.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: the `Writer.print` doc comment: placeholder grammar `{[argument][specifier]:[fill][alignment][width].[precision]}`, numeric and `[name]` arguments, specifiers `x X s t b64 e d b o c u D B Bi ? ! * any f`, and `{{` escapes; `fmt.zig` tests for `{?}`, `{*}`, `{any}`, `{e}`, `{b}`, `{o}`, `{u}`; `debug.print` source. Fixed: the 0.15.1 `format(self, writer)` / `{f}` signature is confirmed. Removed: the `{}`-on-bytes error claim and the quoted compile error text.

Method: documentation only; no commands were run.

## Self-check
Print an enum with `{s}` and `@tagName`, a float with `{d:.3}`, and a padded hex byte.
