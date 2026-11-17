---
id: computing-software.firmware-embedded-development.stm32.ll-utilities
name: ll-utilities
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-ll, ll-utils, ll-mdelay, ll-init-1mstick, ll-setsystemcoreclock, stm32, firmware-embedded-development]
level: practitioner
status: draft
description: "Use STM32 LL utility functions (stm32xxxx_ll_utils) for clock setup, 1 ms tick, blocking delays and device info in HAL-free projects, and know their limits."
sources:
  - https://www.st.com/resource/en/user_manual/um1884-description-of-stm32l4l4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
  - https://github.com/STMicroelectronics/stm32l4xx_hal_driver
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LL utilities

`stm32xxxx_ll_utils.c/.h` provides the few services a HAL-free project needs: system clock
configuration helpers, SysTick-based delays and device identification.

## Tick and delay
```c
LL_Init1msTick(SystemCoreClock);          /* SysTick reload for 1 ms, no interrupt */
LL_SetSystemCoreClock(80000000);          /* updates the CMSIS SystemCoreClock variable */
LL_mDelay(100);                            /* busy-waits on SysTick COUNTFLAG */
```
- `LL_mDelay` polls SysTick's COUNTFLAG; it does not use interrupts and doesn't need a tick ISR.
  If you also run SysTick as an interrupt-driven tick (RTOS, own `SysTick_Handler`), the
  COUNTFLAG read in LL_mDelay is cleared by whichever reader sees it first: delays become wrong.
  Use one or the other.
- `LL_mDelay(n)` waits at least n ms (adds one tick for safety).

## Clock configuration helpers
```c
LL_UTILS_PLLInitTypeDef pll = { .PLLM = LL_RCC_PLLM_DIV_1, .PLLN = 40, .PLLR = LL_RCC_PLLR_DIV_2 };
LL_UTILS_ClkInitTypeDef clk = { LL_RCC_SYSCLK_DIV_1, LL_RCC_APB1_DIV_1, LL_RCC_APB2_DIV_1 };
LL_PLL_ConfigSystemClock_MSI(&pll, &clk);       /* or _HSI / _HSE variants */
```
These set flash latency, voltage scaling checks and update `SystemCoreClock`. CubeMX's LL
`SystemClock_Config` usually does the same steps explicitly with `LL_RCC_*` calls; either way.
`LL_SetFlashLatency(freq)` (newer packages) computes wait states for a target frequency.

## Device info
```c
uint32_t uid0 = LL_GetUID_Word0();
uint32_t flash_kb = LL_GetFlashSize();
uint32_t pkg = LL_GetPackageType();
```

## Limits
- No timeout-based helpers for peripherals: write your own using a millisecond counter (SysTick
  interrupt) for robust code instead of LL_mDelay loops.
- `LL_mDelay` blocks; never use it in ISRs.

## Verify
- [ ] Scope a GPIO toggled with `LL_mDelay(10)`: ~10-11 ms.
- [ ] `SystemCoreClock` matches the MCO-measured clock after setup.
