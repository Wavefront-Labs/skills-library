---
id: computing-software.software-engineering.assembly.call-ret-stack
name: call-ret-stack
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, call-ret-stack, asm-x86-control]
level: practitioner
status: draft
description: "CALL and RET on x86-64: return address push/pop, stack growth, 16-byte alignment at call sites, and indirect calls."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://gitlab.com/x86-psABIs/x86-64-ABI
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# CALL, RET and the stack
**Goal:** keep the stack balanced and aligned across calls.

- `call target` pushes the 8-byte return address (address of the next instruction) and jumps; `ret` pops it into RIP.
- The stack grows downward: `push` decrements rsp by 8 then stores; `pop` loads then increments.
- Both SysV and Win64 require rsp to be 16-byte aligned immediately before the `call`, so at function entry rsp is 8 modulo 16.
```nasm
caller:
    sub  rsp, 8            ; re-align: entry rsp = 8 mod 16, now 0 mod 16
    call callee
    add  rsp, 8
    ret
    ; or: push rbx ... pop rbx  (one push also fixes alignment)
```
- Indirect forms: `call rax`, `call [rel fp]`, `call [rdi+8]` (vtable-style); with CET indirect-branch tracking the target begins with `endbr64`.
- `ret imm16` pops extra bytes (callee-cleanup, 32-bit stdcall style; not used by x64 ABIs).

## Gotchas
- Unbalanced push/pop corrupts the return address and `ret` jumps to garbage.
- Never `jmp` over a `ret` mismatch trick in production: it breaks return-address prediction and shadow stacks.
- SSE aligned moves (`movaps`) on a misaligned stack fault; alignment bugs often show up there first.

## Self-check
Single-step a call in a debugger and watch rsp drop by 8 and `[rsp]` hold the return address.
