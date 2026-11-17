---
id: computing-software.firmware-embedded-development.stm32.exti-line-configuration
name: exti-line-configuration
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-gpio, exti, syscfg-exticr, external-interrupt, exti-line-sharing, exti9-5, exti15-10, rising-falling-trigger, pending-register, firmware-embedded-development]
level: practitioner
status: gated
description: "Configure STM32 EXTI external interrupts: SYSCFG port selection, line sharing (one port per line), grouped IRQ handlers, pending-bit clearing and edge selection."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0440-stm32g4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EXTI line configuration

**Goal:** GPIO interrupts that fire once per edge, on the pins you meant, with handlers that
can tell which line fired.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## The constraint that shapes pinouts
EXTI line N serves **pin N of exactly one port** (`SYSCFG->EXTICR` selects A, B, C...).
PA3 and PB3 cannot both have interrupts. Assign interrupt inputs to distinct pin numbers when
planning the schematic.

## IRQ grouping (F4/F1/L4 style)
| Lines | IRQ handler |
|---|---|
| 0..4 | `EXTI0_IRQHandler` .. `EXTI4_IRQHandler` (one each) |
| 5..9 | `EXTI9_5_IRQHandler` (shared) |
| 10..15 | `EXTI15_10_IRQHandler` (shared) |
Put latency-critical inputs on lines 0-4 to get a dedicated vector. G0/C0/U5/H5 families have
separate rising/falling pending registers (`RPR1`/`FPR1`) and different handler grouping
(e.g. `EXTI0_1_IRQHandler` on G0): check the vector table of your part.

## Register setup (F4)
```c
RCC->APB2ENR |= RCC_APB2ENR_SYSCFGEN;                  /* forgetting this = EXTICR ignored */
SYSCFG->EXTICR[13/4] = (SYSCFG->EXTICR[13/4] & ~(0xFu << ((13%4)*4))) | (2u << ((13%4)*4)); /* PC13 */
EXTI->FTSR |= (1u << 13);      /* falling edge */
EXTI->RTSR &= ~(1u << 13);
EXTI->PR    = (1u << 13);      /* clear stale pending (write 1) */
EXTI->IMR  |= (1u << 13);
NVIC_SetPriority(EXTI15_10_IRQn, 6);
NVIC_EnableIRQ(EXTI15_10_IRQn);

void EXTI15_10_IRQHandler(void) {
    uint32_t pr = EXTI->PR & EXTI->IMR & 0xFC00u;
    EXTI->PR = pr;                  /* clear first, write-1-to-clear, no RMW */
    if (pr & (1u << 13)) button_isr();
}
```
HAL equivalent: `GPIO_MODE_IT_FALLING` in `HAL_GPIO_Init`, handler calls
`HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_13)`, user code in `HAL_GPIO_EXTI_Callback(pin)`.

## Gotchas
- **Clearing PR with `|=`** clears every pending line (read-modify-write of a w1c register).
  Write only the bit(s) you handle.
- **Clear late = double interrupt**: clearing PR as the last instruction can re-enter the
  handler because the write hasn't propagated before exception return; clear early or add
  `__DSB()`.
- Bouncing switches create bursts of interrupts; debounce with a timer, not a delay in the ISR.
- Event mode (`EMR`) wakes from WFE without an ISR; useful for low power, but nothing runs.

## Verify
- [ ] One press = one callback (count with a counter while pressing 100 times with hardware
      debounce or a clean signal generator edge).
- [ ] Other lines sharing the handler still fire independently.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
