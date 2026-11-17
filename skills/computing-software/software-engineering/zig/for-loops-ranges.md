---
id: computing-software.software-engineering.zig.for-loops-ranges
name: for-loops-ranges
category: computing-software
field: software-engineering
product: zig
tags: [zig, for-loops-ranges, zig-control-flow, for-range, multi-object-for, inline-for]
level: intro
status: docs-checked
description: "Iterate slices and ranges with Zig for, including index captures, multiple parallel sequences, inline for and labeled breaks."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# for loops, ranges and multi-object iteration
**Goal:** loop without C-style counters.

```zig
for (items) |x| { ... }                 // by value
for (items) |*x| { x.* *= 2; }          // by pointer, mutates
for (items, 0..) |x, i| { ... }         // index via open range
for (a, b) |x, y| { ... }               // parallel; lengths must match (checked)
for (0..10) |i| { ... }                 // i: usize
for (items) |x| { if (x == 0) break; } else { /* no break */ }
```
- Ranges are `start..end` (end exclusive); `0..` is open-ended and only valid next to a bounded object.
- Mismatched lengths in a multi-object `for` panic in safe modes (illegal behavior otherwise).
- `inline for` unrolls at comptime and works over tuples and comptime-known arrays; required to iterate struct fields from `std.meta.fields`.
- Labels: `outer: for (...) |x| { for (...) |y| { continue :outer; } }`.
- `for` is also an expression with `else`: the else branch value is used when no `break` happened.

## Gotchas
- Old syntax `for (items) |x, i|` (index as second capture) was removed in 0.13-era releases; use the range form.
- Loop variable `i` from `0..n` is `usize`; cast for signed math.

## Self-check
Zip two arrays with `for (a, b)`; then make lengths differ and confirm the safety panic.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: for over multiple objects, ranges, inline for, labeled continue (language reference for section).
- Removed or changed: nothing.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
