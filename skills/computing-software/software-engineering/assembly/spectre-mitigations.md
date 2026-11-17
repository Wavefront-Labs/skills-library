---
id: computing-software.software-engineering.assembly.spectre-mitigations
name: spectre-mitigations
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, spectre-mitigations, asm-security]
level: sme
status: draft
description: "Speculative-execution mitigations in assembly: LFENCE after bounds checks, index masking, retpoline thunks, and Arm CSDB/SB barriers."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://developer.arm.com/documentation/ddi0487/latest
  - https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Spectre mitigations: lfence, retpoline
**Goal:** know the standard code patterns that blunt speculative leaks.

- Variant 1 (bounds-check bypass): the CPU may speculatively read `a[i]` past the bounds check. Fix by serialising speculation or masking the index.
```nasm
cmp  rsi, rdx          ; index < length ?
jae  .oob
lfence                 ; stop speculation past the check (heavy)
mov  al, [rdi + rsi]
```
Index masking keeps the pipeline full: compute an all-ones or zero mask from the comparison with `cmp` / `sbb` or `cmov`, then `and` the index so a mispredicted path cannot use an out-of-range value (the pattern behind the Linux `array_index_nospec` helper).
- Variant 2 (branch target injection): compile indirect branches as retpolines so the CPU cannot use poisoned predictor entries.
```nasm
__x86_indirect_thunk_rax:      ; replaces: jmp rax
    call .set_up
.capture:
    pause
    lfence
    jmp  .capture             ; speculative path spins harmlessly
.set_up:
    mov  [rsp], rax           ; overwrite return address with the target
    ret                       ; non-speculatively jumps to rax
```
- Compiler flags: GCC `-mindirect-branch=thunk`, Clang `-mretpoline`, Clang `-mspeculative-load-hardening`, GCC/Clang `-mharden-sls` for straight-line speculation.
- Arm: `csdb` (consumption of speculative data barrier) and the `sb` speculation barrier instruction (FEAT_SB) provide the equivalent of `lfence`.
- Hardware features (eIBRS and similar) reduce or replace retpoline on newer CPUs; follow your OS and vendor guidance.

## Gotchas
- A mitigation that is correct on one CPU generation can be unnecessary or insufficient on another.
- On some AMD parts `lfence` is only a speculation barrier when set to be dispatch-serialising (unconfirmed details; follow vendor guidance).

## Self-check
Compile `-mretpoline` code with an indirect call and find the thunk call in the disassembly.
