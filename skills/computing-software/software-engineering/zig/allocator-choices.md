---
id: computing-software.software-engineering.zig.allocator-choices
name: allocator-choices
category: computing-software
field: software-engineering
product: zig
tags: [zig, allocator-choices, zig-memory, arenaallocator, generalpurposeallocator, debugallocator, fixedbufferallocator, page-allocator, c-allocator]
level: practitioner
status: docs-checked
description: "Select the right Zig allocator: page_allocator, ArenaAllocator, GeneralPurposeAllocator or DebugAllocator, FixedBufferAllocator, c_allocator, smp_allocator."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/heap.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/heap/debug_allocator.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/heap/arena_allocator.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing an allocator: arena, GPA, fixed buffer, page, C
**Goal:** pick the allocator that fits lifetime and environment.

| Use | Allocator |
|---|---|
| Whole-request or whole-program scoped, free all at once | `std.heap.ArenaAllocator` |
| Dev/test of general code, leak and double-free detection | `std.heap.DebugAllocator(.{})` (`GeneralPurposeAllocator` is an alias in 0.15.1) |
| Fast general-purpose in release | `std.heap.c_allocator` (needs libc) or `std.heap.smp_allocator` |
| No heap / bounded memory | `std.heap.FixedBufferAllocator` over a stack buffer |
| Whole pages straight from the OS | `std.heap.page_allocator` |
| wasm32 | `std.heap.wasm_allocator` |
| Tests | `std.testing.allocator` (fails test on leak) |

```zig
var gpa = std.heap.GeneralPurposeAllocator(.{}){};
defer _ = gpa.deinit();               // returns .leak if anything leaked
const alloc = gpa.allocator();

var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
defer arena.deinit();                 // frees everything at once
const a = arena.allocator();

var buf: [4096]u8 = undefined;
var fba = std.heap.FixedBufferAllocator.init(&buf);
```
## Gotchas
- Arena memory is released by `deinit` or `reset`; a long-lived arena keeps growing until then.
- Check `gpa.deinit()` result in Debug; ignoring it loses leak detection.
- `c_allocator` without linking libc fails to compile or link.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `ArenaAllocator` (`deinit`, `reset(.retain_capacity)`), `DebugAllocator`/`GeneralPurposeAllocator` alias, `.init`, `deinit()` returning `std.heap.Check` (`.leak`/`.ok`), `FixedBufferAllocator`, `c_allocator`, `smp_allocator`, `page_allocator`, `wasm_allocator`. Removed: the arena free-no-op remark and the page_allocator cost remark.

Method: documentation only; no commands were run.

## Self-check
Write the same function with arena and with GPA, confirm no leak report, and show `FixedBufferAllocator` returning `OutOfMemory` when the buffer is too small.
