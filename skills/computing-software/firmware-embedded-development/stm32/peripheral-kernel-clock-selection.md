---
id: computing-software.firmware-embedded-development.stm32.peripheral-kernel-clock-selection
name: peripheral-kernel-clock-selection
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-clocks, kernel-clock, periphclk-config, ccipr, independent-clock, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Choose STM32 peripheral kernel clocks (UART, I2C, ADC, USB, SPI on H7) via RCC_CCIPR muxes so peripherals keep exact rates, work in Stop mode and survive SYSCLK changes."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0433-stm32h742-stm32h743753-and-stm32h750-value-line-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Peripheral kernel clock selection

Newer STM32s separate a peripheral's **bus clock** (register access, APB) from its **kernel
clock** (what drives baud rate, sampling, timing). The kernel clock is selected per peripheral
in `RCC_CCIPR`/`CCIPR2` (L4, G4, U5) or `RCC_D1CCIPR/D2CCIP1R/D3CCIPR` (H7).

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Typical choices
| Peripheral | Options (L4 example) | Pick when |
|---|---|---|
| USART/LPUART | PCLK, SYSCLK, HSI16, LSE | HSI16 for wake from Stop and fixed baud regardless of SYSCLK; LSE for 9600 LPUART in Stop 2 |
| I2C | PCLK, SYSCLK, HSI16 | HSI16 to keep timing register valid across clock changes, address-match wake |
| ADC | PLLSAI1R, PLLSAI2R, SYSCLK | dedicated PLL output for exact sample rate |
| USB/RNG/SDMMC (CLK48) | HSI48, PLLSAI1Q, PLLQ, MSI | 48 MHz exact |
| LPTIM | PCLK, LSI, HSI16, LSE | LSE/LSI for Stop mode operation |
| SPI/SAI (H7) | PLL1Q, PLL2P, PLL3P, PER_CK | audio-friendly PLL for SAI |

## Configure
```c
RCC_PeriphCLKInitTypeDef p = {0};
p.PeriphClockSelection = RCC_PERIPHCLK_USART2 | RCC_PERIPHCLK_I2C1 | RCC_PERIPHCLK_LPUART1;
p.Usart2ClockSelection = RCC_USART2CLKSOURCE_HSI;
p.I2c1ClockSelection = RCC_I2C1CLKSOURCE_HSI;
p.Lpuart1ClockSelection = RCC_LPUART1CLKSOURCE_LSE;
HAL_RCCEx_PeriphCLKConfig(&p);
```
The HAL computes baud and timing from the selected source (`HAL_RCCEx_GetPeriphCLKFreq`).
The I2C `Timing` register value from CubeMX depends on the kernel clock: changing source
needs a new value.

## Stop mode
Peripherals that must work or wake in Stop need a kernel clock that runs in Stop (HSI16 with
`HSIKERON`/wake-up capability, LSE, LSI) and the UESM/WUPEN bits. PCLK stops.

## Gotchas
- Switching SYSCLK frequency (e.g. low-power run) breaks baud rates only for peripherals
  clocked from PCLK/SYSCLK; kernel-clock choice isolates them.
- The source oscillator must be enabled; selecting HSI16 for USART without HSI on gives no clock
  (HAL may enable it, but in LL code it is your job).
- H7: some PLL outputs (PLL2/3) must be enabled separately and their dividers set before selecting them.

## Verify
- [ ] Baud rate measured on scope unchanged after SYSCLK change.
- [ ] Peripheral wakes the device from Stop with the chosen kernel clock.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
