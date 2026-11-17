---
id: computing-software.firmware-embedded-development.freertos.passing-parameters-to-tasks
name: passing-parameters-to-tasks
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [task-parameters, pvparameters, xtaskcreate, task-instance-data, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Pass per-instance data into FreeRTOS tasks through pvParameters safely: lifetime rules, one task function for many instances, and casting integers without UB."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/GCC/ARM_CM4F/port.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passing parameters to tasks

**Goal:** one task function, several instances (e.g. one per UART), each with its own config,
without globals.

## Pattern
```c
typedef struct {
    UART_HandleTypeDef *huart;
    QueueHandle_t       rx;
    uint32_t            baud;
} uart_task_cfg_t;

static uart_task_cfg_t cfg1 = { &huart1, NULL, 115200 };   /* static storage */
static uart_task_cfg_t cfg2 = { &huart2, NULL, 9600 };

static void vUartTask(void *pv)
{
    uart_task_cfg_t *cfg = (uart_task_cfg_t *)pv;   /* cast once, at the top */
    configASSERT(cfg != NULL);
    for (;;) { /* use cfg->huart, cfg->rx ... */ }
}

cfg1.rx = xQueueCreate(32, 1);
xTaskCreate(vUartTask, "uart1", 512, &cfg1, 3, NULL);
xTaskCreate(vUartTask, "uart2", 512, &cfg2, 3, NULL);
```

## The lifetime rule
`pvParameters` is just a pointer copied into the TCB. The task may not run until after the
creating function returns (or the scheduler starts), so the pointee **must outlive the task**:
- OK: `static`/global objects, heap blocks owned by the task, `const` tables.
- Broken: a local struct in `main()` or in a creator function. On the Cortex-M ports the
  scheduler start sets the main stack pointer back to the start of the stack (port.c), so
  `main()`'s locals are not preserved.

If the task takes ownership of a heap block, document it and `vPortFree()` it before
`vTaskDelete(NULL)`.

## Passing a small integer
```c
xTaskCreate(vLedTask, "led0", 128, (void *)(uintptr_t)LED_GREEN, 1, NULL);
/* in the task */
uint32_t led = (uint32_t)(uintptr_t)pv;
```
Go through `uintptr_t` so the integer-to-pointer conversion is explicit and the same width on
every target.

## Gotchas
- Same function, many instances: every local variable is per-instance (own stack), but any
  `static` local inside the task function is shared by all instances.
- Do not pass the address of a loop variable when creating tasks in a loop; all tasks get the
  same pointer. Use an array of configs indexed by the loop counter.
- With `xTaskCreateStatic` the parameter rule is identical; only the stack/TCB storage moves.

## Verify
- [ ] Every pvParameters pointee has static or task-owned heap lifetime.
- [ ] Two instances run concurrently with different configs (check with a debugger or log).
- [ ] No `static` locals inside a multi-instance task function unless deliberately shared.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: xTaskCreate takes a void * pvParameters stored for the task (task.h); the Cortex-M4F port resets MSP to the start of the stack when starting the first task (port.c, "Set the msp back to the start of the stack"); static allocation takes the same parameter. Removed the 64-bit warning claim. 
Method: documentation only; no commands were run.
