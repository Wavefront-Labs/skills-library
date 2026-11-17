---
id: computing-software.software-engineering.assembly.aapcs64-arg-registers
name: aapcs64-arg-registers
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, aapcs64-arg-registers, asm-abi-aapcs64]
level: practitioner
status: docs-checked
description: "AAPCS64 argument and return rules: X0-X7, V0-V7, X8 indirect result pointer, small aggregates, HFAs and stack arguments."
sources:
  - https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst
  - https://man7.org/linux/man-pages/man2/syscall.2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AAPCS64 argument registers
**Goal:** call and implement functions on 64-bit Arm Linux.

- Integer/pointer arguments go in `x0`-`x7`, floating-point and short-vector arguments in `v0`-`v7` (as `s`, `d`, `q` views). Remaining arguments go on the stack; the next stacked argument address (NSAA) has a minimum alignment of 8.
- A result is returned in the registers that would carry the same value as an argument (`x0`, `x1`, `v0`...). If it would not fit registers, the caller reserves memory and passes its address in `x8`; the callee need not preserve `x8`.
- A composite larger than 16 bytes is copied to caller-allocated memory and replaced by a pointer. Other composites are rounded up to a multiple of 8 bytes and travel in general registers or on the stack.
- Homogeneous Floating-point Aggregates (HFA: at most four members of the same floating-point type) are used unmodified and each element goes in its own `v` register; if they do not fit in registers they go on the stack, never in general registers.
```asm
// double dot2(double a, double b, double c, double d)   v0..v3 -> v0
dot2:
    fmul d0, d0, d1
    fmadd d0, d2, d3, d0      // d0 = d2*d3 + d0
    ret
```
- The base standard marshals the anonymous arguments of a variadic call with the same rules as named ones; platforms may deviate (see aapcs64-platform-variants).
- SP mod 16 must be 0 whenever memory is accessed through SP and at any public interface.

## Gotchas
- `x8` is the indirect-result register; Linux syscalls also take the syscall number in `w8`/`x8` (see linux-arm64-syscalls).
- Named integral arguments are narrowed by the callee, the standard does not require the caller to widen them, and padding bits have unspecified content at entry. Extend explicitly when you need the upper bits.

## Self-check
Compile `struct {double a, b;} f(void)` for aarch64 and check whether the result comes back in `v0`/`v1`.

## Checked
2026-11-02. Checked against the AAPCS64 document (abi-aa, aapcs64.rst): parameter passing stages, result return rules, HFA definition and notes, stack constraints, register table (r8 indirect result register), plus the man7 syscall(2) table for `x8`. Removed: the claim that Apple deviates on variadics (Apple documentation not read), the "128-bit in x1" wording, and the statement that extension rules are platform specific (the standard says callee narrows).

Method: documentation only; no commands were run.
