---
id: computing-software.firmware-embedded-development.bootloader-development.ecc-flash-and-double-word-programming
name: ecc-flash-and-double-word-programming
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [flash-ecc, flash-programming, double-word-programming, eccd-nmi, write-once-granularity, firmware-embedded-development]
level: advanced
status: draft
description: "Program ECC-protected MCU flash (STM32L4/G4/H7/U5): 64-256 bit write units, no rewriting of written words, ECC double-error NMI on reads, and format consequences."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4894-eeprom-emulation-techniques-and-software-for-stm32-microcontrollers-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ECC flash and double-word programming

Many modern MCUs store ECC bits alongside each flash word. The ECC is computed over the whole
programming unit, which changes how firmware can write flash.

## Programming granularity
| Family | Unit |
|---|---|
| STM32L4, G4, WB | 64-bit double word (+8 ECC bits) |
| STM32U5, L5, H5 | 128-bit quad word |
| STM32H7 | 256-bit flash word |
| nRF52 | 32-bit word (no ECC exposure, but limited rewrites per word: `n_write`) |
Rules on ECC parts:
- Write the **whole unit at once**, aligned. Partial writes are impossible.
- A unit can be programmed **only once after erase**. Writing again (even to clear more bits, which
  works on older non-ECC flash) gives a programming error (`PROGERR`) or corrupts the ECC.
  Old "set flag by clearing bits later" tricks don't work.
- Erased state is all ones; ECC of an erased unit is consistent.

## Read-side ECC errors
- Single-bit errors are corrected silently (flag `ECCC`, address in `FLASH_ECCR`).
- Double-bit errors (`ECCD`) raise an **NMI** (STM32L4/G4) or bus error. Reading a unit that was
  interrupted mid-programming (power loss) can produce ECCD: your bootloader or settings reader
  then faults instead of seeing "invalid data".
  Handle it: in the NMI handler, check `FLASH->ECCR & FLASH_ECCR_ECCD`, record the address, clear the
  flag, and mark that page as invalid (skip the faulting load by adjusting the stacked PC, or
  re-design to verify via CRC with a fault-tolerant read routine).

## Consequences for update and storage formats
- Pad image chunks and records to the unit size (8/16/32 bytes); buffer incoming data until a full
  unit is available (`stream_flash` with `write-block-size` in Zephyr DT does this).
- Status flags in flash (e.g. "image valid", MCUboot trailer magic) occupy a full unit each.
  MCUboot handles this via `BOOT_MAX_ALIGN` and the flash driver's write-block-size.
- EEPROM emulation: records must be unit-sized; one write per unit per erase cycle.
- Never "patch" a written header field in place; write a new record instead.

## Verify
- [ ] All flash write paths write aligned, full units exactly once between erases (unit test against a flash simulator that enforces it).
- [ ] Simulated power cut during programming followed by reads does not hang: ECCD handled.
