---
id: computing-software.software-engineering.assembly.sve-predicates
name: sve-predicates
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, sve-predicates, asm-arm64-simd]
level: sme
status: gated
description: "AArch64 SVE: scalable Z registers, predicate registers, WHILELT loops and vector-length-agnostic code, with feature-detection caveats."
sources:
  - https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst
  - https://docs.kernel.org/arch/arm64/sve.html
  - https://gcc.gnu.org/onlinedocs/gcc/AArch64-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SVE predicates and vector-length-agnostic code
**Goal:** write one loop that runs on any SVE vector length.

- SVE adds scalable vector registers `z0`-`z31` (each extends the SIMD register of the same number: `z0` extends `v0`) and sixteen scalable predicate registers `p0`-`p15`, plus the first-fault register FFR. The vector length is a multiple of 16 bytes (128 bits), `16 <= VL <= VLmax`, and is chosen by the hardware or by the OS interface.
```asm
// void add(float *dst, const float *a, int n)   dst += a  (x0 dst, x1 a, w2 n)
    mov    x3, #0
    whilelt p0.s, x3, x2          // p0 = lanes where i < n
1:  ld1w   {z0.s}, p0/z, [x1, x3, lsl #2]
    ld1w   {z1.s}, p0/z, [x0, x3, lsl #2]
    fadd   z1.s, p0/m, z1.s, z0.s // merge-predicated
    st1w   {z1.s}, p0, [x0, x3, lsl #2]
    incw   x3                     // x3 += number of 32-bit lanes
    whilelt p0.s, x3, x2
    b.first 1b                    // loop while any lane active
    ret
```
- The meaning of `/z`, `/m`, `whilelt`, `incw`/`cntw`, `rdvl` and `b.first` comes from the Arm Architecture Reference Manual and the SVE instruction pages (gated: unconfirmed, source is paywalled or blocked).
- AAPCS64: `z0`-`z7` and `p0`-`p3` pass and return scalable arguments; if a routine takes or returns scalable vector or predicate values, all of `z8`-`z23` and `p4`-`p15` are callee-saved, otherwise only the low 64 bits of `z8`-`z15` are and all predicates are caller-saved.
- Detect SVE on Linux with `HWCAP_SVE` in the `AT_HWCAP` aux vector entry; `HWCAP2_SVE2` in `AT_HWCAP2` reports SVE2. GCC's `-march` table lists `+sve` as an extension (implied by `armv9-a`).

## Gotchas
- Never assume a particular vector length.
- Whether a given core implements SVE is a hardware fact; use the hwcap and fall back to NEON when it is absent.

## Self-check
Run under an emulator with different vector lengths and verify identical output.

## Checked
2026-11-02. Checked against AAPCS64 (scalable vector and predicate register sections), the Linux arm64 SVE document (register set, VL multiple of 16, `HWCAP_SVE`, `HWCAP2_SVE2`) and the GCC AArch64 options page (`+sve` extension). Gated: the instruction semantics in the example and the SVE mnemonic notes, because the Arm Architecture Reference Manual page is not readable. Removed: the 2048-bit upper bound, the `-march=armv8-a+sve` spelling and the claim about particular consumer cores lacking SVE.

Method: documentation only; no commands were run.
