---
id: computing-software.firmware-embedded-development.esp-idf.dual-core-task-pinning-and-watchdog
name: dual-core-task-pinning-and-watchdog
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-idf, esp32, dual-core, core-affinity, xtaskcreatepinnedtocore, protocore, appcore, task-watchdog, esp-task-wdt, int-wdt, cache-disabled-while-flash-op, spinlock, portmux, cross-core-interrupt, wifi-stack-core0, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use ESP32's dual Xtensa cores correctly: core affinity with xTaskCreatePinnedToCore, the interrupt/task watchdog panic dump, and the flash-operation-disables-cache trap that stalls the other core."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/freertos_idf.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/wdts.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/spi_flash/spi_flash_concurrency.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESP32 dual-core task pinning and watchdogs

**Goal:** place tasks correctly across ESP32's two Xtensa cores and read its
watchdog panic output, extending the general FreeRTOS priority/stack guidance
in `computing-software.firmware-embedded-development.freertos.task-and-queue-design`
with ESP32-specific SMP behavior that single-core Cortex-M FreeRTOS doesn't have.

## Core affinity basics
`xTaskCreatePinnedToCore(fn, name, stack, arg, priority, &handle, core_id)`
where `core_id` is `0`, `1`, or `tskNO_AFFINITY` (scheduler picks either core per
run, task can migrate between calls). In typical ESP-IDF applications the tasks handling protocol processing such as Wi-Fi or Bluetooth are pinned to core 0 (`PRO_CPU`) and the rest of the application to core 1 (`APP_CPU`); the aliases reflect that usage and are a convention, not a hardware requirement. Chips with a single core have no second core to pin to, so check your chip.

## Shared-resource locking across cores
Unlike single-core FreeRTOS where disabling interrupts is enough to make a
section atomic, two cores can execute simultaneously — a critical section
needs a **spinlock** (`portMUX_TYPE`, `portENTER_CRITICAL`/`portEXIT_CRITICAL`)
that actually contends across cores, not just local interrupt masking. Code
ported from a single-core FreeRTOS project that only disabled interrupts for
"atomicity" is not actually safe on ESP32's dual core without auditing for this.

## Task watchdog vs interrupt watchdog
- **Task Watchdog Timer (`esp_task_wdt`)**: each subscribed task must call
  `esp_task_wdt_reset()` periodically; a panic dump on timeout names the
  specific task and core that failed to check in — far more diagnosable than a
  generic reset. By default the TWDT watches the idle task of each CPU
  (`CONFIG_ESP_TASK_WDT_CHECK_IDLE_TASK_CPU0` and related options), so a CPU-bound task starving the idle task on its core triggers it even if
  your own task "isn't hung", just monopolizing the CPU.
- **Interrupt Watchdog (`CONFIG_ESP_INT_WDT`, enabled by default; timeout `CONFIG_ESP_INT_WDT_TIMEOUT_MS`)**: catches a core stuck with
  interrupts disabled for too long (deadlock, infinite loop in a critical
  section) and reports "Interrupt wdt timeout on CPU0" or "CPU1" through the panic handler. A different failure class from a task simply not yielding.
Reading the serial panic output's "CPU halted" / backtrace per core after
either fire is the first diagnostic step; map the PC with `addr2line` per
`computing-software.firmware-embedded-development.hardware-debugging.cortex-m-hardfault-analysis`'s
method (ESP32 uses Xtensa, not Cortex-M, so the exception frame layout differs,
but the addr2line workflow is the same idea).

## The flash-operation-stalls-the-other-core trap
While SPI1 flash operations (erase, write, such as an NVS commit or OTA write) run, the caches are disabled, other tasks are suspended and the other core polls in a busy loop; only IRAM-safe interrupt handlers (registered with `ESP_INTR_FLAG_IRAM`) keep running. Time-critical code on the other core therefore stalls for the duration of the flash operation. This
shows up as latency spikes or watchdog trips correlated with NVS
writes/OTA, not necessarily as a crash, so correlate watchdog timestamps with flash-write
call sites before assuming a scheduling bug. Handlers that cannot tolerate the stall must be IRAM-safe (`IRAM_ATTR`, with their data in DRAM); see the flash cache-error skill.

## Verify
- [ ] Task-to-core placement matches measured contention (not just copied convention); CPU-heavy work isn't fighting Wi-Fi-stack tasks on core 0.
- [ ] Shared mutable state touched from tasks on both cores uses `portENTER_CRITICAL`/a mutex, not interrupt-disable alone.
- [ ] A deliberately CPU-starved task reproduces a task watchdog panic naming the correct task/core, confirming the watchdog is actually wired up.
- [ ] Timing-sensitive ISRs are marked `IRAM_ATTR` and tested for correctness during a concurrent flash write (NVS commit or OTA) on the other core.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the IDF FreeRTOS, watchdog and SPI flash concurrency pages: xTaskCreatePinnedToCore with core 0, 1 or tskNO_AFFINITY, PRO_CPU/APP_CPU convention, disabling interrupts and scheduler suspension are not valid mutual exclusion in SMP (spinlocks are), TWDT watches idle tasks by default and esp_task_wdt_reset, IWDT default-on with CONFIG_ESP_INT_WDT and its panic message, cache disabled during flash operations with the other core busy-polling. Removed unconfirmed stall duration and per-chip core-count claims. Cross-references to other library skills were not changed.
Method: documentation only; no commands were run.
