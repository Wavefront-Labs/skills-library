---
id: computing-software.software-engineering.assembly.lock-atomics
name: lock-atomics
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, lock-atomics, asm-x86-string-atomic]
level: advanced
status: draft
description: "x86-64 atomic read-modify-write: LOCK prefix, XCHG, XADD, CMPXCHG, CMPXCHG16B, and a minimal spinlock with PAUSE."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# LOCK prefix and atomics
**Goal:** write correct lock-free primitives and spinlocks.

```nasm
lock add dword [rdi], 1          ; atomic increment
mov  eax, 1
lock xadd [rdi], eax             ; fetch-and-add; eax = old value
mov  eax, [rdi]                  ; compare-and-swap loop
.retry:
    lea  ecx, [rax + 1]
    lock cmpxchg [rdi], ecx      ; if [rdi]==eax then [rdi]=ecx else eax=[rdi]
    jne  .retry
```
- `xchg reg, mem` is implicitly locked (no LOCK prefix needed).
- `cmpxchg` compares with rax/eax/ax/al; ZF reports success.
- `cmpxchg16b` needs a 16-byte aligned operand and the CX16 feature (CPUID.1:ECX bit 13).
```nasm
spin_lock:                       ; rdi = &lock (0 free, 1 held)
    mov  eax, 1
.try:
    xchg eax, [rdi]
    test eax, eax
    jz   .got
.wait:
    pause
    cmp  dword [rdi], 0
    jne  .wait
    jmp  .try
.got: ret
spin_unlock:
    mov  dword [rdi], 0      ; plain store is a release on x86
    ret
```

## Gotchas
- LOCK on an operand split across cache lines is very slow (split lock); keep atomics naturally aligned.
- LOCK applies only to memory destinations; `lock add eax, 1` is #UD.

## Self-check
Run the increment from 4 threads and verify the exact total.
