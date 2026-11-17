---
id: computing-software.software-engineering.zig.comptime-execution
name: comptime-execution
category: computing-software
field: software-engineering
product: zig
tags: [zig, comptime-execution, zig-comptime, comptime, comptime-var, compileerror, inline-for]
level: practitioner
status: docs-checked
description: "Run Zig code at compile time with comptime parameters, comptime blocks, inline loops and compile errors for validation."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# comptime parameters, variables and blocks
**Goal:** move work from runtime to compile time safely.

```zig
fn fib(comptime n: u32) u32 {
    return if (n < 2) n else fib(n - 1) + fib(n - 2);
}
const table = blk: {                       // comptime-evaluated initializer
    var t: [10]u32 = undefined;
    for (&t, 0..) |*e, i| e.* = @intCast(i * i);
    break :blk t;
};
comptime {
    if (@sizeOf(usize) != 8) @compileError("64-bit only");
}
```
- Top-level declarations, array lengths, type values and `comptime` parameters are comptime-known.
- `comptime var` lives only at comptime and can change in comptime blocks.
- `@compileError("...")`, `@compileLog(x)` (debug only) for diagnostics; `@setEvalBranchQuota(n)` raises the loop limit (default 1000 backward branches).
- Comptime code cannot do I/O, allocate with runtime allocators or touch extern state.
- `inline for`/`inline while` unroll; a regular `for` over comptime-known data can still run at runtime.
- Call at comptime explicitly: `const x = comptime fib(20);`.

## Gotchas
- "evaluation exceeded 1000 backwards branches" means call `@setEvalBranchQuota`.
- Runtime values cannot be used where comptime is required ("unable to resolve comptime value").

## Self-check
Compute a CRC table at comptime and `expectEqual` the first entries; trigger the branch-quota error with a big loop then fix it.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: comptime blocks, @compileError, @compileLog, @setEvalBranchQuota, 1000 backwards branches error text (language reference).
- Removed or changed: nothing.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
