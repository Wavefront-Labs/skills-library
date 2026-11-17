---
id: computing-software.software-engineering.zig.wrapping-saturating-ops
name: wrapping-saturating-ops
category: computing-software
field: software-engineering
product: zig
tags: [zig, wrapping-saturating-ops, zig-int-semantics, wrapping-arithmetic, saturating-arithmetic, overflow-detection, addwithoverflow]
level: practitioner
status: gated
description: "Choose among Zig checked, wrapping (+%), saturating and overflow-reporting arithmetic for hashes, counters and parsing."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wrapping and saturating operators
**Goal:** pick the right overflow behaviour deliberately.

| Operators | Behaviour |
|---|---|
| `+ - * <<` | overflow is illegal behavior: panic in Debug/ReleaseSafe, undefined in ReleaseFast/Small |
| `+% -% *%` | wrap around (two's complement) |
| `+\| -\| *\| <<\|` | saturate at min/max |
| `@addWithOverflow(a,b)` | returns tuple `{result, overflow_bit}` |

```zig
var h: u32 = 2166136261;
for (data) |b| { h ^= b; h *%= 16777619; }          // FNV-1a needs wrapping
const sat: u8 = 250 +| 10;                          // 255
const r = @addWithOverflow(@as(u8, 250), 10);       // r[0]==4, r[1]==1
const ok = std.math.add(u8, 250, 10) catch return error.Overflow;
```
- `std.math.add/sub/mul/cast(T, x)` return errors or `null` (`std.math.cast` returns `?T`): the right tool for parsing untrusted numbers. (gated: unconfirmed, source is paywalled or blocked)
- Division by zero is illegal behavior; `@divTrunc`, `@divFloor`, `@rem`, `@mod` are required for signed ints (signed operands of plain `/` must be comptime-known and positive per the operator table).
- Compile-time overflow is always a compile error.

## Gotchas
- Release-fast overflow silently produces UB, so tests in Debug are essential.
- `-x` on `i32` min overflows; use `0 -% x` or check.

## Self-check
Compute FNV-1a of "hello" with wrapping and compare to the known 32-bit value 0x4f9f2cab.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: +%, +|, @addWithOverflow, division rules, compile-time overflow (language reference operator table).
- Removed or changed: the imprecise claim that plain / on negative ints is a compile error.
- Gated: library (std) names not covered by the language reference stay marked in the text.
Method: documentation only; no commands were run.
