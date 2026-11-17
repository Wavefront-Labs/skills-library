---
id: computing-software.firmware-embedded-development.stm32.afio-remapping-stm32f1
name: afio-remapping-stm32f1
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-gpio, afio-remap, stm32f1, jtag-remap, partial-remap, stm32, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Remap peripheral pins on STM32F1 with AFIO_MAPR (full/partial remaps, JTAG release), and avoid the classic F1 traps compared with per-pin AF selection on later series."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0008-stm32f101xx-stm32f102xx-stm32f103xx-stm32f105xx-and-stm32f107xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/datasheet/stm32f103c8.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AFIO remapping on STM32F1

STM32F1 has no per-pin alternate function number (no AFR registers like F2+). Each peripheral has
a fixed default pin set and a few remap options in `AFIO_MAPR` (and `AFIO_MAPR2`).

## Enable AFIO clock first
```c
__HAL_RCC_AFIO_CLK_ENABLE();      /* RCC_APB2ENR_AFIOEN; remap writes are ignored without it */
__HAL_AFIO_REMAP_USART1_ENABLE(); /* USART1 TX/RX from PA9/PA10 to PB6/PB7 */
__HAL_AFIO_REMAP_TIM2_PARTIAL_1();
__HAL_AFIO_REMAP_SWJ_NOJTAG();    /* free PA15, PB3, PB4; keep SWD */
```
Then configure pins: outputs as `GPIO_MODE_AF_PP`, inputs (USART RX, timer capture) as plain
`GPIO_MODE_INPUT` or `GPIO_MODE_AF_INPUT`; F1 has no AF selection for inputs, the peripheral
just reads the pin.

## JTAG pins
PA15 (JTDI), PB3 (JTDO), PB4 (NJTRST) are JTAG after reset. To use them as GPIO or for TIM2/SPI1
remaps, release JTAG with `SWJ_NOJTAG` (keeps SWD on PA13/PA14). Never use `SWJ_DISABLE` in
development: it kills SWD too and you need connect-under-reset to recover.

## MAPR write gotcha
`SWJ_CFG` bits are write-only and read back as 0. A read-modify-write of `AFIO_MAPR` can
re-enable full JTAG by accident. The HAL macros handle this by preserving SWJ bits; in register
code always OR in your SWJ setting on every MAPR write.

## Conflicts
- Remaps are all-or-nothing per peripheral: partial remap moves a fixed group of pins.
- Two peripherals sharing a pin (e.g. SPI1 remap and JTAG) both need resolving.
- CAN remap on F103 moves CAN to PB8/PB9 but those also host I2C1 remap.

## Porting to F4/L4
Later series replace MAPR with per-pin AF numbers (`GPIO_AFx_...` in `GPIOx->AFR`). Rebuild
the pin plan from the new datasheet's alternate function table; remap names don't carry over.

## Verify
- [ ] Remapped peripheral signals measured on the new pins.
- [ ] SWD still connects after JTAG release.

## Checked

2026-10-31: Confirmed `__HAL_AFIO_REMAP_USART1_ENABLE`, `__HAL_AFIO_REMAP_TIM2_PARTIAL_1`, `__HAL_AFIO_REMAP_SWJ_NOJTAG`/`SWJ_DISABLE`, `__HAL_AFIO_REMAP_CAN1_1`..`_3` and `__HAL_AFIO_REMAP_I2C1_ENABLE` from stm32f1xx_hal_gpio_ex.h, including the `AFIO_DBGAFR_CONFIG` read-modify-write handling of the write-only SWJ_CFG bits; `GPIO_MODE_AF_PP` and `GPIO_MODE_AF_INPUT` from stm32f1xx_hal_gpio.h; the pin roles PA15=JTDI, PB3=JTDO, PB4=NJTRST and PB8/PB9 carrying both the CAN remap and the I2C1 remap from the STM32F103C8 datasheet pin table.

Method: documentation only; no commands were run.
