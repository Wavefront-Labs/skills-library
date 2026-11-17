---
id: computing-software.firmware-embedded-development.stm32.pcrop-and-write-protection
name: pcrop-and-write-protection
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-security, pcrop, wrp, readout-protection, rdp-levels, execute-only-code, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Protect STM32 flash with option bytes: RDP levels, write protection (WRP) for bootloaders, and PCROP execute-only regions for IP, including the compiler flags PCROP code needs."
sources:
  - https://www.st.com/resource/en/application_note/an5156-introduction-to-stm32-microcontrollers-security-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4968-proprietary-code-read-out-protection-pcrop-on-stm32f72xxx-and-stm32f73xxx-microcontrollers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PCROP and write protection

Three option-byte mechanisms, often combined:

| Mechanism | Protects against | Typical use |
|---|---|---|
| RDP (readout protection) | debugger/bootloader reading flash | every production unit |
| WRP (write protection) | erase/program of chosen pages, by anyone incl. your own app | bootloader, keys area |
| PCROP | **reads** of a region via data bus; code can only be executed | third-party library, licensed algorithm |

## RDP levels
- Level 0 (`0xAA`): open.
- Level 1 (any other value except `0xCC`): debug connection allowed but flash reads from the
  debugger/bootloader/RAM-booted code are blocked. Regression to level 0 **mass-erases** flash
  (PCROP areas too, depending on `PCROP_RDP`).
- Level 2 (`0xCC`): debug disabled permanently, option bytes frozen. **Irreversible.** Only
  with a field update path that doesn't need the debugger, and after a qualification run.
Newer series (L5/U5/H5) add RDP levels with password-based regression (`OEM key`); read the RM.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## WRP for a bootloader
Protect the bootloader pages so a bug or attacker in the app can't overwrite it (STM32L4 style):
```bash
STM32_Programmer_CLI -c port=SWD -ob WRP1A_STRT=0x0 WRP1A_END=0x7     # pages 0-7 of bank 1
```
Or from firmware with `HAL_FLASHEx_OBProgram()` (`OptionType = OPTIONBYTE_WRP`) followed by
`HAL_FLASH_OB_Launch()` (which resets the device). Bank/page numbering and field names differ
per series; F4 uses per-sector `nWRP` bits.

## PCROP
```bash
STM32_Programmer_CLI -c port=SWD -ob PCROP1_STRT=0x40 PCROP1_END=0x5F PCROP_RDP=1
```
Code inside PCROP is fetched via the instruction bus only. Any **data** read of the region
(including literal pools that the compiler places next to code, jump tables, constants) faults
or reads zero. Therefore the protected code must be built **execute-only**:
```
arm-none-eabi-gcc -mpure-code ...      # ARMv7-M/v8-M.main: no literal pools in .text
```
(Arm Compiler: `-mexecute-only`.) Constants must live outside the PCROP region. Typical flow:
the IP vendor delivers a pre-linked, execute-only library placed at a fixed address, and the
customer's app calls it through a header with function addresses.

## Order of operations in production
1. Program firmware and verify.
2. Program WRP/PCROP option bytes.
3. Set RDP level 1 (or 2 if the product qualifies).
4. Power cycle (RDP takes full effect after POR).
5. Verify: reading flash via the probe fails; the app boots.

## Gotchas
- Debugging PCROP code: you can't read it, so the debugger shows garbage; set breakpoints only
  on known addresses.
- WRP-protected pages can't be erased by a mass erase from your app; remember them when writing
  an in-app updater.
- RDP level 1 still allows SRAM access via debug on some parts. Don't keep secrets in RAM
  longer than necessary; combine with TrustZone/secure boot (see sbsfu-secure-boot-and-update).

## Verify
- [ ] CubeProgrammer read of the protected range fails with RDP 1 set.
- [ ] PCROP library executes correctly (built with `-mpure-code`, no data reads from region).
- [ ] App-level flash write to a WRP page is rejected (returns error, no corruption).

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
