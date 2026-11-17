---
id: computing-software.firmware-embedded-development.esp-idf.idf-freertos-smp-differences
name: idf-freertos-smp-differences
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-dual-core, idf-freertos-smp, freertos-smp, task-affinity, critical-section-spinlock, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write correct FreeRTOS code for ESP-IDF's SMP port: core affinity, spinlock critical sections, per-core idle/tick hooks, scheduler suspension semantics and Amazon SMP option."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/freertos_idf.html
  - https://github.com/espressif/esp-idf/blob/v6.1/components/freertos/Kconfig
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_system/include/esp_freertos_hooks.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IDF FreeRTOS SMP differences

ESP-IDF's FreeRTOS is a modified dual-core (SMP) kernel. Code written for single-core vanilla
FreeRTOS often assumes things that are false here.

## Key differences
| Topic | Vanilla | IDF SMP |
|---|---|---|
| Task creation | `xTaskCreate` | plus `xTaskCreatePinnedToCore(..., core)`; `tskNO_AFFINITY` floats |
| Critical sections | `taskENTER_CRITICAL()` disables interrupts | `taskENTER_CRITICAL(&spinlock)` takes a `portMUX_TYPE` spinlock as well as disabling interrupts on the calling core; the other core keeps running code that does not take that spinlock |
| Scheduler suspend | stops all switching | `vTaskSuspendAll` only affects the calling core |
| Idle/tick hooks | one | per core (`esp_register_freertos_idle_hook_for_cpu`) |
| Highest-priority task running | the scheduler always runs the highest-priority ready task | each core schedules independently, so two tasks of different priorities run at the same time, and core affinity can leave the second-highest-priority task not running |
| Time slicing | round robin | best-effort round robin (perfect round robin only if all tasks of a priority are pinned to the same core) |

## Consequences
- "Higher priority means exclusive access" is false: a priority 10 task on core 0 and a
  priority 5 task on core 1 run at the same time. Protect shared data with mutexes or spinlocks.
- `vTaskSuspendAll()` does not protect data from the other core.
- Interrupt-disable tricks (`portDISABLE_INTERRUPTS`) only affect the current core.

## Spinlocks
```c
static portMUX_TYPE mux = portMUX_INITIALIZER_UNLOCKED;
taskENTER_CRITICAL(&mux);   /* in ISRs: taskENTER_CRITICAL_ISR(&mux) */
counter++;
taskEXIT_CRITICAL(&mux);
```
Keep it short: the longer a critical section lasts, the longer pending interrupts are delayed, and
FreeRTOS APIs must not be called inside one. Critical sections can nest, but nesting different
spinlocks can deadlock. Atomics (`stdatomic.h`) work for simple counters.

## Affinity choices
- The Wi-Fi task is pinned to core 0 by default (`CONFIG_ESP_WIFI_TASK_CORE_ID`, choice `ESP_WIFI_TASK_PINNED_TO_CORE_0`);
  consider putting latency-critical app tasks on core 1.
- On chips with an FPU, IDF FreeRTOS saves FPU registers lazily per core, so a task that uses a `float`
  in its call flow is automatically pinned to the core it is running on. FPU use inside an interrupt
  handler is not supported by default.

## Amazon SMP kernel
`CONFIG_FREERTOS_SMP=y` selects the Amazon SMP FreeRTOS kernel instead of the IDF kernel. In the v6.1 Kconfig it
depends on the ESP32 target and is labelled "FEATURE UNDER DEVELOPMENT" (use at your own risk); both kernels
are SMP-capable but differ in implementation and features. Don't mix assumptions between them; pick one.

## Verify
- [ ] Every shared variable between tasks on different cores has a lock or atomic.
- [ ] Stress test with tasks floating across cores shows no data races (counters consistent).

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-reference/system/freertos_idf.rst, components/freertos/Kconfig, components/esp_system/include/esp_freertos_hooks.h, components/esp_wifi/Kconfig).
Confirmed: dual-core targets and the Vanilla FreeRTOS v10.5.1 base; `xTaskCreatePinnedToCore` and `tskNO_AFFINITY`; per-core independent scheduling and the example where the second-highest-priority task does not run; best-effort round-robin; `vTaskSuspendAll` only affecting the calling core and not giving mutual exclusion; spinlock critical-section API with `portMUX_TYPE`, `portMUX_INITIALIZER_UNLOCKED`, `_ISR` variants and the short-critical-section guidance; `esp_register_freertos_idle_hook_for_cpu`; lazy FPU context and automatic pinning; `CONFIG_ESP_WIFI_TASK_CORE_ID` default core 0; `CONFIG_FREERTOS_SMP` ESP32-only and under development. Removed unconfirmed claims: `vTaskCoreAffinitySet` and the interrupt-watchdog consequence of long critical sections.

Method: documentation only; no commands were run.
