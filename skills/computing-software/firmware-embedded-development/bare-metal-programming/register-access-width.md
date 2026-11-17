---
id: computing-software.firmware-embedded-development.bare-metal-programming.register-access-width
name: register-access-width
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [register-access-width, mmio, byte-access, unaligned-access, packed-struct, firmware-embedded-development]
level: advanced
status: draft
description: "Match register access width to the peripheral (8/16/32-bit), stop the compiler from splitting or widening MMIO accesses, and avoid packed/unaligned access faults."
sources:
  - https://developer.arm.com/documentation/ddi0403/latest/
  - https://gcc.gnu.org/onlinedocs/gcc/ARM-Options.html
  - https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Register access width and unaligned access

Reference manuals state per peripheral: "The peripheral registers have to be accessed by words
(32 bits)" or "can be accessed by half-words or words". Wrong width means ignored writes,
duplicated bytes, or a BusFault.

## Typical cases
- **32-bit-only peripherals** (many RCC, GPIO on some parts, most Cortex-M PPB registers): a byte
  store may be ignored or replicated across all four lanes.
- **Data registers that care:** STM32 SPI `DR` with FIFO (F0/F3/L4/G4): an 8-bit write sends one
  byte, a 16-bit write sends two (packing). To send one byte:
  `*(volatile uint8_t *)&SPI1->DR = b;`. Reading `DR` as 16-bit pops two bytes from RXFIFO.
- **CRC unit:** writing `DR` as byte, half-word or word feeds 8/16/32 bits into the CRC.
- **PPB (0xE000_0000)**: NVIC IPR registers support byte access (CMSIS uses `NVIC->IP[n]` as
  bytes on v7-M), but v6-M (M0) IPR is word-access only: CMSIS M0 headers do RMW on words.

## Compiler-generated surprises
- C bit-fields in a register struct (`REG.bits.EN = 1;`) may compile to byte or half-word
  load/store. GCC flag `-fstrict-volatile-bitfields` (default on ARM EABI) forces the declared
  container width; don't rely on it with other compilers. Prefer masks.
- `memcpy` to or from peripheral memory (USB packet RAM, CAN mailboxes, external SRAM) may use
  byte, unaligned word or LDM accesses. Write explicit loops with `volatile uint32_t *`.
- USB packet memory on STM32F1/F3 is 16-bit wide with 32-bit address stride: only half-word
  access at word-aligned addresses.

## Unaligned access
- ARMv7-M allows unaligned LDR/STR/LDRH/STRH to **Normal** memory (slower); unaligned access to
  **Device** memory always faults (UNALIGNED in UFSR or precise BusFault).
- LDM/STM/LDRD/STRD and all ARMv6-M (M0/M0+) accesses must be aligned.
- `__attribute__((packed))` structs make GCC assume misalignment; with `-munaligned-access`
  (default on v7-M) it may emit unaligned LDRs. Don't overlay packed structs on peripherals; for
  M0 targets, GCC emits byte-wise access for packed fields (correct but slow).
- `-mno-unaligned-access` forces byte access for any possibly-unaligned data.

## Verify
- [ ] Disassembly of each driver register access shows the intended `STRB/STRH/STR`.
- [ ] SPI 8-bit frames: logic analyser shows one byte per write.
- [ ] Enable `CCR.UNALIGN_TRP` in a test build to find accidental unaligned accesses.
