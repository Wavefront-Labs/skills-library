---
id: computing-software.firmware-embedded-development.stm32.switching-sysclk-at-runtime
name: switching-sysclk-at-runtime
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-clocks, sysclk-switch, dynamic-frequency-scaling, voltage-scaling, low-power-run, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Change STM32 SYSCLK at runtime (PLL to MSI/HSI and back) safely: flash wait-state and voltage-scale ordering, peripheral re-init, SysTick and low-power run."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Switching SYSCLK at runtime

Lowering the clock during idle-but-awake phases cuts run current roughly in proportion.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Ordering rules
**Increasing frequency**: raise voltage scale first (wait VOSF), then increase flash wait
states, then switch the clock up.
**Decreasing frequency**: switch the clock down first, then reduce wait states, then lower
the voltage scale.
Getting this wrong runs the core faster than flash or regulator allow: random hard faults.
`HAL_RCC_ClockConfig(&clk, latency)` orders wait states relative to the switch for you;
voltage scaling (`HAL_PWREx_ControlVoltageScaling`) you sequence yourself.

## Example (L4): 80 MHz PLL -> 4 MHz MSI -> back
```c
void clock_low(void) {
    RCC_ClkInitTypeDef c = { .ClockType = RCC_CLOCKTYPE_SYSCLK | RCC_CLOCKTYPE_HCLK,
                             .SYSCLKSource = RCC_SYSCLKSOURCE_MSI, .AHBCLKDivider = RCC_SYSCLK_DIV1 };
    HAL_RCC_ClockConfig(&c, FLASH_LATENCY_0);                         /* MSI range 6 = 4 MHz */
    __HAL_RCC_PLL_DISABLE();                                          /* save PLL current */
    HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE2);    /* max 26 MHz */
    /* optional: HAL_PWREx_EnableLowPowerRunMode() at <= 2 MHz */
}
void clock_high(void) {
    HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1);    /* waits for VOSF */
    SystemClock_Config();                                             /* PLL on, latency 4, switch */
}
```

## After every switch
- `SystemCoreClock` updates in HAL; SysTick is re-initialised by `HAL_RCC_ClockConfig`.
- Peripherals using PCLK as kernel clock need re-init (UART baud, I2C timing, SPI prescaler,
  timer prescalers). Prefer HSI16/LSE kernel clocks for UART/I2C to avoid that.
- With FreeRTOS, `configCPU_CLOCK_HZ` is constant: the tick rate changes unless you
  reprogram SysTick (or use LPTIM tick). Do switches with the scheduler suspended.

## Low-power run
At <= 2 MHz with the regulator in low-power mode (`LPR`), run current drops further; exit LPR
before raising clocks or entering Stop 2.

## Verify
- [ ] Scope on MCO and a UART output during repeated switches: no garbled bytes, no faults.
- [ ] 100k switch cycles soak test.
- [ ] Measured current in low clock matches datasheet run-current tables.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
