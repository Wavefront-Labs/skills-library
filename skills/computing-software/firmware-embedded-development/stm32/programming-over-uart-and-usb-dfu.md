---
id: computing-software.firmware-embedded-development.stm32.programming-over-uart-and-usb-dfu
name: programming-over-uart-and-usb-dfu
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-programmer, cubeprogrammer-dfu, uart-bootloader, usb-dfu, boot0, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Flash STM32 parts without a debugger through the ROM bootloader over UART or USB DFU with STM32CubeProgrammer: boot pin entry, jump-to-bootloader from firmware and driver issues."
sources:
  - https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an3155-usart-protocol-used-in-the-stm32-bootloader-stmicroelectronics.pdf
  - https://www.st.com/resource/en/user_manual/um2237-stm32cubeprogrammer-software-description-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Programming over UART and USB DFU

Every STM32 has a ROM bootloader in system memory. AN2606 lists per part: which interfaces (USART,
USB DFU, I2C, SPI, CAN, FDCAN), which pins, and how to enter it.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Enter the bootloader
- **Pins**: BOOT0 = 1 at reset (and BOOT1/nBOOT1 or option bits on some series). G0/C0/L4+ may
  use option bytes `nBOOT_SEL`, `nSWBOOT0`, `nBOOT0` instead of a physical pin.
- **Empty flash**: many newer parts (G0, L4 with `nBOOT0` patterns, U5) boot the bootloader
  automatically when flash is blank.
- **From firmware** (field update button/command):
  ```c
  void jump_to_bootloader(void) {
      const uint32_t SYSMEM = 0x1FFF0000;       /* AN2606: per part (F4: 0x1FFF0000, L4: 0x1FFF0000, G0: 0x1FFF0000, H7: 0x1FF09800) */
      HAL_RCC_DeInit(); HAL_DeInit();
      SysTick->CTRL = 0; SysTick->LOAD = 0; SysTick->VAL = 0;
      __disable_irq();
      for (int i = 0; i < 8; i++) { NVIC->ICER[i] = 0xFFFFFFFF; NVIC->ICPR[i] = 0xFFFFFFFF; }
      __enable_irq();
      __HAL_SYSCFG_REMAPMEMORY_SYSTEMFLASH();    /* where available */
      __set_MSP(*(volatile uint32_t *)SYSMEM);
      ((void (*)(void))(*(volatile uint32_t *)(SYSMEM + 4)))();
  }
  ```
  Disabling all interrupts and peripherals first matters: a pending interrupt with a vector into
  your app crashes the bootloader. A cleaner method: set a RAM/backup-register flag, reset, and
  jump early in startup before any init.

## UART
```bash
STM32_Programmer_CLI -c port=COM5 br=115200 parity=even -w app.hex -v -s
```
8E1 framing, auto-baud from the 0x7F byte. Use the USART pins from AN2606 (often PA9/PA10).
Any other traffic on RX at reset can confuse auto-baud.

## USB DFU
```bash
STM32_Programmer_CLI -l usb
STM32_Programmer_CLI -c port=USB1 -w app.hex -v -s 0x08000000
```
- Needs HSE on many older parts (F2/F4: bootloader measures HSE to derive 48 MHz; unsupported
  crystal values fail). Newer parts use HSI48 + CRS.
- Windows: install the "STM32 Bootloader" driver (CubeProgrammer installer, or WinUSB via Zadig
  for dfu-util). `dfu-util -a 0 -s 0x08000000:leave -D app.bin` works cross-platform.

## RDP
With RDP level 1 the bootloader allows only mass erase (read-out unprotect) and write-memory
is refused; level 2 disables the bootloader entirely.

## Verify
- [ ] Firmware-initiated jump enters DFU reliably (100 attempts).
- [ ] UART flash at the production baud rate verifies OK.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
