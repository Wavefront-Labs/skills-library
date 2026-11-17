---
id: computing-software.software-engineering.zig.illegal-behavior-safety
name: illegal-behavior-safety
category: computing-software
field: software-engineering
product: zig
tags: [zig, illegal-behavior-safety, zig-int-semantics, illegal-behavior, setruntimesafety, unreachable, safety-checks]
level: advanced
status: gated
description: "Know the Zig illegal behaviors that panic in safe modes, where @setRuntimeSafety changes them, and how to find them with sanitizers."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Illegal behavior and safety checks
**Goal:** understand what the compiler guarantees per build mode.

Illegal behavior (checked in Debug and ReleaseSafe, UB in ReleaseFast/ReleaseSmall): integer overflow, out-of-bounds index, `unreachable` reached, wrong union field access, invalid `@enumFromInt`, bad `@intCast`/`@alignCast`, null `.?`, division by zero, slice length mismatch in `@memcpy`, shift amount too large, reading `undefined`.
- Panic message names the check and prints a stack trace.
- Switch off locally for hot loops, per scope, only after profiling:
```zig
fn hot() void {
    @setRuntimeSafety(false);
    ...
}
```
- Keep ReleaseSafe for services where crashes beat corruption; use ReleaseFast for performance-critical code that is well tested.
- Set a custom panic handler: `pub const panic = std.debug.FullPanic(myPanic);` (newer) or `pub fn panic(msg: []const u8, trace: ?*std.builtin.StackTrace, ret_addr: ?usize) noreturn` in the root file (older); check the version (gated: unconfirmed, source is paywalled or blocked).
- Sanitizers and valgrind: see `zig build-exe --help` and the Zig build docs for the flags your compiler supports (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- `unreachable` is an optimization hint in release-fast: wrongly asserting it is a miscompile.
- Debug and ReleaseSafe builds fill `undefined` with `0xaa`; a bug that hides behind zero memory can appear only there.

## Self-check
Write a test that triggers each of overflow and out-of-bounds in Debug, confirm panic text, then compare behaviour under `-Doptimize=ReleaseFast`.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: illegal behavior list, safety modes, @setRuntimeSafety, unreachable optimisation, 0xaa fill (language reference).
- Removed or changed: the unverifiable sanitizer flag names.
- Gated: library (std) names not covered by the language reference stay marked in the text.
Method: documentation only; no commands were run.
