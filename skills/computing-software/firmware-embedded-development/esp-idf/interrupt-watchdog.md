---
id: computing-software.firmware-embedded-development.esp-idf.interrupt-watchdog
name: interrupt-watchdog
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-system, interrupt-watchdog, int-wdt, isr-latency, critical-section-length, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Understand and fix ESP-IDF interrupt watchdog timeouts: what the IWDT detects, timeout config, long critical sections and ISRs, and reading the panic output."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/wdts.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_system/Kconfig
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/fatal-errors.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interrupt watchdog

The interrupt watchdog (IWDT) panics when a CPU core can't run the FreeRTOS tick
interrupt (which feeds the watchdog) within `CONFIG_ESP_INT_WDT_TIMEOUT_MS` (default 300 ms, or
800 ms when PSRAM support is enabled). It catches
interrupts disabled too long and ISRs that never return. The task watchdog (TWDT) is a
separate mechanism for tasks that don't yield.

## Panic signature
```
Guru Meditation Error: Core  0 panic'ed (Interrupt wdt timeout on CPU0).
```
The backtrace shows where the core was stuck. Typical lines: inside a `portENTER_CRITICAL`
section, a busy-wait in an ISR, or a spinlock waiting on the other core.

## Common causes
- Long work inside `portENTER_CRITICAL(&mux)`: flash erase, printf, loops over large buffers.
  Critical sections should last microseconds.
- ISR that loops waiting for hardware, or calls blocking APIs.
- Deadlock on a spinlock (both cores in critical sections waiting for each other).

## Config
```
CONFIG_ESP_INT_WDT=y
CONFIG_ESP_INT_WDT_TIMEOUT_MS=300       # default is 800 with PSRAM
CONFIG_ESP_INT_WDT_CHECK_CPU1=y
```
Raising the timeout hides bugs; the guide suggests it only when the code cannot be changed to
shorten critical sections or interrupts. The timeout must exceed twice the FreeRTOS tick period.

## Fix patterns
- Move work out of ISRs: ISR copies data and notifies a task (`xTaskNotifyFromISR`).
- Replace critical sections guarding long operations with a mutex.
- For bit-banged protocols that need interrupts off, keep each critical window short (one byte,
  not the whole frame) or use RMT/SPI hardware instead.

## Verify
- [ ] Panic backtrace decoded to the exact function (idf.py monitor with ELF).
- [ ] Longest critical section measured (`esp_cpu_get_cycle_count` around it) and well below the timeout.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed in the watchdog page and esp_system/Kconfig: IWDT uses the FreeRTOS tick interrupt on each CPU, panic text "Interrupt wdt timeout on CPU0/1", CONFIG_ESP_INT_WDT, CONFIG_ESP_INT_WDT_TIMEOUT_MS and CONFIG_ESP_INT_WDT_CHECK_CPU1, critical-section and ISR causes, remedies. Wrong: the default timeout is 300 ms only without PSRAM (800 ms with SPIRAM). Removed unconfirmed claims about esp_rom_delay_us and IRAM-flag cache errors.
Method: documentation only; no commands were run.
