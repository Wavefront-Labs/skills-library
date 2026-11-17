---
id: computing-software.software-engineering.assembly.rust-asm-macro
name: rust-asm-macro
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, rust-asm-macro, asm-inline]
level: advanced
status: draft
description: "Rust inline assembly with core::arch::asm!, global_asm!, operand classes, options, clobber_abi and a Linux syscall example; note on naked functions."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Rust asm! and global_asm!
**Goal:** use stable inline assembly from Rust.

```rust
use std::arch::asm;

fn add(a: u64, b: u64) -> u64 {
    let mut x = a;
    unsafe { asm!("add {0}, {1}", inout(reg) x, in(reg) b, options(pure, nomem, nostack)); }
    x
}

#[cfg(all(target_arch = "x86_64", target_os = "linux"))]
fn write(fd: u64, buf: &[u8]) -> i64 {
    let ret: i64;
    unsafe {
        asm!("syscall",
             inlateout("rax") 1i64 => ret,
             in("rdi") fd, in("rsi") buf.as_ptr(), in("rdx") buf.len(),
             lateout("rcx") _, lateout("r11") _,
             options(nostack));
    }
    ret
}

std::arch::global_asm!(".globl my_func", "my_func:", "ret");
```
- Syntax is Intel on x86 by default (`options(att_syntax)` switches). Operands are `in(reg)`, `out(reg)`, `inout(reg)`, `lateout`, specific registers by name (`in("rdi")`), and `_` for discarded outputs.
- Options: `pure`, `nomem`, `readonly`, `nostack`, `preserves_flags`, `noreturn`. If you omit `nomem`/`readonly`, memory is assumed read and written; if you omit `preserves_flags`, flags are assumed clobbered.
- `clobber_abi("C")` marks every caller-saved register of the C ABI as clobbered, for asm that calls a function.
- `asm!` requires `unsafe`; the compiler trusts your declarations exactly as GCC does.
- Naked functions (`#[unsafe(naked)]` with `naked_asm!`) were stabilised in recent Rust releases; check your toolchain version (unconfirmed which).

## Gotchas
- `in(reg)` may allocate any register, including ones your template also names explicitly; use specific registers when it matters.
- A wrong `options(pure)` lets the compiler delete or deduplicate calls.

## Self-check
Compile in release mode, look at the output with `cargo asm` or `--emit asm`, and confirm `add` becomes one instruction.
