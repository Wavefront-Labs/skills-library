---
id: computing-software.firmware-embedded-development.stm32.hse-startup-and-clock-security-system
name: hse-startup-and-clock-security-system
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-clocks, clock-security-system, hse, hse-bypass, hse-startup-timeout, css-nmi, stm32, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Bring up the STM32 HSE crystal or bypass clock robustly and enable the Clock Security System so an oscillator failure falls back to HSI via NMI instead of hanging."
sources:
  - https://www.st.com/resource/en/application_note/an2867-guidelines-for-oscillator-design-on-stm8afals-and-stm32-mcusmpus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HSE startup and the clock security system

## Crystal vs bypass
```c
RCC_OscInitTypeDef osc = {0};
osc.OscillatorType = RCC_OSCILLATORTYPE_HSE;
osc.HSEState = RCC_HSE_ON;          /* crystal/resonator on OSC_IN/OSC_OUT */
/* osc.HSEState = RCC_HSE_BYPASS;      external clock (TCXO, ST-LINK MCO) on OSC_IN only */
osc.PLL.PLLState = RCC_PLL_ON;
osc.PLL.PLLSource = RCC_PLLSOURCE_HSE;
...
if (HAL_RCC_OscConfig(&osc) != HAL_OK) { clock_fallback_to_hsi(); }
```
- Nucleo-64 boards feed 8 MHz from the ST-LINK MCO (fixed frequency, so that's **bypass**, not
  crystal; on NUCLEO-L476RG/L452RE the MCO is not connected and HSE is unused). Copying a
  Nucleo config to a custom board with a crystal (or vice versa) gives a non-starting HSE.
- `HSE_VALUE` in `stm32xxxx_hal_conf.h` (or `-DHSE_VALUE=`) must equal the real frequency.
  A wrong value builds and runs, but every baud rate and timer is off by the ratio.
- `HSE_STARTUP_TIMEOUT` (default 100 ms) bounds the wait for HSERDY.

## Don't hang on a dead crystal
CubeMX's `SystemClock_Config` calls `Error_Handler()` (an infinite loop) when HSE doesn't
start. A cracked crystal or bad solder joint then bricks the unit. Fall back instead:
```c
static void clock_fallback_to_hsi(void) {
    clock_fault = 1;                      /* report later */
    RCC_OscInitTypeDef osc = { .OscillatorType = RCC_OSCILLATORTYPE_HSI,
        .HSIState = RCC_HSI_ON, .HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT,
        .PLL.PLLState = RCC_PLL_ON, .PLL.PLLSource = RCC_PLLSOURCE_HSI, /* M/N/R for target */ };
    HAL_RCC_OscConfig(&osc);
    /* then HAL_RCC_ClockConfig with the matching flash latency */
}
```
HSI accuracy (15.88-16.08 MHz at 3.0 V/30 °C, about 1% over temperature per the L476
datasheet) is enough for UART at most baud rates but not for USB or CAN. Disable those
features in fallback mode.

## Clock security system (CSS)
```c
HAL_RCC_EnableCSS();      /* after HSE is running */
```
If HSE stops while in use, hardware switches SYSCLK to HSI (or MSI on some series), disables
HSE and the PLL fed by it, and raises an **NMI** (non-maskable).
```c
void NMI_Handler(void) { HAL_RCC_NMI_IRQHandler(); }   /* clears CSSF, calls callback */
void HAL_RCC_CSSCallback(void) {
    clock_fault = 1;
    /* SYSCLK is now HSI at reset frequency: SystemCoreClock is wrong until updated */
    SystemCoreClockUpdate();
    reinit_baud_rates_and_timers();   /* or trigger a controlled reset */
}
```
Without an NMI handler that clears the flag, the CPU re-enters the NMI forever.

LSE has its own CSS on many series (`HAL_RCCEx_EnableLSECSS()`, see lse-crystal-for-rtc).

## Hardware checks
Crystal load capacitors: `C1 = C2 = 2 x (CL - Cstray)` with Cstray ~2-5 pF. Check the
oscillator **gain margin** per AN2867 (should be >5). Verify frequency on MCO (see
clock-verification-via-mco).

## Verify
- [ ] Unit with HSE crystal removed boots on HSI and reports the fault.
- [ ] Shorting/removing HSE at run time triggers CSS callback and the system stays alive.
- [ ] MCO frequency measured within crystal tolerance; `HSE_VALUE` matches.

## Checked

2026-10-31: Confirmed HSE_STARTUP_TIMEOUT 100 ms default and HSE_VALUE 8 MHz (stm32l4xx_hal_conf_template.h); the CSS APIs and behaviour (`HAL_RCC_EnableCSS`, `HAL_RCC_NMI_IRQHandler` clearing CSSF and calling `HAL_RCC_CSSCallback`, the CSS failure interrupt linked to the Cortex-M4 NMI) from stm32l4xx_hal_rcc.h/.c; `SystemCoreClockUpdate` from system_stm32l4xx.c; the Nucleo ST-LINK MCO fixed at 8 MHz, including the NUCLEO-L476RG/L452RE exception where the MCO is not connected, from UM1724; HSI16 15.88-16.08 MHz at 3.0 V/30 degC from the STM32L476RG datasheet and the gain margin >5 rule from AN2867. Rewrote the Nucleo and HSI-accuracy sentences accordingly; the load-capacitor and gain-margin formulas are AN2867 guidance.

Method: documentation only; no commands were run.
