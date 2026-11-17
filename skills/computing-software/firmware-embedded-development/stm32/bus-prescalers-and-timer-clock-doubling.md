---
id: computing-software.firmware-embedded-development.stm32.bus-prescalers-and-timer-clock-doubling
name: bus-prescalers-and-timer-clock-doubling
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-clocks, apb-prescaler, ahb-prescaler, timer-clock-x2, pclk-frequency, stm32, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Set STM32 AHB/APB prescalers within limits and compute timer clocks correctly, including the x2 rule when an APB prescaler is not 1 and its effect on peripherals."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bus prescalers and timer clock doubling

## Limits
Each bus has a maximum frequency from the datasheet. STM32F407 at 168 MHz:
HCLK 168, APB1 max 42 (prescaler /4), APB2 max 84 (/2). STM32L4 at 80 MHz: both APBs can run
at 80 (/1). STM32H7 has AHB/APB domains D1/D2/D3 with their own prescalers (`D1PPRE`, `D2PPRE1`...).

## Timer clock rule
If an APB prescaler is 1, timers on that bus get PCLK. If it is greater than 1, timers get
**2 x PCLK**. (Some series have `TIMPRE` that makes it 4x or HCLK; H7 has `TIMPRE` in RCC_CFGR.)

F407 example: APB1 = 42 MHz with /4 -> TIM2-7, 12-14 clocked at 84 MHz; APB2 = 84 MHz with /2 ->
TIM1, TIM8-11 at 168 MHz.

Get it right in code:
```c
uint32_t tim_clk(TIM_TypeDef *t) {
    uint32_t pclk, ppre;
    if (IS_APB2_TIM(t)) { pclk = HAL_RCC_GetPCLK2Freq(); ppre = RCC->CFGR & RCC_CFGR_PPRE2; }
    else                { pclk = HAL_RCC_GetPCLK1Freq(); ppre = RCC->CFGR & RCC_CFGR_PPRE1; }
    return (ppre == 0) ? pclk : 2 * pclk;    /* PPREx = 0xx means /1 */
}
```
`IS_APB2_TIM` is your own macro based on the RM's bus map. CubeMX's clock tree shows
"APB1 Timer clocks" directly.

## Choosing prescalers
- Max APB for fastest peripheral access and timer resolution.
- Lower APB to save power on idle buses (dynamic power scales with clock).
- UART max baud = PCLK/8 (oversampling 8) or /16. SPI max = PCLK/2.
- ADC clock has its own limit (e.g. F4 ADCCLK max 36 MHz from APB2 /4 prescaler in ADC_CCR).

## Changing at runtime
`HAL_RCC_ClockConfig()` updates prescalers; afterwards re-init UART/SPI/timers clocked from
PCLK, and call `HAL_InitTick()` (HAL does it) so SysTick stays 1 ms.

## Verify
- [ ] Timer period measured on scope matches computed value (x2 rule applied).
- [ ] All bus clocks within datasheet maximum for the chosen voltage scale.

## Checked

2026-10-31: Confirmed the F407 bus limits (APB1 42 MHz max, APB2 84 MHz max) and the timer x2 rule from the STM32F407VG datasheet timer tables; `RCC_CFGR_PPRE1`/`PPRE2`, `RCC_DCKCFGR_TIMPRE` (F4) and `RCC_CFGR_TIMPRE` (H7) plus the H7 `D1PPRE`/`D2PPRE` domain prescalers from the CMSIS device headers; `HAL_RCC_GetPCLK1Freq`/`GetPCLK2Freq`, `HAL_RCC_ClockConfig` and `HAL_InitTick` from the L4 HAL sources; the F407 ADC clock limit (fADC up to 36 MHz) from the datasheet. L4 maximum 80 MHz and the mode tables per AN4621.

Method: documentation only; no commands were run.
