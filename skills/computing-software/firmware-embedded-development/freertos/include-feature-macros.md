---
id: computing-software.firmware-embedded-development.freertos.include-feature-macros
name: include-feature-macros
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [include-macros, include-vtaskdelete, include-vtasksuspend, freertosconfig-h, api-trimming, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Set FreeRTOS INCLUDE_ macros to compile in exactly the optional APIs you use, decode the link errors they cause, and know which ones change kernel behaviour."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/FreeRTOS.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/event_groups.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/History.txt
  - https://github.com/FreeRTOS/FreeRTOS-Kernel-Book/blob/main/ch05.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# INCLUDE_ feature macros

`INCLUDE_xxx` in `FreeRTOSConfig.h` decides whether the optional API `xxx` is compiled. Setting
one to 0 saves flash; using a disabled API gives an **undefined reference** at link time (or an
implicit-declaration warning), not a runtime error.

## Common set
```c
#define INCLUDE_vTaskPrioritySet             1
#define INCLUDE_uxTaskPriorityGet            1
#define INCLUDE_vTaskDelete                  1
#define INCLUDE_vTaskSuspend                 1
#define INCLUDE_xTaskDelayUntil              1   /* replaces INCLUDE_vTaskDelayUntil (xTaskDelayUntil added in V10.4.2) */
#define INCLUDE_vTaskDelay                   1
#define INCLUDE_xTaskGetSchedulerState       1
#define INCLUDE_xTaskGetCurrentTaskHandle    1
#define INCLUDE_uxTaskGetStackHighWaterMark  1
#define INCLUDE_xTaskGetIdleTaskHandle       0
#define INCLUDE_eTaskGetState                1
#define INCLUDE_xTimerPendFunctionCall       1   /* also needs configUSE_TIMERS 1 */
#define INCLUDE_xTaskAbortDelay              0
#define INCLUDE_xTaskGetHandle               0
#define INCLUDE_xSemaphoreGetMutexHolder     1
```
Defaults (from `FreeRTOS.h`) apply when a macro is omitted: in V11.3.2 most of the ones above
default to 0, while `INCLUDE_xTaskResumeFromISR` and `INCLUDE_xTaskGetCurrentTaskHandle`
default to 1. State every macro you rely on explicitly.

## Macros that change behaviour, not just availability
- A block time of `portMAX_DELAY` waits indefinitely only if `INCLUDE_vTaskSuspend` is 1
  (Kernel Book, queue API descriptions). With it 0 the wait is just the largest tick count and
  code expecting "wait forever" eventually times out.
- Deleted-task memory is reclaimed by the idle task, so keep the idle task from starvation
  (task.h `vTaskDelete`); `INCLUDE_vTaskDelete` compiles the deletion support.
- `INCLUDE_xTimerPendFunctionCall` requires `configUSE_TIMERS 1`; the ISR-safe event-group
  functions such as `xEventGroupSetBitsFromISR` and `xEventGroupClearBitsFromISR` are compiled
  only when both are set, because they are deferred through the timer command queue.

## Debugging a link error
```
undefined reference to `vTaskDelete'
```
Search `FreeRTOSConfig.h` for the matching `INCLUDE_` macro; also check the build includes the
right `FreeRTOSConfig.h` (projects often have several, and the wrong one on the include path is
a classic cause).

## Trimming for size
Linker section garbage collection (for example `-ffunction-sections -fdata-sections
-Wl,--gc-sections` with GCC) can drop unused functions even when their INCLUDE_ macro is 1;
the macros matter most when you do not use it.

## Verify
- [ ] Every INCLUDE_ macro the code relies on is explicit in `FreeRTOSConfig.h`.
- [ ] `INCLUDE_vTaskSuspend` is 1 wherever `portMAX_DELAY` means "forever".
- [ ] Only one `FreeRTOSConfig.h` is on the include path.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: INCLUDE_ defaults in FreeRTOS.h (0 for the listed macros except INCLUDE_xTaskResumeFromISR and INCLUDE_xTaskGetCurrentTaskHandle, which are 1); INCLUDE_xTaskDelayUntil replaced INCLUDE_vTaskDelayUntil and xTaskDelayUntil was introduced in V10.4.2 (History.txt); portMAX_DELAY waits indefinitely only with INCLUDE_vTaskSuspend 1 (Book ch05); the idle task frees deleted tasks (task.h); event-group ISR functions need INCLUDE_xTimerPendFunctionCall and configUSE_TIMERS (event_groups.c). Removed INCLUDE_xEventGroupSetBitsFromISR, which is not a macro in FreeRTOS.h, and the certification claim. 
Method: documentation only; no commands were run.
