---
id: computing-software.software-engineering.assembly.gas-intel-syntax
name: gas-intel-syntax
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, gas-intel-syntax, asm-gas]
level: practitioner
status: docs-checked
description: "Use Intel syntax in the GNU assembler with .intel_syntax noprefix: byte/dword/qword ptr operand sizes, RIP-relative symbols, and differences from AT&T."
sources:
  - https://sourceware.org/binutils/docs/as/i386_002dVariations.html
  - https://sourceware.org/binutils/docs/as/i386_002dMemory.html
  - https://sourceware.org/binutils/docs/as/Symbol-Names.html
  - https://gcc.gnu.org/onlinedocs/gcc/x86-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GAS Intel syntax
**Goal:** write Intel-style code that GNU as accepts.

```gas
        .intel_syntax noprefix
        .globl  sum
        .text
sum:                                   # long sum(long *a, long n)
        xor     eax, eax
        test    rsi, rsi
        jz      2f
1:      add     rax, qword ptr [rdi]
        add     rdi, 8
        dec     rsi
        jnz     1b
2:      ret
        .att_syntax                    # restore default if mixing
```
- `.intel_syntax` selects Intel mode and `.att_syntax` switches back. Either takes an optional `prefix` or `noprefix` argument saying whether registers need a `%`; write `noprefix` explicitly so register names carry no `%`.
- Operands are in Intel order (destination first), immediates and registers undelimited, and absolute jump/call operands have no `*`.
- Sizes prefix the memory operand, not the mnemonic: `byte ptr`, `word ptr`, `dword ptr`, `qword ptr`, plus `xmmword ptr`, `ymmword ptr`, `zmmword ptr`. Intel `mov al, byte ptr foo` is AT&T `movb foo, %al`.
- RIP-relative symbols are written `[rip + symbol]`, e.g. `mov eax, dword ptr [rip + counter]` or `lea rsi, [rip + msg]` (AT&T `symbol(%rip)`).
- `1:`/`1b`/`2f` are numeric local labels: `Nb` refers to the most recent previous `N:` and `Nf` to the next one.
- GCC can emit this dialect: `gcc -S -masm=intel`; the option also sets the dialect GCC uses for inline asm.

## Gotchas
- Inline asm or basic asm written in AT&T syntax will not compile under `-masm=intel`, since the option sets the dialect for it; keep each file in one dialect or switch explicitly.
- Intel and AT&T differ in operand order; Intel `add eax, 4` is AT&T `addl $4, %eax`.

## Self-check
Assemble the sum function, call it from C and test with a four element array.

## Checked
2026-11-08. Confirmed against the GNU as manual pages AT&T Syntax versus Intel Syntax (`.intel_syntax`/`.att_syntax`, prefix/noprefix, `byte ptr` family, order), Memory References (`[rip + symbol]`), Symbol Names (numeric local labels `1:`, `1b`, `1f`) and GCC x86 Options (`-masm=intel`). Removed: the Clang flag claim, the "symbol named like a register" trap, the claims about NASM differences, `OFFSET` and `symbol[rip]` forms, and the "directives stay GNU style" remark (not on these pages).
Method: documentation only; no commands were run.
