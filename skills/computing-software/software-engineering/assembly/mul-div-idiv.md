---
id: computing-software.software-engineering.assembly.mul-div-idiv
name: mul-div-idiv
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, mul-div-idiv, asm-x86-integer]
level: practitioner
status: draft
description: "x86-64 multiply and divide: one-operand MUL/IMUL widening, IMUL two/three-operand forms, DIV/IDIV register contract and divide-error faults."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# MUL, IMUL, DIV, IDIV
**Goal:** use the fixed-register multiply/divide forms without raising #DE.

```nasm
imul eax, ebx          ; eax = low 32 bits of eax*ebx (signed or unsigned same low bits)
imul rax, rdi, 12      ; rax = rdi * 12
mul  rcx               ; rdx:rax = rax * rcx (unsigned, 128-bit result)
imul rcx               ; rdx:rax = rax * rcx (signed)

xor  edx, edx          ; unsigned divide: zero the high half
div  rcx               ; rax = rdx:rax / rcx, rdx = remainder
cqo                    ; signed: sign-extend rax into rdx
idiv rcx
```
- 32-bit variants use edx:eax (`cdq` before `idiv`).
- A divisor of zero or a quotient that does not fit raises the divide-error exception (SIGFPE on Linux). INT_MIN / -1 overflows and faults too.
- The multi-operand `imul` forms leave rdx alone and set CF/OF if the full result does not fit.
- Division is slow (tens of cycles on many cores); divide by constants with multiply-shift (see division-by-constant) and by powers of two with shifts.

## Gotchas
- Forgetting `cqo`/`xor edx,edx` before dividing gives garbage or #DE.
- Remainder sign for `idiv` follows the dividend (truncating division like C).

## Self-check
Write `divmod(a,b)` returning quotient and remainder and test with a=-7, b=2 (expect -3 and -1).
