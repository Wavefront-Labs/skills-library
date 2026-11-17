---
id: computing-software.software-engineering.assembly.asm-arrays-structs
name: asm-arrays-structs
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, asm-arrays-structs, asm-data-patterns]
level: practitioner
status: draft
description: "Address array elements and struct fields in assembly: offsets, natural alignment and padding, scaled indexing, NASM struc, and keeping C and assembly layouts in sync."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://www.nasm.us/doc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Array loops and struct offsets
**Goal:** index arrays and structs without off-by-one layout bugs.

```c
struct P { int x; int y; };            /* size 8, y at offset 4 */
struct Q { char c; long l; };          /* size 16: 7 bytes padding, l at offset 8 */
long sum_y(const struct P *a, long n);
```
```nasm
; long sum_y(const struct P *a, long n)
sum_y:
    xor  eax, eax                       ; sum
    xor  ecx, ecx                       ; i
    test rsi, rsi
    jle  .done
.loop:
    movsxd rdx, dword [rdi + rcx*8 + 4] ; a[i].y   (scale 8 = sizeof(struct P))
    add  rax, rdx
    inc  rcx
    cmp  rcx, rsi
    jl   .loop
.done:
    ret
```
- Scaled index handles element sizes 1, 2, 4, 8. For other sizes compute `imul rax, rcx, SIZE` (or `lea` combinations) and add the base.
- C layout rule: each field is placed at the next multiple of its alignment, and the struct size is a multiple of its largest alignment. Verify with `offsetof` and `sizeof`.
- Keep layouts in sync by generating constants from C: compile a tiny program printing `offsetof(struct P, y)` or use `_Static_assert(offsetof(struct P, y) == 4, "layout")` next to a header shared with assembly.
- AArch64: `ldrsw x2, [x0, x3, lsl #3]` style scaled loads; add the field offset with `add x4, x0, #4` first when the offset is not encodable in the addressing mode.

## Gotchas
- `packed` structs and bit-fields change offsets; mirror them exactly or avoid touching them in assembly.
- Signed versus unsigned index extension (`movsxd` versus 32-bit write) changes behaviour for negative indices.

## Self-check
Add a `char tag` field in the middle of the struct in C and see which assembly constants must change.
