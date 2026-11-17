---
id: computing-software.firmware-embedded-development.stm32.hardware-watchdog-option-byte
name: hardware-watchdog-option-byte
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-watchdog, hardware-watchdog, iwdg-sw, watchdog-auto-start, wwdg-sw, stm32, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use the STM32 hardware watchdog option bytes (IWDG_SW, WWDG_SW) so the watchdog starts at reset before any code runs, and handle bootloaders, debugging and long init."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4435-guidelines-for-obtaining-ulcsaiec-607301-class-b-certification-in-any-stm32-application-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardware watchdog option byte

With `IWDG_SW = 0` (hardware watchdog), the IWDG starts automatically at every reset with its
default prescaler/reload settings (check the IWDG reset values in your reference manual; at
/4 and a full reload that is roughly 0.5 s at a 32 kHz LSI). Software can't stop it.
This protects against code that hangs before it would have started the watchdog (corrupted
startup, bootloader hang, early clock init failure). Required or recommended by IEC 60730 Class B
style designs.

## Set
Program it with STM32CubeProgrammer's option-byte editing (IWDG_SW; the CLI commands are in
UM2237) or with the firmware sequence below.
Some series also have `WWDG_SW = 0` (window watchdog starts at reset) - rarely used because WWDG
timeouts are short.

## Consequences
- **Every boot stage must refresh within ~512 ms** (or the default timeout for your LSI range):
  bootloader, C runtime init (zeroing large .bss on slow clocks), clock setup with HSE startup
  timeouts, external RAM tests. Measure boot time to first refresh.
- Reconfigure early: write PR/RLR in the first lines of `main` (or even in `SystemInit`) to the
  application's timeout. Writing `IWDG->KR = 0x5555` then PR/RLR works with hardware watchdog too.
- Bootloader update loops (receiving firmware over UART) must refresh.
- ROM system bootloader: only some parts refresh the IWDG while in the bootloader. Check AN2606
  per part ("IWDG" note); on the others a hardware watchdog resets the device mid-flash.
- Debugging: freeze it on halt (`DBGMCU` IWDG freeze), or every breakpoint resets after 0.5 s.
- Low power: combine with IWDG_STOP/STDBY option bits or periodic wakes.

## Detecting watchdog resets
At boot read `RCC_CSR` (`__HAL_RCC_GET_FLAG(RCC_FLAG_IWDGRST)`), log a counter in a backup
register, clear flags with `__HAL_RCC_CLEAR_RESET_FLAGS()`. Repeated watchdog resets in boot ->
enter a safe/recovery mode instead of looping.

## Verify
- [ ] Blank-loop firmware without refresh resets every ~0.5 s (proves the option is active).
- [ ] Measured boot time to first refresh well below the default timeout at the slowest clock config.

## Checked

2026-10-31: Confirmed the `IWDG_SW`/`WWDG_SW` option bits (stm32l476xx.h), the HAL OB constants (`OB_IWDG_HW`/`OB_IWDG_SW`, `IS_OB_USER_IWDG`), `RCC_FLAG_IWDGRST` and reset-flag clearing (stm32l4xx_hal_rcc.h), and the Class-B recommendation to enable the IWDG through the hardware option bytes from AN4435. Rewrote the default-timeout claim to point at the IWDG reset values in the reference manual (RM0351 exceeds the fetch size limit) and the CubeProgrammer line to a UM2237 pointer (its PDF redirects to a JS-only docs site).

Method: documentation only; no commands were run.
