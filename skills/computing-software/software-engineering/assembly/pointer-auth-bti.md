---
id: computing-software.software-engineering.assembly.pointer-auth-bti
name: pointer-auth-bti
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, pointer-auth-bti, asm-arm64-system]
level: sme
status: gated
description: "AArch64 hardening: pointer authentication (PACIASP/AUTIASP/RETAA) and branch target identification (BTI) in hand-written assembly and toolchain flags."
sources:
  - https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst
  - https://github.com/ARM-software/abi-aa/blob/main/sysvabi64/sysvabi64.rst
  - https://gcc.gnu.org/onlinedocs/gcc/AArch64-Options.html
  - https://docs.kernel.org/arch/arm64/elf_hwcaps.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pointer authentication and BTI
**Goal:** make assembly functions compatible with PAC/BTI-hardened binaries.

- BTI (Branch Target Identification) lets pages be guarded: an indirect branch from a guarded page must land on a `bti` instruction or an instruction with implicit BTI behaviour.
- The AArch64 SysV ABI requires that an executable or shared library that supports BTI has a `bti c` instruction at the start of any entry that might be called indirectly (it shows `bti c` at the start of PLT entries and `.got.plt[0]`).
- Return-address signing is the PAC side: `paciasp` and `autiasp` bracket a function that saves the link register (gated: unconfirmed, source is paywalled or blocked).
```asm
func:
    bti   c                      // landing pad for indirect calls
    paciasp                      // sign LR
    stp   x29, x30, [sp, #-16]!
    ...
    ldp   x29, x30, [sp], #16
    autiasp                      // authenticate LR
    ret
```
- Compilers: GCC documents `-mbranch-protection=standard` as turning on all branch-protection features; `pac-ret` signs the return address of functions that save it (A-key), `pac-ret+leaf` extends that to leaf functions, `+b-key` selects the B-key, and `bti` turns on branch target identification. Clang accepts `-mbranch-protection=<arg>` too.
- Mark objects with the GNU property note `GNU_PROPERTY_AARCH64_FEATURE_1_AND` (type 0xc0000000): bit 0 is `..._FEATURE_1_BTI` (all executable sections compatible with BTI) and bit 1 is `..._FEATURE_1_PAC`. A static linker sets a bit in its output only if every input object has it, and a loader may then enable the feature for that file.
- Linux exposes `HWCAP_PACA` (address authentication) and `HWCAP2_BTI` in the auxiliary vector hwcaps.

## Gotchas
- Hand-written code without `bti c` at indirectly called entry points leaves the object unmarked, and the linker then clears the BTI bit for the whole output.
- Exact `bti c/j/jc` target semantics, the NOP-on-older-cores behaviour of the hint instructions, `retaa`, and the `.cfi_negate_ra_state` directive are in the Arm ARM and binutils manual, which were not read; verify there before relying on them.

## Self-check
Disassemble a PAC-enabled compiler output and match your prologue/epilogue to it.

## Checked
2026-11-02. Checked against AAELF64 (BTI definition), AArch64 SysV ABI (BTI PLT requirement, `GNU_PROPERTY_AARCH64_FEATURE_1_AND` bits and static-linker rule), GCC AArch64 options (`-mbranch-protection` forms) and the kernel arm64 ELF hwcaps page (`HWCAP_PACA`, `HWCAP2_BTI`). Gated: the `paciasp`/`autiasp` roles and the example's PAC instructions (Arm ARM not readable). Removed: the `bti j`/`jc` semantics, the NOP-compatibility claim, `.cfi_negate_ra_state`, `retaa`/FEAT_PAuth and the dynamic loader detail, which sit in pages not readable here (Arm ARM).

Method: documentation only; no commands were run.
