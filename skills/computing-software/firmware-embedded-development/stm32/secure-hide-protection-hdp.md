---
id: computing-software.firmware-embedded-development.stm32.secure-hide-protection-hdp
name: secure-hide-protection-hdp
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-security, hdp, secure-hide-protection, hdpen, bootloader-isolation, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Use STM32 secure hide protection (HDP) on G0/G4/L5/U5/H7/H5 to make the boot or root-of-trust code and keys inaccessible after it runs, until the next reset."
sources:
  - https://www.st.com/resource/en/application_note/an5156-introduction-to-stm32-microcontrollers-security-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0440-stm32g4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure hide protection (HDP)

HDP (called "securable memory" on G0/G4, "secure access mode" region on H7, HDP on L5/U5/H5) marks
a flash area that is executable and readable only until software closes it. After closing, any
access (fetch, read, debug) returns errors or zero until the next reset. Typical content:
bootloader, root of trust, decryption keys.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Flow
1. Option bytes define the HDP region (e.g. G4: `SEC_SIZE1` pages from the bank start; L5/U5:
   `HDP1_PEND` with `HDP1EN` in the secure watermark option bytes).
2. Device boots into the hidden region (boot address must point into it).
3. Boot code verifies the application, derives/loads keys into peripherals (AES key registers),
   wipes RAM copies, then closes HDP and jumps:
   ```c
   /* G4 */  FLASH->CR |= FLASH_CR_SEC_PROT1;          /* HAL: HAL_FLASHEx_EnableSecMemProtection(FLASH_BANK_1) */
   /* U5 */  FLASH->SECHDPCR |= FLASH_SECHDPCR_HDP1_ACCDIS;
   jump_to_app();
   ```
4. Application cannot read or call bootloader code anymore.

## Combine with
- RDP level 1 or 2: at RDP 0 a debugger can halt at reset inside the hidden region, before it closes.
- WRP over the same area so the app can't erase/reprogram it.
- On TrustZone parts, HDP lives in secure flash; the non-secure world never sees it anyway, HDP
  additionally protects it from later secure code.

## Pitfalls
- Code in the region must not be called after closing (including ISRs vectored there, library
  functions linked into the bootloader and reused by the app: link them separately).
- Size changes require option byte changes, often only possible at RDP 0 (with regression erase).
- Debugging the bootloader: closing HDP makes breakpoints in it fault; use a debug build that
  skips the close.

## Verify
- [ ] After jump, reading the HDP area from the app returns zeros/faults.
- [ ] Debugger connecting under reset at production RDP cannot read the area.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
