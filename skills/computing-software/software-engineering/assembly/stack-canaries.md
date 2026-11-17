---
id: computing-software.software-engineering.assembly.stack-canaries
name: stack-canaries
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, stack-canaries, asm-stack-frames]
level: advanced
status: draft
description: "How stack protector canaries work in compiled x86-64 code (FS:0x28 on glibc), reading the check sequence, and adding one to hand-written assembly."
sources:
  - https://gitlab.com/x86-psABIs/x86-64-ABI
  - https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Stack canaries
**Goal:** recognise and reproduce the stack-smashing check.

- GCC/Clang `-fstack-protector-strong` places a random value between locals and the saved return address, and checks it before returning.
- Typical x86-64 glibc output (canary stored at `fs:0x28` in the thread control block):
```nasm
    mov  rax, [fs:0x28]
    mov  [rbp-8], rax
    xor  eax, eax
    ...
    mov  rdx, [rbp-8]
    sub  rdx, [fs:0x28]
    jne  .fail
    leave
    ret
.fail:
    call __stack_chk_fail
```
- `__stack_chk_fail` aborts; it never returns. Compile with `-fno-stack-protector` only for freestanding code that has no TLS.
- Windows MSVC `/GS` compares against a cookie variable (`__security_cookie`) XORed with the frame address.
- AArch64 Linux compilers load the guard through a symbol or a thread register depending on platform and flags (exact sequence: unconfirmed; compile a sample to see it).

## Gotchas
- The canary's low byte is zero on glibc, which stops string-copy overflows from reproducing it.
- Hand-written assembly functions usually skip canaries; buffers on their stack are unprotected.

## Self-check
Compile `char buf[64]; gets(buf);` with `-fstack-protector-all -S` and find the check.
