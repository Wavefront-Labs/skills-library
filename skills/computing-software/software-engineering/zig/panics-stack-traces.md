---
id: computing-software.software-engineering.zig.panics-stack-traces
name: panics-stack-traces
category: computing-software
field: software-engineering
product: zig
tags: [zig, panics-stack-traces, zig-debugging, panic-handler, stack-trace, segfault-handler, symbolication]
level: practitioner
status: docs-checked
description: "Read Zig panic messages and stack traces, install custom panic or segfault handlers, and get symbolised traces in release builds."
sources:
  - https://ziglang.org/documentation/0.15.1/#Illegal-Behavior
  - https://ziglang.org/documentation/0.15.1/#Panic-Handler
  - https://ziglang.org/documentation/0.15.1/#Error-Return-Traces
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/debug.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Panics, stack traces and crash handling
**Goal:** diagnose crashes quickly.

- When a safety check fails, the default panic handler crashes with a stack trace. Safety checks are on in Debug and ReleaseSafe and disabled by default in ReleaseFast and ReleaseSmall; `@setRuntimeSafety` overrides the mode per block.
- Error return traces show every point where an error was returned to its caller. They are enabled by default in Debug and disabled by default in ReleaseFast, ReleaseSafe and ReleaseSmall (`-ferror-tracing` enables them in ReleaseFast). They print when an error is returned from `main` or reaches `catch unreachable` with the default panic handler, and `@errorReturnTrace` plus `std.debug.dumpStackTrace` can print them yourself.
- Custom handler (0.15.1): the standard library looks for a `panic` declaration in the root source file that is a namespace of handlers. `std.debug.FullPanic` keeps the formatted safety panics:
```zig
pub const panic = std.debug.FullPanic(myPanic);
fn myPanic(msg: []const u8, first_trace_addr: ?usize) noreturn {
    std.debug.print("Panic! {s}\n", .{msg});
    std.process.exit(1);
}
```
- `std.debug.defaultPanic`, `std.debug.simple_panic`, `std.debug.captureStackTrace`, `std.debug.dumpStackTrace` and `std.debug.getSelfDebugInfo` exist in `std/debug.zig`.
- `std.Options.enable_segfault_handler` (default `std.debug.default_enable_segfault_handler`, true when runtime safety and platform support are present) controls the segfault handler.
- `-fno-formatted-panics` / `-fformatted-panics` select formatted or unformatted safety panics on the CLI; `-fstrip` omits debug symbols.

## Self-check
Cause an index out of bounds in Debug and read the trace to the exact source line.

## Checked
2026-11-02. Confirmed in the 0.15.1 language reference (Illegal Behavior, Panic Handler, Error Return Traces) and `lib/std/debug.zig`, `lib/std/std.zig`, `src/main.zig` help text.
Fixed: the old `pub fn panic(msg, trace, ret_addr)` signature is replaced by the `panic` namespace form shown in the reference; the segfault option name is now confirmed. Removed: exact trace line format, "traces absent with strip", addr2line/llvm-symbolizer advice, Windows PDB and thread-panic gotchas.
Method: documentation only; no commands were run.
