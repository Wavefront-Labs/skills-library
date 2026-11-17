---
id: computing-software.software-engineering.zig.container-level-vars
name: container-level-vars
category: computing-software
field: software-engineering
product: zig
tags: [zig, container-level-vars, zig-variables, threadlocal, global-variables, static-local]
level: practitioner
status: docs-checked
description: "Declare file-scope globals, static locals via struct, and threadlocal variables in Zig, including initialisation order rules."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/atomic.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Thread.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container-level and threadlocal variables
**Goal:** use global state correctly in a language without implicit statics.

- Container level variables have static lifetime and are order-independent and lazily analyzed. Their initialization value is implicitly `comptime`; a `const` is comptime-known, a `var` is runtime-known.
- They can be declared inside a `struct`, `union`, `enum` or `opaque`.
- A function-local "static" is a `var` inside an anonymous struct:
```zig
fn nextId() u32 {
    const S = struct { var counter: u32 = 0; };
    S.counter += 1;
    return S.counter;
}
```
- Per-thread state: `threadlocal var depth: usize = 0;`.
- Globals are plain memory, not synchronised. For cross-thread use `std.atomic.Value(T)` or a `std.Thread.Mutex`.

## Gotchas
- A container level `var` initialiser is evaluated at comptime, so a runtime call there is a compile error; initialise in `main` or use `undefined` plus an init function.
- Thread local variables may not be `const`; in single-threaded builds they behave as regular container level variables.
- Globals make tests order-dependent; reset them in each `test` block.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: the Container Level Variables, Static Local Variables and Thread Local Variables sections of the language reference; `std.atomic.Value` and `std.Thread.Mutex` exist in the 0.15.1 source. Removed: the quoted error message and the comptime-access claim.

Method: documentation only; no commands were run.

## Self-check
Call `nextId()` three times, expect 1,2,3; mark counter `threadlocal`-style in a second function and verify per-thread values with two spawned threads.
