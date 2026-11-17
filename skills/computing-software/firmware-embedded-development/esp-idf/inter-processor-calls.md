---
id: computing-software.firmware-embedded-development.esp-idf.inter-processor-calls
name: inter-processor-calls
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-dual-core, esp-ipc, esp-ipc-call, esp-ipc-isr, cross-core-execution, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Run a function on the other ESP32 core with esp_ipc_call and esp_ipc_isr: when you need it (core-bound registers, interrupt allocation), blocking semantics and limits."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/ipc.html
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_system/include/esp_ipc.h
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_system/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inter-processor calls (IPC)

Some operations must run on a specific core: per-core registers (interrupt matrix allocation
on that core, CCOUNT, cache settings), or functions that touch core-local state. IPC executes a
callback on the other core.

## Task-context IPC
```c
#include "esp_ipc.h"
static void alloc_on_core1(void *arg) {
    esp_intr_alloc(ETS_GPIO_INTR_SOURCE, ESP_INTR_FLAG_IRAM, gpio_isr, arg, NULL);
}
ESP_ERROR_CHECK(esp_ipc_call_blocking(1, alloc_on_core1, ctx));   /* waits for completion */
/* esp_ipc_call(1, fn, arg) returns once fn has started */
```
Runs in the target core's IPC task, created at the highest priority (`configMAX_PRIORITIES - 1`);
with `CONFIG_ESP_IPC_USES_CALLERS_PRIORITY` (default y) the task's priority is lowered to the
target core's current priority before the callback runs. The callback must never block or yield.
Stack size: `CONFIG_ESP_IPC_TASK_STACK_SIZE` (default 1024 bytes, 1280 on ESP32-S3, 2048 with app tracing; raise it if the callback is heavy).
The IPC feature is protected by a mutex, so simultaneous calls from several cores are serialised. Both calls return
`ESP_ERR_INVALID_STATE` if the FreeRTOS scheduler is not running.

## ISR-context IPC
```c
esp_ipc_isr_call_blocking(fn, arg);     /* fn runs in a High Priority Interrupt on the other core; busy-waits until done */
esp_ipc_isr_stall_other_cpu(); ... esp_ipc_isr_release_other_cpu();   /* stall and resume the other core */
```
`esp_ipc_isr_call` returns once the callback has begun; `esp_ipc_isr_call_blocking` waits for completion. On Xtensa chips the callback
(type `esp_ipc_isr_func_t`) must be written entirely in assembly, placed in IRAM at a 4-byte aligned address, and may only use registers a2
(the `void *arg`), a3 and a4; on RISC-V chips it can be written in C with the same restrictions as a regular interrupt handler.
While the callback runs, the calling core disables interrupts of level 3 and lower.

## Alternatives
Often simpler: create a task pinned to the core (`xTaskCreatePinnedToCore`) and do the work there,
or allocate interrupts from a task that is already pinned to that core.

## Pitfalls
- A callback that blocks or yields blocks the target core's IPC task (and, through the mutex, every other IPC caller).
- In single-core mode `esp_ipc_call` and `esp_ipc_call_blocking` return `ESP_ERR_INVALID_ARG` for core 1.
- The task-context variants (`esp_ipc_call`, `esp_ipc_call_blocking`) are for task context; do not call them from ISRs.

## Verify
- [ ] `esp_intr_dump(stdout)` shows the interrupt on the intended core.
- [ ] Callback runs on the right core (`esp_cpu_get_core_id()` inside it).

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-reference/system/ipc.rst, components/esp_system/include/esp_ipc.h, components/esp_system/Kconfig, esp_intr_alloc.h and esp_cpu.h).
Confirmed: `esp_ipc_call` (returns when the callback has begun) and `esp_ipc_call_blocking` (waits for completion), `esp_ipc_isr_call`, `esp_ipc_isr_call_blocking`, `esp_ipc_isr_stall_other_cpu`/`esp_ipc_isr_release_other_cpu`; the Xtensa assembly-only ISR callback restrictions and RISC-V C callbacks; IPC task priority and `CONFIG_ESP_IPC_USES_CALLERS_PRIORITY`; `CONFIG_ESP_IPC_TASK_STACK_SIZE` defaults; ESP_ERR_INVALID_ARG for cpu 1 in single-core mode; `esp_intr_alloc`, `esp_intr_dump`, `esp_cpu_get_core_id` exist. Removed unconfirmed or wrong claims: that the ISR callback can be an ordinary short C function on Xtensa, the `ipc1` task name, flash operations being the user of the stall API, an inline run when targeting the current core and the high-priority-hog deadlock scenario.

Method: documentation only; no commands were run.
