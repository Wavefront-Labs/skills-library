---
id: computing-software.firmware-embedded-development.hardware-debugging.clock-verification-via-mco
name: clock-verification-via-mco
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [board-bring-up, mco-clock-output, hse-startup, crystal-verification, clock-out-pin, frequency-counter, pll-check, firmware-embedded-development]
level: practitioner
status: draft
description: "Verify crystals, PLL output and system clock frequency on new hardware by routing clocks to the MCO pin, without loading the oscillator with a probe."
sources:
  - https://www.st.com/resource/en/application_note/an2867-guidelines-for-oscillator-design-on-stm8afals-and-stm32-mcusmpus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clock verification via MCO

**Goal:** prove the external crystal oscillates at the right frequency and the PLL produces
the expected system clock, before trusting UART baud rates, USB or timing.

## Why not probe the crystal
A 10x probe adds ~10-15 pF to XTAL pins and can stop a marginal oscillator or shift its
frequency by tens of ppm. Route the clock out through the **MCO** (microcontroller clock
output) pin instead, buffered by the MCU.

## STM32 example
```c
/* MCO1 on PA8: output HSE / 1 */
HAL_RCC_MCOConfig(RCC_MCO1, RCC_MCO1SOURCE_HSE, RCC_MCODIV_1);
/* MCO2 on PC9 (F4): SYSCLK / 4, keeps frequency within GPIO capability */
HAL_RCC_MCOConfig(RCC_MCO2, RCC_MCO2SOURCE_SYSCLK, RCC_MCODIV_4);
```
Sources typically include HSI, HSE, LSE, LSI, PLL, SYSCLK. Use the divider to stay within
the pin's speed (set GPIO speed very high for > 50 MHz) and the scope's bandwidth.
Other vendors: NXP `CLKOUT`, nRF none (use a timer toggling a pin via PPI/GPIOTE), ESP32
`CLK_OUT` pins.

## What to check
- **Frequency**: scope frequency measurement or a frequency counter; crystal error should be
  within its tolerance (+/-20-50 ppm). Larger offsets suggest wrong load capacitors.
- **HSE startup**: does `HSERDY` set? Time from enable to ready (normally < 2-10 ms). Failure =
  wrong load caps, wrong crystal type, drive level setting, or layout.
- **LSE (32.768 kHz)**: very sensitive to load capacitance and leakage (flux residue!); check
  startup over temperature. LSE drive-strength setting (`LSEDRV`) low saves power but may fail
  to start on some crystals.
- **PLL**: SYSCLK/N on MCO matches calculation from `PLLM/N/P`.
- **Clock security system** behaviour: disconnect HSE (in a test) and verify CSS switches to HSI
  and raises NMI.

## Load capacitor maths
`C_L = (C1 x C2)/(C1 + C2) + C_stray`, with C_stray ~2-5 pF. For a 12 pF crystal and 4 pF
stray, C1 = C2 = 16 pF. Measure the actual frequency and adjust: too low frequency = too much
capacitance.

## Verify
- [ ] MCO frequency measured and logged per board in bring-up.
- [ ] HSE/LSE start reliably at cold and hot temperature extremes.
