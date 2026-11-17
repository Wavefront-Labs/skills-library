---
id: computing-software.firmware-embedded-development.zephyr.uart-async-api
name: uart-async-api
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [uart-async-api, uart-rx-enable, uart-callback-set, uart-rx-buf-request, dma-uart, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Receive and transmit with the Zephyr UART async (DMA) API: event-driven callbacks, double-buffered RX with inactivity timeout, buffer handoff, and error recovery."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/uart.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/drivers/serial/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UART async API

Three UART APIs exist: polling, interrupt-driven, and **async** (DMA-backed, event callbacks).
Async gives the lowest CPU use at high baud rates.

```
CONFIG_SERIAL=y
CONFIG_UART_ASYNC_API=y
# CONFIG_UART_ASYNC_API depends on SERIAL_SUPPORT_ASYNC, which the driver provides; check your driver's
# Kconfig and devicetree (for DMA-backed drivers, the DMA channels)
```

## RX with double buffering
```c
#define RX_BUF 64
static uint8_t rx_bufs[2][RX_BUF];
static uint8_t next_idx = 1;

static void uart_cb(const struct device *dev, struct uart_event *evt, void *ud)
{
    switch (evt->type) {
    case UART_RX_RDY:          /* data available: offset+len inside current buffer */
        ring_buf_put(&rx_rb, evt->data.rx.buf + evt->data.rx.offset, evt->data.rx.len);
        k_sem_give(&rx_sem);
        break;
    case UART_RX_BUF_REQUEST:  /* driver wants the next buffer */
        uart_rx_buf_rsp(dev, rx_bufs[next_idx], RX_BUF);
        next_idx ^= 1;
        break;
    case UART_RX_BUF_RELEASED: /* driver done with evt->data.rx_buf.buf */
        break;
    case UART_RX_DISABLED:     /* RX stopped (error or buffers exhausted): restart */
        uart_rx_enable(dev, rx_bufs[0], RX_BUF, 10000 /*us inactivity timeout*/);
        next_idx = 1;
        break;
    case UART_RX_STOPPED:      /* error: evt->data.rx_stop.reason = UART_ERROR_OVERRUN etc. */
        rx_errors++;
        break;
    case UART_TX_DONE:
    case UART_TX_ABORTED:
        k_sem_give(&tx_done);
        break;
    default: break;
    }
}

void uart_start(const struct device *uart)
{
    uart_callback_set(uart, uart_cb, NULL);
    uart_rx_enable(uart, rx_bufs[0], RX_BUF, 10000);
}
```
- The `uart_rx_enable()` timeout is in microseconds and counts from the last received byte: after that long
  without new bytes, received data is reported as `UART_RX_RDY`, so short messages arrive promptly. If no data
  was received there is no timeout event. `SYS_FOREVER_US` disables the timeout.
- `UART_RX_RDY` can fire several times per buffer; process `offset..offset+len` only. `UART_RX_BUF_RELEASED`
  immediately follows an `UART_RX_RDY` for a buffer the driver has finished with.
- Treat the callback as interrupt-context code (the header does not state the context): copy out quickly (ring buffer,
  msgq) and do not block.

## TX
```c
int rc = uart_tx(uart, buf, len, SYS_FOREVER_US /*timeout*/);
k_sem_take(&tx_done, K_FOREVER);   /* buf must stay valid until TX_DONE */
```
Only one TX in flight; `uart_tx()` returns `-EBUSY` otherwise. The TX timeout is in microseconds and is
valid only if flow control is enabled; on timeout the event is `UART_TX_ABORTED`. `uart_tx_abort()` also
generates `UART_TX_ABORTED`.

## Errors and recovery
- A `UART_RX_STOPPED` event (reasons include `UART_ERROR_OVERRUN`, `UART_ERROR_PARITY`, `UART_ERROR_FRAMING`,
  `UART_BREAK`) is followed by `UART_RX_RDY` if data was received, `UART_RX_BUF_RELEASED` for each buffer in use, and
  finally `UART_RX_DISABLED`; re-enable RX from the `DISABLED` case (as above).
- Not answering `UART_RX_BUF_REQUEST` with `uart_rx_buf_rsp()` before the current buffer fills stops reception
  (after `UART_RX_RDY`, then `UART_RX_DISABLED`).
- `uart_rx_disable()` for shutdown; wait for `UART_RX_DISABLED` (and the `UART_RX_BUF_RELEASED` events) before
  reusing buffers.

## Verify
- [ ] Bursts at max baud complete with no `UART_RX_STOPPED` overruns.
- [ ] Short messages arrive within the inactivity timeout.
- [ ] RX restarts automatically after a forced framing error (send a break).

## Checked

Checked 2026-10-26 against `include/zephyr/drivers/uart.h` and `drivers/serial/Kconfig` on Zephyr main: event types and the
documented reception/transmission sequence, `struct uart_event` data fields (`rx`, `rx_buf`, `rx_stop`), `UART_ERROR_*` and
`UART_BREAK` stop reasons, `uart_rx_enable()` timeout in microseconds and counted from the last byte, `SYS_FOREVER_US`, `uart_tx()`
timeout (valid only with flow control) and `-EBUSY`, `uart_rx_buf_rsp()` behaviour, and `CONFIG_UART_ASYNC_API` depending on
`SERIAL_SUPPORT_ASYNC`. Removed the claims that older releases used milliseconds, that the callback runs in ISR context, and that
buffers may need to be DMA-reachable, none of which the header states, and the SoC-specific Kconfig and devicetree examples.

Method: documentation only; no commands were run.
