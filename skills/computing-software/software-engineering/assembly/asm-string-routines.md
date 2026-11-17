---
id: computing-software.software-engineering.assembly.asm-string-routines
name: asm-string-routines
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, asm-string-routines, asm-data-patterns]
level: advanced
status: draft
description: "Write string and memory routines in assembly: a SysV x86-64 SSE2 strlen with aligned loads that never crosses a page, and loop patterns for memcpy-like code."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://gitlab.com/x86-psABIs/x86-64-ABI
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# String and memory routines
**Goal:** implement a correct vectorised `strlen` and understand its safety rules.

```nasm
; size_t strlen(const char *s)         SysV: rdi = s -> rax
global strlen
strlen:
    mov      rsi, rdi
    and      rdi, -16               ; aligned block containing s
    pxor     xmm0, xmm0
    movdqa   xmm1, [rdi]
    pcmpeqb  xmm1, xmm0             ; 0xFF where byte == 0
    pmovmskb eax, xmm1              ; 16-bit mask
    mov      ecx, esi
    and      ecx, 15
    shr      eax, cl                ; drop bytes before s
    test     eax, eax
    jnz      .first
.loop:
    add      rdi, 16
    movdqa   xmm1, [rdi]
    pcmpeqb  xmm1, xmm0
    pmovmskb eax, xmm1
    test     eax, eax
    jz       .loop
    bsf      eax, eax
    lea      rax, [rax + rdi]
    sub      rax, rsi
    ret
.first:
    bsf      eax, eax
    ret
```
- An aligned 16-byte load never crosses a 4 KiB page boundary, so reading a few bytes past the terminator stays inside a mapped page whenever the terminator's page is mapped. This is why libc implementations use aligned reads.
- Unaligned vector loads can fault when they straddle into an unmapped page.
- For copying: handle small sizes with overlapping loads, large sizes with a vector loop, and consider `rep movsb` on CPUs with ERMS; always define the overlap behaviour (`memcpy` forbids it, `memmove` handles it).
- Test with every start alignment 0..15 and every terminator position.

## Gotchas
- `bsf` of zero is undefined; the code branches before using it.
- Sanitizers may flag the intentional over-read; libc routines are exempted by interposition.

## Self-check
Fuzz-compare against libc `strlen` for all offsets and lengths 0..100.
