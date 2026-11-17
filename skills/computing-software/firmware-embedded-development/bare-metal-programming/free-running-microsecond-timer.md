---
id: computing-software.firmware-embedded-development.bare-metal-programming.free-running-microsecond-timer
name: free-running-microsecond-timer
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [free-running-timer, systick-timebase, microsecond-clock, timer-prescaler-setup, timestamp, firmware-embedded-development]
level: practitioner
status: draft
description: "Configure a general-purpose timer as a free-running 1 MHz counter for timestamps, timeouts and delays, independent of SysTick and the RTOS tick."
sources:
  - https://www.st.com/resource/en/application_note/an4776-generalpurpose-timer-cookbook-for-stm32-microcontrollers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hardware timer as free-running microsecond clock

SysTick is usually owned by the RTOS or HAL and interrupts every millisecond. A dedicated
32-bit timer counting at 1 MHz, with no interrupt at all, gives microsecond timestamps,
busy-wait delays and timeouts that keep working with interrupts disabled.

## STM32 example (TIM2, 32-bit)
```c
void us_timer_init(void) {
    RCC->APB1ENR1 |= RCC_APB1ENR1_TIM2EN;
    (void)RCC->APB1ENR1;                         /* wait for clock enable to take effect */
    TIM2->PSC = (timer_clock_hz() / 1000000u) - 1u;
    TIM2->ARR = 0xFFFFFFFFu;                     /* full 32-bit range */
    TIM2->EGR = TIM_EGR_UG;                      /* load PSC now (it is preloaded) */
    TIM2->SR  = 0;                               /* UG sets UIF: clear it */
    TIM2->CR1 = TIM_CR1_CEN;
}
static inline uint32_t micros(void) { return TIM2->CNT; }

void delay_us(uint32_t us) { uint32_t t0 = micros(); while ((uint32_t)(micros() - t0) < us) {} }
```

## Timer clock gotcha
The timer clock is **not** PCLK when the APB prescaler is not 1: on most STM32 families it is
`2 x PCLK`. With SYSCLK 80 MHz, APB1 prescaler 2, PCLK1 = 40 MHz but TIM2 runs at 80 MHz. Compute
`timer_clock_hz()` from RCC registers or `HAL_RCC_GetPCLK1Freq() * (APB1 prescaler > 1 ? 2 : 1)`
(H7 and some G4 settings use `TIMPRE` for x4). A wrong assumption makes every timestamp off by 2x.

## Without a 32-bit timer
- 16-bit timer + overflow count (see 64-bit timestamp extension).
- DWT CYCCNT on M3/M4/M7/M33: core-clock resolution, stops in sleep, not on M0/M0+.
- Low-power timer (LPTIM) on LSE for timestamps that survive Stop mode, at 30.5 us resolution.

## Freeze in debug
Halting at a breakpoint leaves timers running, so timeouts expire while you step. Set
`DBGMCU->APB1FZR1 |= DBGMCU_APB1FZR1_DBG_TIM2_STOP` (name varies by family) in debug builds.

## Verify
- [ ] Toggle a GPIO around `delay_us(1000)`: scope shows 1.000 ms (+ a few cycles).
- [ ] `micros()` difference across `HAL_Delay(100)` reads ~100000.
- [ ] Changing the APB prescaler in CubeMX does not change the measured delay.
