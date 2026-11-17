---
id: computing-software.software-engineering.assembly.asm-unit-tests
name: asm-unit-tests
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, asm-unit-tests, asm-project]
level: practitioner
status: draft
description: "Test assembly routines from C: differential tests against reference implementations, boundary vectors, alignment sweeps and a callee-saved register preservation check."
sources:
  - https://gitlab.com/x86-psABIs/x86-64-ABI
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Testing asm routines from C
**Goal:** catch ABI violations and edge-case bugs automatically.

```c
#include <assert.h>
#include <string.h>
extern size_t my_strlen(const char *);
int main(void) {
    char buf[256];
    for (int off = 0; off < 16; off++)                 /* alignment sweep */
        for (int len = 0; len < 100; len++) {
            memset(buf, 'a', sizeof buf);
            buf[off + len] = 0;
            assert(my_strlen(buf + off) == (size_t)len);   /* differential vs known length */
        }
    return 0;
}
```
- Compare against a trusted reference (libc or a plain C version) on random and edge inputs: 0, 1, maximum, sign boundaries, page-edge buffers (place the buffer at the end of an `mmap`ed page followed by a guard page).
- Check preserved registers with a tiny shim that loads known values into callee-saved registers, calls the routine through a pointer, then compares:
```nasm
; int clobbered(void (*fn)(void)): 0 when rbx and r12 survive
clobbered:
    push rbx
    push r12
    sub  rsp, 8
    mov  rbx, 0x1111111111111111
    mov  r12, 0x2222222222222222
    call rdi
    mov  rax, 0x1111111111111111
    xor  rax, rbx
    mov  rcx, 0x2222222222222222
    xor  rcx, r12
    or   rax, rcx
    add  rsp, 8
    pop  r12
    pop  rbx
    ret
```
(Extend with rbp, r13-r15 for the full SysV set.)
- Run under Valgrind (works at machine-code level) and with `-fsanitize=undefined` on the C driver; AddressSanitizer does not instrument hand-written assembly.
- Add the tests to CI on every architecture you support.

## Gotchas
- A routine that passes on random data can still fail on alignment or page-boundary cases.
- Tests that call with a misaligned stack will pass in the shim but fail under libc; call through real C code too.

## Self-check
Break the routine by clobbering `rbx` and confirm the shim reports non-zero.
