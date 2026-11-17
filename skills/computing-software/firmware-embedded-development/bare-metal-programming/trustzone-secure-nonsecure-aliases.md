---
id: computing-software.firmware-embedded-development.bare-metal-programming.trustzone-secure-nonsecure-aliases
name: trustzone-secure-nonsecure-aliases
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [secure-alias, trustzone-m, memory-aliasing, gtzc, idau, firmware-embedded-development]
level: advanced
status: draft
description: "Work with TrustZone-M secure/non-secure address aliases (STM32 0x0C000000 vs 0x08000000): per-world linker scripts, peripheral attribution, access faults."
sources:
  - https://www.st.com/resource/en/application_note/an5347-arm-trustzone-features-for-stm32l5-and-stm32u5-series-stmicroelectronics.pdf
  - https://developer.arm.com/documentation/100690/latest/
  - https://developer.arm.com/documentation/ddi0553/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure and non-secure memory aliases

Most ARMv8-M MCUs expose each memory and peripheral at **two addresses**: a non-secure alias and
a secure alias, distinguished by one address bit (address bit 28 on STM32L5/U5/H5, Nordic nRF91/53
and NXP LPC55S use similar schemes). The IDAU (implementation-defined attribution unit) marks the
alias ranges secure or non-secure; the SAU (programmed by secure code) can only make things
*more* secure.

## STM32U5 example
| Resource | Non-secure | Secure |
|---|---|---|
| Flash | 0x0800_0000 | 0x0C00_0000 |
| SRAM1 | 0x2000_0000 | 0x3000_0000 |
| Peripherals | 0x4000_0000 | 0x5000_0000 |
Same physical memory, two views. Whether the access succeeds depends on the alias used *and*
the security state of the memory block (flash watermarks/option bytes, GTZC MPCBB for SRAM
blocks, GTZC TZSC for peripherals).

## Linker scripts per world
Secure image links against secure aliases, non-secure against non-secure:
```ld
/* secure */   FLASH (rx) : ORIGIN = 0x0C000000, LENGTH = 256K
               RAM  (rwx) : ORIGIN = 0x30000000, LENGTH = 96K
/* non-secure */ FLASH (rx) : ORIGIN = 0x08040000, LENGTH = 768K
                 RAM  (rwx) : ORIGIN = 0x20018000, LENGTH = 672K
```
The physical ranges must not overlap between worlds. Device headers provide both sets:
`GPIOA_NS`/`GPIOA_S`; the plain `GPIOA` macro resolves by `__ARM_FEATURE_CMSE == 3` (secure build).

## Peripheral and memory attribution
- Peripherals: GTZC `TZSC->SECCFGRx` sets each peripheral secure or non-secure; `PRIVCFGRx` for
  privilege. A non-secure access to a secure peripheral is RAZ/WI or raises an illegal-access
  interrupt (`GTZC_IRQn`), depending on configuration.
- SRAM: GTZC MPCBB marks 512-byte blocks secure/non-secure.
- Flash: secure watermark option bytes (`SECWM1_PSTRT/PEND`).
- GPIO pins individually: `GPIOx->SECCFGR`. A pin left secure (the reset default on STM32 with
  TZEN=1) cannot be driven by non-secure code: the classic "my non-secure LED does nothing".

## Debugging access faults
- Non-secure code touching a secure alias: SecureFault (`SFSR.AUVIOL`), handled in the secure world.
- Secure code using the wrong alias for non-secure-owned memory: works or not depending on
  attribution; always use the alias matching the target's security.
- Debuggers need the right alias to show memory: reading 0x0800_0000 from a secure debug session
  may show non-secure flash contents only if that flash is non-secure.

## Verify
- [ ] Map files of both images use only their world's aliases.
- [ ] Each peripheral and GPIO used by the non-secure app is set non-secure in GTZC/GPIO SECCFGR during secure boot.
