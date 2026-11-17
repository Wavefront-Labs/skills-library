---
id: computing-software.firmware-embedded-development.stm32.hal-msp-init-callbacks
name: hal-msp-init-callbacks
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-hal-comms, msp-init, hal-msp, peripheral-deinit, pin-and-clock-init, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Understand STM32 HAL MSP init/deinit callbacks: what goes in HAL_xxx_MspInit (clocks, GPIO, DMA, NVIC), multiple instances, and clean DeInit for low power and re-init."
sources:
  - https://www.st.com/resource/en/user_manual/um1884-description-of-stm32l4l4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
  - https://wiki.st.com/stm32mcu/wiki/Getting_started_with_UART
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MSP init callbacks

HAL splits peripheral setup: `HAL_UART_Init()` configures the peripheral registers, and it calls
the weak `HAL_UART_MspInit()` (MCU Support Package) for the board-specific part. CubeMX generates
MSP functions in `stm32xxxx_hal_msp.c`.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## What belongs in MspInit
1. Peripheral clock enable (`__HAL_RCC_USART2_CLK_ENABLE()`), kernel clock selection.
2. GPIO clocks and pin AF configuration.
3. DMA channel init and linking (`__HAL_LINKDMA(huart, hdmarx, hdma_usart2_rx)`).
4. NVIC priority and enable for the peripheral and its DMA IRQs.

## Multiple instances
One MspInit per peripheral type handles all instances:
```c
void HAL_UART_MspInit(UART_HandleTypeDef *h) {
    if (h->Instance == USART2) { /* ... */ }
    else if (h->Instance == USART3) { /* ... */ }
}
```

## DeInit for low power or re-init
`HAL_UART_DeInit()` calls `HAL_UART_MspDeInit()`: disable the clock, set pins back to analog,
de-init DMA and disable IRQs. Use this before Stop modes or when a peripheral is unused for long
periods; then `HAL_UART_Init()` again restores everything. Calling Init twice without DeInit is
fine for registers, but MspInit runs again: avoid allocation or side effects in it.

## Register callbacks alternative
With `USE_HAL_UART_REGISTER_CALLBACKS = 1`, `HAL_UART_RegisterCallback(h, HAL_UART_MSPINIT_CB_ID, fn)`
must be called **before** `HAL_UART_Init` (the handle's State must be RESET), otherwise the weak
default runs.

## The HAL state trap
`HAL_xxx_Init` only calls MspInit when `handle->State == HAL_xxx_STATE_RESET`. A handle that
isn't zeroed (e.g. stack-allocated) skips MspInit: no clock, nothing works. Use static/global
handles or memset to 0.

## Global MSP
`HAL_MspInit()` (called by `HAL_Init()`) is for system-wide setup: SYSCFG/PWR clocks, NVIC
priority grouping, pin remaps like UCPD dead-battery disable on G4/G0.

## Verify
- [ ] DeInit/Init cycle around Stop mode leaves the peripheral fully working.
- [ ] Current in Stop matches expectations after MspDeInit (pins analog).

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com, wiki.st.com); no readable alternative was found.

Method: documentation only; no commands were run.
