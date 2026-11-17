---
id: computing-software.software-engineering.zig.switch-exhaustive
name: switch-exhaustive
category: computing-software
field: software-engineering
product: zig
tags: [zig, switch-exhaustive, zig-control-flow, switch-range, inline-else, exhaustive-switch]
level: practitioner
status: gated
description: "Write exhaustive Zig switch expressions over ints, enums and tagged unions with ranges, multiple values, captures and inline else."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# switch: ranges, captures and exhaustiveness
**Goal:** use `switch` as the primary branching tool.

```zig
const r = switch (n) {
    0 => "zero",
    1, 2, 3 => "small",
    4...9 => "digit",          // inclusive range
    else => "big",
};
switch (tagged) {
    .num => |v| use(v),
    .text => |*s| s.* = "x",   // pointer capture mutates the union payload
    inline else => |v, tag| std.debug.print("{s}\n", .{@tagName(tag)}),
}
```
- Must be exhaustive: covering every enum member or adding `else`. Adding a new enum member breaks switches without `else`, which is the point.
- Integer switch needs `else` unless ranges cover the whole type.
- `inline else` generates one branch per remaining tag with a comptime-known payload type.
- `switch` can return noreturn in a branch: `else => unreachable`.
- Labeled switch with `continue :sw value` (state machines, dispatch loops) is documented in the 0.15.2 language reference: `sw: switch (x) { 0 => continue :sw 1, ... }`.

## Gotchas
- Use `else => unreachable` only when truly impossible; it is UB in ReleaseFast.
- String switching is not supported: use `std.meta.stringToEnum` or `std.mem.eql` chains. (gated: unconfirmed, source is paywalled or blocked)

## Self-check
Remove a case from an enum switch and confirm "switch must handle all possibilities".

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: ranges, inline else, labeled switch continue, else unreachable (language reference 0.15.2).
- Removed or changed: the version-gate hedge on labeled switch.
- Gated: library (std) names not covered by the language reference stay marked in the text.
Method: documentation only; no commands were run.
