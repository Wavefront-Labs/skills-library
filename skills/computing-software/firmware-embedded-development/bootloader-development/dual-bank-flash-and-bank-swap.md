---
id: computing-software.firmware-embedded-development.bootloader-development.dual-bank-flash-and-bank-swap
name: dual-bank-flash-and-bank-swap
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [flash-bank-swap, flash-programming, dual-bank, read-while-write, swap-bank-option, firmware-embedded-development]
level: advanced
status: draft
description: "Use dual-bank flash for updates: run from one bank while programming the other, then swap banks via option bytes (STM32 SWAP_BANK/BFB2), with rollback and pitfalls."
sources:
  - https://www.st.com/resource/en/application_note/an4767-onthefly-firmware-update-for-dual-bank-stm32-microcontrollers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0440-stm32g4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dual-bank flash and bank swap

Parts with two independent flash banks (STM32F42x/F76x/G47x/L4+/H7/U5, NXP LPC55 some, Kinetis
with swap) allow reading/executing from one bank while erasing and programming the other: no
stalls, no RAM-resident flash routines, and an atomic switch.

## Update flow (STM32 example)
1. App runs from bank 1 (mapped at 0x0800_0000).
2. App receives the new image and programs it into bank 2 (mapped at 0x0808_0000 for a 1 MB part
   with 512 KB banks); CPU keeps running (read-while-write).
3. Verify bank 2 (CRC/signature).
4. Toggle the swap option bit: STM32G4/L4+ `BFB2` (boot from bank 2) or H7/U5 `SWAP_BANK`; unlock
   option bytes, change bit, `OBL_LAUNCH` (option byte reload) which resets the device.
5. After reset, bank 2 is **mapped at 0x0800_0000**: the same image, linked for 0x0800_0000, runs
   from the other physical bank. No relinking required.
```c
HAL_FLASH_Unlock(); HAL_FLASH_OB_Unlock();
FLASH_OBProgramInitTypeDef ob = { .OptionType = OPTIONBYTE_USER, .USERType = OB_USER_BFB2,
                                  .USERConfig = current_bfb2 ? OB_BFB2_DISABLE : OB_BFB2_ENABLE };
HAL_FLASHEx_OBProgram(&ob);
HAL_FLASH_OB_Launch();      /* resets */
```

## Rollback
The old image remains intact in the other bank. If the new image fails its self-test, toggle the
bit back. Combine with a watchdog: a new image that hangs is reset by the IWDG; boot logic (a
small bootloader, or the app's early init on BFB2 parts where the ROM checks both banks) decides
whether to swap back based on a boot attempt counter.

## Pitfalls
- **Bank size mode**: some parts (STM32G4 cat. 3, L4+) can be single-bank or dual-bank via
  `DBANK` option byte; in single-bank mode there is no swap. Check before designing.
- Data at absolute addresses (settings, calibration) shifts with the swap: keep persistent data in
  a region not affected (dedicated bank area, external flash) or account for the mapping
  (`FLASH_OPTR` / `SYSCFG_MEMRMP.FB_MODE` tells you which bank is current).
- Write protection and PCROP areas are per bank; mirror them.
- Debuggers may show the physical bank, not the mapped one; reprogramming the "wrong" bank in
  production programming scripts is a common mistake.
- BFB2 boot behaviour involves the ROM bootloader checking bank validity (first word as stack
  pointer) on some families: an erased bank 2 with BFB2 set boots bank 1 or the system bootloader.

## Verify
- [ ] Update + swap works repeatedly in both directions; persistent settings survive swaps.
- [ ] A new image that never confirms swaps back after N watchdog resets.
