---
id: computing-software.firmware-embedded-development.bootloader-development.bootloader-size-budgeting
name: bootloader-size-budgeting
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [bootloader-architecture, bootloader-size, code-size, crypto-footprint, tinycrypt, mbedtls-config, bloaty, puncover, firmware-embedded-development]
level: advanced
status: draft
description: "Keep a bootloader inside its fixed flash budget for its whole life: measure per-component size, pick small crypto, strip HAL bloat and track growth in CI."
sources:
  - https://docs.mcuboot.com/design.html
  - https://github.com/google/bloaty
  - https://sourceware.org/binutils/docs/binutils/size.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bootloader size budgeting

**Goal:** the bootloader fits its reserved sectors today and after the security fixes you
will have to ship, because its region size can't change in the field.

## Typical footprints (Cortex-M, -Os, order of magnitude)
| Component | Size |
|---|---|
| Minimal jump + CRC32 check | 2-4 KB |
| UART/YMODEM loader | +3-6 KB |
| SHA-256 | 1.5-3 KB |
| ECDSA P-256 verify (TinyCrypt) | ~8-12 KB |
| ECDSA via mbedTLS (trimmed config) | ~20-35 KB |
| Ed25519 verify | ~6-10 KB |
| USB DFU device stack | 10-20 KB |
| Full STM32 HAL init for a few peripherals | 5-15 KB |
MCUboot with ECDSA-P256 and swap typically lands around 24-40 KB.

## Measure before arguing
```
arm-none-eabi-size -A -d boot.elf            # per-section
arm-none-eabi-nm --size-sort -S -C boot.elf | tail -30
bloaty boot.elf -d compileunits              # per source file
```
`puncover` gives a browsable per-function view with stack usage. Track the `.text + .rodata
+ .data` total as a CI metric and fail the build above, say, 85 % of the region.

## Reduction techniques (in order of payoff)
1. `-Os` (or `-Oz` with clang), `-ffunction-sections -fdata-sections -Wl,--gc-sections`,
   `--specs=nano.specs`, no `printf` with floats.
2. Replace HAL init with LL or register writes for the 3-4 peripherals used.
3. Choose compact crypto: TinyCrypt/`micro-ecc` or a trimmed mbedTLS config
   (`MBEDTLS_ECP_NIST_OPTIM` off, only P-256, no ASN.1 parse if keys are raw).
4. Use hardware: ROM crypto routines (some vendors ship them), hardware SHA/PKA.
5. Remove features: a bootloader that only verifies and swaps, with the download protocol
   in the application (MCUboot model), is far smaller than one with its own transport.
6. LTO (`-flto`) often saves 5-15 %, but verify that `KEEP()`ed vectors and weak handlers
   survive.

## Budget policy
- Reserve at least **1.5x** the first release size (e.g. 48 KB region for a 30 KB loader).
- Leave the transport/recovery code minimal and stable; put complexity in the updatable app.
- Record the size of every release; growth over time shows up early.

## Verify
- [ ] CI prints bootloader size and fails over the threshold.
- [ ] The release build with all security options enabled (debug off, logs off) is the one
      measured, and the debug build also fits (needed to debug in the field).
