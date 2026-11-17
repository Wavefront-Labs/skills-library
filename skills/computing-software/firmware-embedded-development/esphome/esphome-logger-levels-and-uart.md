---
id: computing-software.firmware-embedded-development.esphome.esphome-logger-levels-and-uart
name: esphome-logger-levels-and-uart
category: computing-software
field: firmware-embedded-development
product: esphome
tags: [esphome, logger, log-level, baud-rate, tag-levels, hardware-uart, tx-buffer-size, on-message, deassert-rts-dtr]
level: practitioner
status: docs-checked
description: "Set up the ESPHome logger: global and per-tag log levels, baud rate, buffers, hardware UART selection, on_message trigger and serial reset behaviour."
sources: ["https://esphome.io/components/logger/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Esphome logger levels and uart

The logger sends messages over the serial port and, when an MQTT client exists, over MQTT topics. The default level is `DEBUG`; raising it to `INFO` or `WARN` helps performance and memory size.

Options:
- `baud_rate` (default 115200; `0` disables UART logging, which is the usual way to free the UART for another component).
- `level`: global minimum severity shown; `initial_level` defaults to `level` and can vary at run time.
- `logs`: mapping that sets the log level for a specific component or tag. `runtime_tag_levels` is enabled automatically when `logs` is used or when `logger.set_level` is called with a `tag`.
- `tx_buffer_size` (default 512): decrease if you have memory problems.
- `task_log_buffer_size` (ESP32, LibreTiny, nRF52 only; default 768B; `0` disables) a thread-safe ring buffer that prevents API disconnections when several threads log together.
- `hardware_uart`: which hardware UART logs; default depends on chip and framework. The ESP32 has three usable UARTs, the ESP8266 two, one of which is transmit-only.
- `on_message`: runs when a message is logged, with `int level`, `const char* tag` and `const char* message` available in lambdas.
- `deassert_rts_dtr`: drives DTR and RTS false after opening the serial connection, resetting the chip into application mode so you capture all boot messages. Default false.
- nRF52 only: `wait_for_cdc` (waits up to 10 seconds for the CDC port) and `early_message` (boot reason).
- `esp8266_store_log_strings_in_flash` is deprecated, ignored and will be rejected from 2027.4.0; remove it.

## Checked

2026-11-04. Prose, option names, defaults and ranges were compared with https://esphome.io/components/logger/ (fetched this batch). Removed the unsourced purpose claim for `logs`.

Method: documentation only; no commands were run.
