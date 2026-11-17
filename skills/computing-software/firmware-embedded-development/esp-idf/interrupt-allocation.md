---
id: computing-software.firmware-embedded-development.esp-idf.interrupt-allocation
name: interrupt-allocation
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-dual-core, esp-intr-alloc, interrupt-priority-levels, shared-interrupts, esp-intr-dump, core-affinity, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Allocate ESP32 interrupts with esp_intr_alloc: priority levels, IRAM and shared flags, which core gets the interrupt, running out of interrupt lines, and inspecting allocation."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/intr_alloc.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/hlinterrupts.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_hw_support/include/esp_intr_alloc.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interrupt allocation

Peripherals raise interrupt **sources**; the interrupt matrix routes each source to a CPU
interrupt line on one core. `esp_intr_alloc` picks a free line with the properties you ask
for. Drivers call it internally; you call it for peripherals you drive directly.

## API
```c
#include "esp_intr_alloc.h"
static intr_handle_t h;
ESP_ERROR_CHECK(esp_intr_alloc(ETS_TG0_T0_LEVEL_INTR_SOURCE,
                               ESP_INTR_FLAG_LEVEL3 | ESP_INTR_FLAG_IRAM,
                               my_isr, NULL, &h));
esp_intr_disable(h);  esp_intr_enable(h);  esp_intr_free(h);
```
Many drivers expose the flags through their config (an `intr_alloc_flags` argument or a
priority field).

## Flags
| Flag | Meaning |
|---|---|
| `ESP_INTR_FLAG_LEVEL1..3` / `LOWMED` | C-callable priority levels (higher preempts lower) |
| `ESP_INTR_FLAG_LEVEL4..6`, `NMI` | `ESP_INTR_FLAG_HIGH`: need to be handled in assembly (Xtensa) |
| `ESP_INTR_FLAG_IRAM` | handler runs while flash cache is disabled; must be IRAM-safe |
| `ESP_INTR_FLAG_SHARED` | share a line with other sources (level-triggered only) |
| `ESP_INTR_FLAG_EDGE` | edge-triggered line |
| `ESP_INTR_FLAG_INTRDISABLED` | allocate disabled, enable later |

## Core affinity: the important rule
For external peripheral sources the interrupt is allocated on the core that executes
`esp_intr_alloc` (on multi-core Xtensa targets), and driver install functions call it, so
install drivers from a task pinned to the core you want; unpinned tasks may migrate, which
makes the handle hard to free. Example for the UART driver:
```c
static void init_on_core1(void *arg) { uart_driver_install(...); vTaskDelete(NULL); }
xTaskCreatePinnedToCore(init_on_core1, "init1", 4096, NULL, 5, NULL, 1);
```
Use this to keep heavy ISRs away from latency-critical ones.

## Running out
Each CPU has a limited number of interrupt lines. With many peripherals a driver can return
`ESP_ERR_NOT_FOUND`. Fixes from the guide: share interrupts with `ESP_INTR_FLAG_SHARED`, spread
drivers across cores, and request levels 2 or 3 where drivers default to `ESP_INTR_FLAG_LEVEL1`
(use `esp_intr_dump` to see free levels).

## Inspect
```c
esp_intr_dump(stdout);    /* per CPU: interrupt number, level, type, status */
```
`esp_intr_get_cpu(h)` and `esp_intr_get_intno(h)` for one handle.

## Latency notes
- Critical sections disable interrupts, so latency-critical work may need high-level (assembly)
  interrupts or hardware peripherals (RMT, MCPWM, DMA).
- Keep ISRs short and defer work to tasks.

## Verify
- [ ] `esp_intr_dump` output reviewed: critical ISRs on the intended core and level.
- [ ] No `ESP_ERR_NOT_FOUND` with all features enabled on the target chip.
- [ ] Latency-critical ISR measured with a GPIO toggle under Wi-Fi load.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed in esp_intr_alloc.h and the interrupt allocation guide: flag names and meanings (LEVEL1-6, NMI, LOWMED, HIGH, SHARED, EDGE, IRAM, INTRDISABLED), shared interrupts are level-triggered only, esp_intr_dump, esp_intr_get_cpu/get_intno, ESP_ERR_NOT_FOUND advice, allocation core and pinned-task advice. Removed unconfirmed claims: 32 lines on ESP32, Wi-Fi on core 0 by default, critical-section masking up to level 3, "no FreeRTOS calls" wording and `.intr_priority` field name.
Method: documentation only; no commands were run.
