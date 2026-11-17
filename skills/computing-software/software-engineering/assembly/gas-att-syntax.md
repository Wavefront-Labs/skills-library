---
id: computing-software.software-engineering.assembly.gas-att-syntax
name: gas-att-syntax
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, gas-att-syntax, asm-gas]
level: practitioner
status: docs-checked
description: "GNU assembler AT&T syntax for x86-64: source-before-destination, register and immediate prefixes, size suffixes, memory operand form and indirect branches."
sources:
  - https://sourceware.org/binutils/docs/as/i386_002dVariations.html
  - https://sourceware.org/binutils/docs/as/i386_002dMnemonics.html
  - https://sourceware.org/binutils/docs/as/i386_002dMemory.html
  - https://sourceware.org/binutils/docs/as/Dot.html
  - https://sourceware.org/binutils/docs/as/Set.html
  - https://sourceware.org/binutils/docs/binutils/objdump.html
  - https://gcc.gnu.org/onlinedocs/gcc/Link-Options.html
  - https://raw.githubusercontent.com/torvalds/linux/master/arch/x86/entry/syscalls/syscall_64.tbl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GAS AT&T syntax
**Goal:** read and write the default GNU as dialect for x86.

```gas
        .globl  _start
        .text
_start:
        movq    $1, %rax              # 1 = write
        movq    $1, %rdi
        leaq    msg(%rip), %rsi       # symbol(%rip) is RIP-relative
        movq    $len, %rdx
        syscall
        movl    $60, %eax             # 60 = exit
        xorl    %edi, %edi
        syscall
        .section .rodata
msg:    .ascii  "hi\n"
        .set    len, . - msg
```
- Order is `op source, destination` (`add eax, 4` in Intel is `addl $4, %eax`). Registers carry `%`, immediates carry `$`, comments use `#`. `bound`, `invlpga` and instructions with two immediates such as `enter` keep their order.
- Size suffix: `b` 8, `w` 16, `l` 32, `q` 64 bits (`movl`, `addq`). An instruction with a memory operand and no register operand must carry a suffix, e.g. `movl $0, (%rdi)`. With no suffix, as takes the size from the destination register.
- Memory: `disp(base, index, scale)` with scale 1, 2, 4 or 8, e.g. `8(%rdi,%rsi,4)`; Intel `[rip + symbol]` is `symbol(%rip)`. Absolute indirect branches use `*`: `call *%rax`, `jmp *8(%rdi)`; without `*`, as uses PC-relative addressing for labels.
- Extension mnemonics: `movzbl`, `movsbq`, `movslq` are the AT&T names for Intel `movzx`/`movsx`/`movsxd`. `cltq` is AT&T for `cdqe`, `cqto` for `cqo`, `cltd` for `cdq`.
- `.` is the current address and `.set sym, expr` (same as `.equ`) defines a symbol, so `.set len, . - msg` gives the string length.
- Linux x86-64 syscall numbers: write is 1 and exit is 60 (kernel `syscall_64.tbl`).
- Build: `as hello.s -o hello.o && ld hello.o -o hello` (`-o` names the output in both tools), or `gcc -nostdlib -static hello.s -o hello` (`-nostdlib` drops the startup files and standard libraries).

## Gotchas
- Operand order is reversed from Intel and NASM; the single most frequent bug when porting snippets.
- `objdump -d -M intel` shows x86 disassembly in Intel syntax; `-M att` selects AT&T.

## Self-check
Translate `mov dword [rdi+rsi*4], 5` into AT&T and assemble it.

## Checked
2026-11-08. Confirmed against the GNU as manual pages AT&T Syntax versus Intel Syntax, i386-Mnemonics (suffixes, cltq/cqto names, movzx/movsx names), Memory References (`*`, RIP-relative, memory size suffix rule), The Special Dot Symbol and .set; the objdump manual (`-M intel`/`att`); GCC Link Options (`-nostdlib`, `-static`); the Linux `syscall_64.tbl` (write 1, exit 60). Removed: the claim that objdump prints AT&T by default (the manual does not state the default).
Method: documentation only; no commands were run.
