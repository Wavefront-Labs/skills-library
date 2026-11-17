---
id: computing-software.firmware-embedded-development.stm32.mixing-hal-and-ll
name: mixing-hal-and-ll
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-ll, hal-ll-mixing, hal-handle-state, custom-irq-handler, ll-fast-path, stm32cubemx, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Combine STM32 HAL and LL in one project safely: HAL for setup, LL for hot paths and ISRs, per-peripheral driver choice in CubeMX, and keeping HAL handle state consistent."
sources:
  - https://www.st.com/resource/en/user_manual/um1884-description-of-stm32l4l4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-for-stm32-configuration-and-initialization-c-code-generation-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mixing HAL and LL

HAL and LL are designed to coexist. HAL itself uses LL headers internally on many series. The
risk is two drivers disagreeing about one peripheral's state.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Per-peripheral choice in CubeMX
*Project Manager > Advanced Settings > Driver Selector*: choose HAL or LL per peripheral (RCC,
GPIO, USART, TIM, ...). Generated init code then uses that driver. A common split:
- LL: GPIO, simple timers, a high-rate UART or SPI.
- HAL: USB, SDMMC, Ethernet, anything with a middleware stack expecting HAL handles.

## Pattern 1: HAL init, LL fast path
HAL configures the UART (clocks, pins via MSP, NVIC), then your ISR uses LL for minimal latency:
```c
/* stm32l4xx_it.c: replace the generated HAL_UART_IRQHandler(&huart2) call */
void USART2_IRQHandler(void)
{
    if (LL_USART_IsActiveFlag_RXNE(USART2)) {
        uint8_t b = LL_USART_ReceiveData8(USART2);     /* reading RDR clears RXNE */
        ring_put(&rx_ring, b);
    }
    if (LL_USART_IsActiveFlag_ORE(USART2)) LL_USART_ClearFlag_ORE(USART2);
}
/* after MX_USART2_UART_Init(): */
LL_USART_EnableIT_RXNE(USART2);
```
Rules for this pattern:
- Once LL owns the data path, **don't** call HAL transfer APIs (`HAL_UART_Receive_IT`) on that
  peripheral: the HAL handle state (`huart2.RxState`) no longer reflects reality and HAL calls
  return `HAL_BUSY` or corrupt the transfer.
- Keep the generated `HAL_UART_IRQHandler` out of the IRQ (CubeMX: NVIC settings > uncheck
  "Call HAL handler" for that IRQ, so regeneration doesn't put it back).
- Error recovery can still use HAL (`HAL_UART_DeInit`/`Init`) when the LL path is quiescent.

## Pattern 2: LL everywhere, HAL for one middleware
Use LL for clocks and most peripherals but HAL for USB device. HAL then needs `HAL_Init()`
and its tick (`HAL_GetTick`) for timeouts. Provide it from SysTick or a TIM (CubeMX *SYS >
Timebase Source*), and don't also call `LL_Init1msTick`, which reprograms SysTick without
the interrupt the HAL tick needs.

## Pattern 3: LL inside HAL callbacks
In a HAL callback (e.g. `HAL_TIM_PeriodElapsedCallback`), LL inline calls like
`LL_GPIO_TogglePin` cost one store instead of HAL's argument checking and locking. Safe because
they touch a different peripheral than the one whose handle is active.

## Clock config
RCC configured by HAL (`HAL_RCC_ClockConfig`) updates `SystemCoreClock`; LL code computing baud
rates reads clocks with `LL_RCC_GetXXXClockFreq()`, which reads registers, so both stay
consistent as long as nobody changes clocks behind the other's back.

## Verify
- [ ] No peripheral is driven by HAL transfer APIs and LL data-path code at the same time (review per peripheral).
- [ ] Regenerating with CubeMX keeps custom IRQ handlers (HAL handler call disabled in NVIC settings).
- [ ] HAL timeouts still work (HAL tick running) in LL-heavy builds.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
