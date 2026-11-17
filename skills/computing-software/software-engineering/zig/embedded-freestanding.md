---
id: computing-software.software-engineering.zig.embedded-freestanding
name: embedded-freestanding
category: computing-software
field: software-engineering
product: zig
tags: [zig, embedded-freestanding, zig-embedded-wasm, freestanding, linker-script, mmio, volatile, microcontroller]
level: sme
status: docs-checked
description: "Target microcontrollers with Zig using freestanding triples, linker scripts, custom start code, MMIO via volatile pointers and ecosystem HALs."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build/Step/Compile.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bare-metal and embedded Zig
**Goal:** run Zig without an OS.

- Pick a freestanding target and CPU: the reference's translate-c example uses `-target thumb-freestanding-gnueabihf`; `-mcpu [cpu]` sets the CPU and feature set. `zig targets` lists what the compiler knows.
- Entry point: a declaration named `_start` in the root file (for example `pub const _start = {};`) disables the default `std.start` logic so your file can export a low-level entry point. In `build.zig`, `Compile.entry` can be `.disabled`, `.enabled` or `.{ .symbol_name = ... }`; the CLI has `-fno-entry` and `-fentry=[name]`.
- Linker script: `exe.setLinkerScript(b.path("link.ld"))`, or `-T[script]` / `--script [script]` on the CLI.
- Memory-mapped IO: the reference models registers as a `packed struct` behind a volatile pointer, `const gpio: *volatile GpioRegister = @ptrFromInt(0x0123);`, and warns that operating on such a struct field by field is the wrong approach (read, modify and write the whole register).
- Panic handler: declare `pub const panic = std.debug.FullPanic(myPanic);` in the root file, where `fn myPanic(msg: []const u8, first_trace_addr: ?usize) noreturn`. The `pub fn panic(...)` form of older releases is not what 0.15.1 documents.
- Size: `-O ReleaseSmall` optimizes for a small binary; `-fstrip` omits debug symbols; `-fsingle-threaded` tells the code it can assume one thread.
- Convert an ELF to another format with `zig objcopy` or `b.addObjCopy`.

## Self-check
Compile for your target, inspect sections with `objdump -h`, and check the vector table sits where your linker script puts it.

## Checked
2026-11-02. Confirmed in the 0.15.1 language reference (Panic Handler, Entry Point, `packed_struct_mmio.zig`, translate-c target example), `lib/std/Build/Step/Compile.zig` (`Entry`, `setLinkerScript`, `addObjCopy`) and `src/main.zig` help text.
Fixed: the old `pub fn panic(...) noreturn { while (true) {} }` form (0.15.1 expects a `panic` namespace such as `std.debug.FullPanic(...)`). Removed: `thumb-freestanding-eabihf`/cortex_m4, RISC-V and AVR claims, `@setRuntimeSafety`, `.vectors` linksection example, FixedBufferAllocator advice, MicroZig, flashing tools, `.bss`/`.data` init and compiler_rt gotchas.
Method: documentation only; no commands were run.
