---
id: computing-software.firmware-embedded-development.stm32.hal-error-and-timeout-handling
name: hal-error-and-timeout-handling
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-hal-uart, hal-timeout-handling, hal-statustypedef, hal-busy, hal-lock, error-handler, peripheral-recovery, hal-max-delay, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Handle STM32 HAL return codes and timeouts: HAL_OK/ERROR/BUSY/TIMEOUT meanings, avoiding HAL_MAX_DELAY, stuck __HAL_LOCK states, and recovering peripherals instead of loops."
sources:
  - https://www.st.com/resource/en/user_manual/um1725-description-of-stm32f4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HAL error and timeout handling

**Goal:** firmware that survives bus glitches, unplugged sensors and noisy lines, instead of
hanging in `HAL_MAX_DELAY` waits or `Error_Handler()`'s infinite loop.

## Return codes
| Code | Meaning | Typical action |
|---|---|---|
| `HAL_OK` | done | continue |
| `HAL_ERROR` | peripheral/protocol error (NACK, framing, parity, overrun) | read `HAL_xxx_GetError()`, recover, retry with limit |
| `HAL_BUSY` | handle locked or a transfer already running | wrong state machine use, or a previous transfer never finished |
| `HAL_TIMEOUT` | flag didn't arrive in time | device absent/hung, bus stuck: recover |
Ignoring return values is the root of most "it hangs sometimes" HAL bugs.

## Timeouts
- **Never `HAL_MAX_DELAY` in production paths**: a disconnected I2C device or a UART that never
  receives blocks the caller forever (and with it the watchdog-feeding loop, so you get resets
  you can't explain). Compute a timeout from the transfer size and speed plus margin.
- Timeouts rely on `HAL_GetTick()`: if SysTick (or the HAL timebase timer) has a lower priority
  than the ISR calling a blocking HAL function, the tick never advances and the timeout never
  expires. Don't call blocking HAL functions from ISRs.

## Stuck states
HAL handles keep `State` and `Lock` fields. After an error mid-DMA or a missing callback, a
handle can stay `HAL_UART_STATE_BUSY_RX` and every further call returns `HAL_BUSY`.
Recovery:
```c
HAL_UART_Abort(&huart2);          /* stops DMA/IT, resets state */
/* or for I2C bus lock-ups: */
HAL_I2C_DeInit(&hi2c1); i2c_bus_clear_gpio(); HAL_I2C_Init(&hi2c1);
```
Don't poke `huart->gState = HAL_UART_STATE_READY` by hand except as a last resort; you skip
cleanup of DMA and interrupts.

## Error_Handler
CubeMX-generated `Error_Handler()` disables interrupts and spins forever: fine during bring-up,
terrible in the field. Replace with: log the error and caller (`__builtin_return_address(0)`),
attempt peripheral recovery where it makes sense, otherwise controlled reset with a recorded
reason.

## Pattern
```c
static int sensor_read(uint8_t reg, uint8_t *v) {
    for (int attempt = 0; attempt < 3; attempt++) {
        if (HAL_I2C_Mem_Read(&hi2c1, ADDR, reg, 1, v, 1, 5) == HAL_OK) return 0;
        if (hi2c1.ErrorCode & (HAL_I2C_ERROR_BERR | HAL_I2C_ERROR_TIMEOUT)) i2c_recover();
    }
    return -EIO;
}
```

## Verify
- [ ] `grep -rn HAL_MAX_DELAY Core/ App/` only finds justified uses.
- [ ] Unplugging each external device at run time produces logged errors, no hang, and recovery
      on reconnect.

## Checked

2026-10-31: Confirmed `HAL_OK`/`HAL_ERROR`/`HAL_BUSY`/`HAL_TIMEOUT` and `HAL_MAX_DELAY` (stm32l4xx_hal_def.h), `HAL_GetTick`/`HAL_InitTick` (stm32l4xx_hal.c), the `HAL_UART_STATE_READY`/`BUSY_RX` names (stm32l4xx_hal_uart.h) and the per-peripheral error accessors such as `HAL_I2C_GetError` (stm32l4xx_hal_i2c.h).

Method: documentation only; no commands were run.
