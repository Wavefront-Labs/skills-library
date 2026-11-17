---
id: computing-software.firmware-embedded-development.esp-idf.uart-driver-and-event-queue
name: uart-driver-and-event-queue
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-peripherals, esp-uart, uart-event-queue, uart-pattern-detect, rs485-half-duplex, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Drive ESP-IDF UARTs with the uart driver: install with an event queue, handle FIFO overflow, pattern detection for line protocols, RS485 half-duplex and pin routing."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/uart.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_uart/include/driver/uart.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UART driver and event queue

## Install
```c
const uart_port_t U = UART_NUM_1;
uart_config_t c = { .baud_rate = 115200, .data_bits = UART_DATA_8_BITS, .parity = UART_PARITY_DISABLE,
                    .stop_bits = UART_STOP_BITS_1, .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
                    .source_clk = UART_SCLK_DEFAULT };
QueueHandle_t q;
ESP_ERROR_CHECK(uart_driver_install(U, 2048 /*rx*/, 0 /*tx: 0 = blocking writes*/, 20, &q, 0));
ESP_ERROR_CHECK(uart_param_config(U, &c));
ESP_ERROR_CHECK(uart_set_pin(U, GPIO_NUM_17, GPIO_NUM_16, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));
```
Pins are chosen with `uart_set_pin`; on many dev boards the USB-UART bridge uses the UART0 default pins.

## Event task
```c
for (;;) {
    uart_event_t e;
    if (!xQueueReceive(q, &e, portMAX_DELAY)) continue;
    switch (e.type) {
    case UART_DATA:        uart_read_bytes(U, buf, e.size, 0); handle(buf, e.size); break;
    case UART_FIFO_OVF:
    case UART_BUFFER_FULL: uart_flush_input(U); xQueueReset(q); break;   /* data lost: resync protocol */
    case UART_PATTERN_DET: {
        int pos = uart_pattern_pop_pos(U);
        int n = uart_read_bytes(U, line, pos + 1, pdMS_TO_TICKS(10));   /* includes '\n' */
        handle_line(line, n); break; }
    case UART_BREAK: case UART_FRAME_ERR: case UART_PARITY_ERR: count_errors(e.type); break;
    default: break;
    }
}
```
Pattern detection for NMEA/AT lines:
```c
uart_enable_pattern_det_baud_intr(U, '\n', 1, 9, 0, 0);
uart_pattern_queue_reset(U, 20);
```

## Timing knobs
- RX timeout (`uart_set_rx_timeout(U, 3)`, in symbol periods, maximum 126) controls how soon UART_DATA fires
  after a pause; RX full threshold (`uart_set_rx_full_threshold`) for bulk streams.
- At high baud rates consider hardware flow control (RTS/CTS); `uart_set_rx_full_threshold` also helps the FIFO drain in time.

## RS485
```c
uart_set_pin(U, TX, RX, DE_PIN /* RTS drives DE */, UART_PIN_NO_CHANGE);
uart_set_mode(U, UART_MODE_RS485_HALF_DUPLEX);
```
The driver toggles RTS around transmission; check turnaround timing on a scope.

## Pitfalls
- `uart_write_bytes` with tx buffer 0 blocks until data is in the FIFO; use a TX buffer for async.
- The console may use the same UART (UART0 by default on many boards); move or disable the console in menuconfig if
  you reuse that port.
- Strapping pins used as RX/TX can break boot; check your chip's datasheet.

## Verify
- [ ] Sustained max-rate traffic for 10 min with zero FIFO_OVF events.
- [ ] Error counters exposed (frame/parity) for field diagnostics.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in peripherals/uart.rst and uart.h: uart_driver_install signature and tx_buffer_size 0 behaviour (writes block until sent), event types (UART_DATA, UART_FIFO_OVF, UART_BUFFER_FULL, UART_PATTERN_DET, UART_BREAK), uart_enable_pattern_det_baud_intr and uart_pattern_pop_pos / uart_pattern_queue_reset, uart_set_rx_timeout in symbol periods (max 126), uart_set_rx_full_threshold, RS485 half-duplex mode via uart_set_mode. Removed unconfirmed claims: any-GPIO matrix statement, 1 Mbit flow-control threshold, strapping pin list, console Kconfig option name.

Method: documentation only; no commands were run.
