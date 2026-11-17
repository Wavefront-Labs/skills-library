---
id: computing-software.firmware-embedded-development.stm32.hal-callbacks-and-register-callbacks
name: hal-callbacks-and-register-callbacks
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-hal-uart, hal-callbacks, weak-callbacks, use-hal-uart-register-callbacks, hal-uart-rxcpltcallback, multiple-instances, callback-context, firmware-embedded-development]
level: practitioner
status: gated
description: "Handle STM32 HAL completion and error callbacks: weak default overrides, dispatching multiple peripheral instances, USE_HAL_*_REGISTER_CALLBACKS, and what is safe inside them."
sources:
  - https://www.st.com/resource/en/user_manual/um1725-description-of-stm32f4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HAL callbacks and register callbacks

**Goal:** clean event handling for interrupt/DMA-driven HAL operations, especially with several
instances of the same peripheral.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Weak callbacks (default model)
HAL defines callbacks as `__weak` functions; you override them by defining a function with the
same name:
```c
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    if (huart->Instance == USART1)      gps_rx_done();
    else if (huart->Instance == USART2) modem_rx_done();
}
void HAL_UART_ErrorCallback(UART_HandleTypeDef *huart) {
    uint32_t err = HAL_UART_GetError(huart);   /* ORE, FE, NE, PE, DMA */
    restart_rx(huart);
}
```
One function serves **all instances**: dispatch on `huart->Instance` (or compare handle pointers).
Forgetting the override = silent no-op; a typo in the name = silent no-op too (it's just a new
function). Keep callbacks in one file to avoid duplicate definitions at link time.

## Register callbacks (per-instance function pointers)
Enable in `stm32xxxx_hal_conf.h` (or CubeMX "Advanced Settings > Register Callback"):
```c
#define USE_HAL_UART_REGISTER_CALLBACKS 1
```
then:
```c
HAL_UART_RegisterCallback(&huart1, HAL_UART_RX_COMPLETE_CB_ID, gps_rx_cb);
HAL_UART_RegisterRxEventCallback(&huart2, modem_rx_event_cb);   /* ReceiveToIdle events */
```
Good for driver modules that own one instance without touching a global dispatcher. Register
**after** `HAL_UART_Init` for most IDs (Init resets callbacks to weak defaults) except MspInit/
MspDeInit, which must be registered before Init in the `HAL_UART_STATE_RESET` state.

## What's safe inside callbacks
They run in **interrupt context** (called from `HAL_xxx_IRQHandler`):
- Keep them short: set flags, give semaphores/notify tasks (FromISR APIs), restart the next
  transfer.
- No blocking HAL calls (`HAL_Delay`, polling `HAL_UART_Transmit` with timeout) and no RTOS
  blocking calls.
- Restarting reception from the callback (`HAL_UART_Receive_IT` again) is the standard pattern;
  check its return value: if it fails (HAL_BUSY), reception silently stops.

## Error callbacks are not optional
Overrun (ORE) on UART stops reception in HAL until handled. Always implement the error
callback: clear and restart. Same for I2C (AF, BERR, ARLO) and SPI (OVR).

## Verify
- [ ] Each instance's events reach the right handler (test both UARTs simultaneously).
- [ ] Forced overrun (pause the CPU with a breakpoint during RX, resume) recovers automatically.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
