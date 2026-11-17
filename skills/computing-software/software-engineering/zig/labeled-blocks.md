---
id: computing-software.software-engineering.zig.labeled-blocks
name: labeled-blocks
category: computing-software
field: software-engineering
product: zig
tags: [zig, labeled-blocks, zig-control-flow, break-with-value, labeled-break, block-expression]
level: practitioner
status: docs-checked
description: "Use Zig labeled blocks to compute values, early-exit nested loops, and defer cleanup ordering at block scope."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Labeled blocks and break with value
**Goal:** replace temp variables and gotos with block expressions.

```zig
const v = blk: {
    if (cond) break :blk 1;
    var t: u32 = 0;
    for (xs) |x| t += x;
    break :blk t;
};
outer: for (rows) |row| {
    for (row) |c| {
        if (c == target) break :outer;
    }
}
```
- Any block can be labeled: `label: { ... break :label value; }`; the block is an expression of the peer type of all breaks.
- `defer` inside a labeled block runs when the block exits by any path.
- Comptime computation helpers are typically written as `comptime blk: { ... }`.
- There is no `goto`; labeled `continue :label` and labeled-switch continue replace it.

## Gotchas
- A labeled block that never executes `break :label` and has no trailing value is `void`.
- Unused labels are a compile error.

## Self-check
Compute the first even number in an array with a labeled block that yields `?u32`.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: labeled blocks, break :label value, labeled loops, labeled switch (language reference).
- Removed or changed: nothing.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
