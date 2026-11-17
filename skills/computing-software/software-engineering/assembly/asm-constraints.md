---
id: computing-software.software-engineering.assembly.asm-constraints
name: asm-constraints
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, asm-constraints, asm-inline]
level: advanced
status: docs-checked
description: "Inline asm operand constraints for x86-64 and AArch64: r, m, i, specific registers, matching digits, early clobber, and operand-size modifiers."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html
  - https://gcc.gnu.org/onlinedocs/gcc/Simple-Constraints.html
  - https://gcc.gnu.org/onlinedocs/gcc/Machine-Constraints.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Operand constraints
**Goal:** tell the compiler exactly what each operand may be.

- Generic: `r` any general register, `m` memory, `i` immediate integer, `g` any register, memory or immediate integer, `0`-`9` same location as that numbered output operand (matching constraint; only inputs may use it).
- x86 specific: `a` rax/eax, `b` rbx, `c` rcx, `d` rdx, `S` rsi, `D` rdi, `x` any SSE register, `I` constant 0..31 (32-bit shift counts), `N` unsigned 8-bit constant (for `in` and `out`). The Machine Constraints page has the full list.
- AArch64 specific: `w` an FP, Advanced SIMD or SVE register, `I` valid ADD immediate, `J` valid SUB immediate (once negated), `K`/`L` constants usable by 32-bit/64-bit logical instructions, `Q` a memory address using a single base register with no offset.
```c
/* output must not share a register with an input that is read after it is written */
__asm__ ("movl $1, %0; addl %1, %0" : "=&r"(out) : "r"(in));      /* & = early clobber */

/* matching digit: input starts equal to output */
__asm__ ("bswap %0" : "=r"(x) : "0"(x));

/* specific registers (x86): c, D and a pin count, p and the byte value; "0"(-1) ties to output 0 */
__asm__ ("repne scasb" : "=c"(count), "+D"(p) : "m"(*(const char (*)[]) p), "0"(-1), "a"(0));
```
- Operand modifiers pick a register width: x86 `%k0` (32-bit), `%q0` (64-bit), `%w0` (16-bit), `%b0` (8-bit); AArch64 `%w0`, `%x0` (general registers) and `%b0`, `%h0`, `%s0`, `%d0`, `%q0` (FP/SIMD views).
- Use `"m"` for operands the asm reads or writes in memory; the compiler then forms a valid address. An output can list alternatives such as `"=rm"` so the compiler picks the best location.

## Gotchas
- Without `&`, GCC may give an output the same register as an unrelated input, assuming inputs are consumed before outputs are written. Use `&` on every output that must not overlap an input.
- Never modify an input-only operand; tie it to an output with a matching digit instead.
- Memory the asm reads or writes beyond its listed operands needs the `"memory"` clobber.

## Self-check
Write a swap-endian helper using matching constraints and inspect the generated code.

## Checked
2026-11-08. Confirmed against the GCC manual pages Extended Asm (output and input operands, matching digits, `&`, clobbers, generic/AArch64/x86 operand modifiers), Simple Constraints (`m r i g 0-9`) and Constraints for Particular Machines (AArch64 and x86 letters). Removed: the Linux syscall example and syscall number, and the claim that `Q` is needed for exclusive loads and stores (not on these pages).
Method: documentation only; no commands were run.
