---
id: computing-software.firmware-embedded-development.esp-idf.stack-smashing-protection
name: stack-smashing-protection
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-debug, esp-stack-smashing, stack-protector, stack-overflow-detection, watchpoint-end-of-stack, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Detect stack buffer overflows and task stack exhaustion in ESP-IDF with -fstack-protector modes, FreeRTOS stack overflow checks, end-of-stack watchpoints and high-water marks."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/fatal-errors.html#stack-smashing
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/freertos_idf.html
  - https://github.com/espressif/esp-idf/blob/v6.1/Kconfig
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/performance/ram-usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stack smashing protection

Two different problems:
1. **Stack smashing**: a local buffer overflow overwrites the return address/canary.
2. **Stack overflow**: the task uses more stack than allocated.

## Compiler stack protector
```
CONFIG_COMPILER_STACK_CHECK_MODE_NORM    # -fstack-protector: functions calling alloca and functions with buffers larger than 8 bytes
CONFIG_COMPILER_STACK_CHECK_MODE_STRONG  # -fstack-protector-strong: NORM plus functions with local arrays or references to local frame addresses
CONFIG_COMPILER_STACK_CHECK_MODE_ALL     # -fstack-protector-all: every function (largest cost)
```
Failure output:
```
Stack smashing protect failure!
Backtrace: ...
```
The backtrace should point to the function where stack smashing occurred (the one whose guard failed). Inspect its local
arrays and every `memcpy`/`sprintf` into them. The Kconfig help notes the protection also increases the stack each task needs.

## Task stack overflow
```
CONFIG_FREERTOS_CHECK_STACKOVERFLOW_CANARY=y      # checked at context switch
CONFIG_FREERTOS_WATCHPOINT_END_OF_STACK=y          # hardware watchpoint: catches it immediately
```
Output: `***ERROR*** A stack overflow in task <name> has been detected.` The watchpoint option watches the last 32 bytes of
the stack (so it can trigger up to 28 bytes early, before the 20-byte FreeRTOS canary is corrupted); on Xtensa it reports
`Debug exception reason: Stack canary watchpoint triggered (<task>)`, on RISC-V a Breakpoint exception. It is not guaranteed
to catch every overflow, because a task can write past the canary. Chips with the assist-debug module also offer a hardware
stack guard (`CONFIG_ESP_SYSTEM_HW_STACK_GUARD`) that raises "Stack protection fault".

## Size stacks properly
```c
UBaseType_t free_bytes = uxTaskGetStackHighWaterMark(NULL);   /* minimum free stack so far; ESP-IDF stack units are bytes */
ESP_LOGI(TAG, "min free stack %u", free_bytes);
```
On ESP-IDF, stack sizes in `xTaskCreate` are in **bytes**, unlike vanilla FreeRTOS (words). Run
worst-case paths (TLS handshake, formatted printing, deep JSON), then size the stack from the measured peak plus a margin you choose.
`vTaskList`/`uxTaskGetSystemState` with `CONFIG_FREERTOS_USE_TRACE_FACILITY` lists all tasks.

## Heavy stack users
Formatted printing, TLS handshakes in the calling task, recursive parsers and large local arrays (make
them static or heap-allocated). Measure these with the high-water mark rather than trusting fixed figures.

## Verify
- [ ] Dev builds run with strong stack protector and end-of-stack watchpoint.
- [ ] High-water marks logged after a soak test; every task has margin.

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-guides/fatal-errors.rst stack overflow and stack smashing sections, docs/en/api-reference/system/freertos_idf.rst, root Kconfig, FreeRTOS-Kernel xtensa port.c and portmacro.h, components/freertos/Kconfig).
Confirmed: `CONFIG_COMPILER_STACK_CHECK_MODE_NORM/STRONG/ALL` meanings and the "Stack smashing protect failure!" output; `CONFIG_FREERTOS_CHECK_STACKOVERFLOW_CANARY`, `CONFIG_FREERTOS_WATCHPOINT_END_OF_STACK` (last 32 bytes, up to 28 bytes early, 20-byte canary, Xtensa message text); the "***ERROR*** A stack overflow in task" string in port.c; stack sizes in bytes (IDF FreeRTOS docs) with `StackType_t` = uint8_t on Xtensa; `CONFIG_FREERTOS_USE_TRACE_FACILITY`; `CONFIG_ESP_SYSTEM_HW_STACK_GUARD`. Removed unconfirmed claims: the strong mode being recommended for development, the specific stack costs of printf with floats and mbedTLS handshakes, and the 25 to 50 percent margin.

Method: documentation only; no commands were run.
