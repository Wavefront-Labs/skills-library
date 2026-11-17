---
id: computing-software.software-engineering.zig.defer-ordering
name: defer-ordering
category: computing-software
field: software-engineering
product: zig
tags: [zig, defer-ordering, zig-defer, defer, lifo, resource-cleanup]
level: intro
status: docs-checked
description: "Use Zig defer for scope-exit cleanup, understand LIFO order, loops and early returns, and pair defer with resource acquisition."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# defer ordering and RAII-style cleanup
**Goal:** guarantee cleanup without destructors.

```zig
const f = try std.fs.cwd().openFile("a.txt", .{});
defer f.close();
const buf = try alloc.alloc(u8, 4096);
defer alloc.free(buf);
// runs: free(buf), then close(f), on every exit path
```
- `defer` runs at the end of the enclosing block, not function, so inside a loop body it runs every iteration.
- Multiple defers run in reverse order (last declared first).
- A deferred expression cannot `return` or `try` out of the function (`defer try x();` is an error); handle errors inside or discard (`defer _ = f() catch {};`).
- Variables captured by the deferred statement are evaluated at defer run time, not declaration time, so later mutation is seen.
- Early `return` or `break :label` triggers the defers of every block it leaves.

## Gotchas
- `defer` in a function that returns the resource to the caller frees it too early; use `errdefer` instead.
- Block-scoped defers in `if (cond) { defer x(); }` fire at the end of the `if` block.

## Self-check
Print in three nested defers and verify the reverse order; move a defer into a loop and count calls.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: defer/errdefer block scope, reverse order, return not allowed inside defer (language reference defer section).
- Removed or changed: nothing.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
