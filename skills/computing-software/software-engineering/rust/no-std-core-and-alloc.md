---
id: computing-software.software-engineering.rust.no-std-core-and-alloc
name: no-std-core-and-alloc
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-embedded-nostd, rust-no-std, no-std, core, alloc, panic-handler, global-allocator]
level: advanced
status: docs-checked
description: "Write Rust for #![no_std]: core vs alloc vs std, the panic handler, heap use through the alloc crate and an allocator, and keeping dependencies free of std."
sources:
  - https://docs.rust-embedded.org/book/intro/no-std.html
  - https://doc.rust-lang.org/core/
  - https://doc.rust-lang.org/alloc/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# no_std, core and alloc

**Goal:** libraries that run on microcontrollers, kernels and similar targets without an operating system.

- `core` is the platform-agnostic subset of the standard library. It is not aware of heap allocation and provides no concurrency or I/O, which need platform integration.
- A program using `core` must define the panic handler: a function taking `&panic::PanicInfo`, which must never return, marked `#[panic_handler]`.
- `std` also provides a runtime (stack overflow protection, command-line arguments, spawning the main thread before `main`); that runtime is not available in a `no_std` environment.
- Heap (dynamic memory) is available in `no_std` only if you use the `alloc` crate together with a suitable allocator. `alloc` provides `Box`, `Rc`/`Arc` and `Vec`, and is what `no_std` crates depend on instead of `std` (its contents are re-exported by `std`).

## Gotchas
- A dependency that pulls in `std` breaks the build for a target that has none; build for the real target early to find it.
- Feature flags that turn `std` on must be additive, so enabling them removes no functionality.

## Checked
2026-11-03. Confirmed against the Embedded Rust Book "no_std" page, the `core` crate page (heap, concurrency, I/O, `#[panic_handler]`, `PanicInfo`, never returns) and the `alloc` crate page (Box, Vec, `no_std` crates use it instead of `std`). Removed: all third-party crate names (embedded-alloc, linked_list_allocator, panic-halt, panic-probe, cortex-m-rt, heapless, postcard, libm, thiserror), the Cargo feature layout, target triple and build/test commands, and the FPU remark, none of which those pages state.
Method: documentation only; no commands were run.
