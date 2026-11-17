---
id: computing-software.software-engineering.assembly.gcc-extended-asm
name: gcc-extended-asm
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, gcc-extended-asm, asm-inline]
level: practitioner
status: docs-checked
description: "GCC extended inline asm: template syntax, outputs, inputs, named operands, AArch64 register-width modifiers and when basic asm falls short."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html
  - https://gcc.gnu.org/onlinedocs/gcc/Basic-Asm.html
  - https://gcc.gnu.org/onlinedocs/gcc/x86-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GCC extended asm
**Goal:** embed instructions in C safely.

```c
#include <stdint.h>
static inline uint64_t rdtsc(void) {
    uint32_t lo, hi;
    __asm__ volatile ("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}
static inline int add(int a, int b) {
    __asm__ ("addl %[b], %[a]" : [a] "+r"(a) : [b] "r"(b) : "cc");   /* AT&T: src, dst */
    return a;
}
/* AArch64: %w0 is the 32-bit view, %x0 the 64-bit view */
static inline int add_a64(int a, int b) {
    int r;
    __asm__ ("add %w0, %w1, %w2" : "=r"(r) : "r"(a), "r"(b));
    return r;
}
```
- Form: `asm [qualifiers] ( "template" : outputs : inputs : clobbers );` plus an optional fifth `: GotoLabels` section when the `goto` qualifier is used. Placeholders are `%0`, `%1`, ... (zero-based, outputs first) or `%[name]`.
- `=` marks write-only, `+` read-write. Multiple instructions in one string are separated with `\n\t`.
- The input + output + goto operand total is limited to 30; a `+` operand counts twice.
- x86 uses AT&T syntax by default; `-masm=intel` selects the Intel dialect, and that option also applies to basic asm.
- Use `__asm__` instead of `asm` when compiling with `-ansi` or a strict `-std` option.
- Basic `asm("...")` has no operands: at file scope it can emit directives or define whole functions, but inside a function GCC cannot learn what the string changes (it assumes general purpose registers are untouched), so use extended asm there.
- Write `%%eax` for a register name in an extended template, but `%eax` in basic asm.

## Gotchas
- Every register or memory your asm modifies must appear as an output, an in-out, or a clobber; otherwise optimisation breaks it.
- GCC does not parse the template, and symbols referenced only in it may be discarded unless they are also operands. Calling functions from a template needs detailed knowledge of the target assembler and ABI.
- Consecutive asm statements are not guaranteed to stay adjacent; put instructions that must stay together in one statement.

## Self-check
Rewrite `add` with positional operands, compile at -O2, and confirm it reduces to a single add instruction.

## Checked
2026-11-08. Confirmed against the GCC manual pages Extended Asm (syntax, qualifiers, operand format, 30-operand limit, `%%`, `\n\t`, volatile, rdtsc pattern, AArch64 `w`/`x` modifiers, template and symbol caveats), Basic Asm (no-operand behaviour, `%eax` versus `%%eax`, `-masm`) and x86 Options (`-masm` default `att`). Removed: the Clang claim and the intrinsics advice (not on these pages).
Method: documentation only; no commands were run.
