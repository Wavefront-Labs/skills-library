---
id: computing-software.firmware-embedded-development.freertos.freertos-mpu-restricted-tasks
name: freertos-mpu-restricted-tasks
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-smp, freertos-mpu, xtaskcreaterestricted, memory-region-t, privileged-functions, privileged-data, mpu-wrappers, freertos, firmware-embedded-development]
level: sme
status: docs-checked
description: "Isolate FreeRTOS tasks with the MPU ports: xTaskCreateRestricted, per-task memory regions, privileged kernel sections in the linker script, and the v2 MPU wrappers."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/FreeRTOS.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/mpu_wrappers.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/GCC/ARM_CM4_MPU/portmacro.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/portable/GCC/ARM_CM33/non_secure/port.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FreeRTOS-MPU restricted tasks

**Goal:** contain faults and untrusted code (third-party libraries, parsers, network stacks)
so a bug in one task can't corrupt the kernel or other tasks' memory.

## Port and config
Use an MPU port: the kernel repository has `portable/GCC/ARM_CM3_MPU`, `ARM_CM4_MPU` and
`ARM_CM33` (the latter with `configENABLE_MPU 1`, a setting the kernel describes as used by
ARMv8-M ports). Key settings (the numbers are examples):
```c
#define configENABLE_MPU 1                       /* ARMv8-M ports; default 0 */
#define configUSE_MPU_WRAPPERS_V1 0              /* default 0 = MPU wrappers v2 */
#define configENABLE_ACCESS_CONTROL_LIST 1       /* needed for vGrantAccessTo*() with v2 wrappers */
#define configPROTECTED_KERNEL_OBJECT_POOL_SIZE 10
#define configSYSTEM_CALL_STACK_SIZE 128         /* in words */
#define configTOTAL_MPU_REGIONS 8                /* the v8-M port asserts 8 or 16 */
```
The kernel code must sit in a privileged-only flash region: the port code references the
linker symbols `__privileged_functions_start__` and `__privileged_functions_end__`, so your
linker script must define them. Take the full list of required symbols and the alignment rules
from your port's documentation and sources.

## Creating a restricted task
```c
static StackType_t net_stack[512] __attribute__((aligned(512 * sizeof(StackType_t))));
static uint8_t rx_buf[1024] __attribute__((aligned(1024)));
static const TaskParameters_t net_params = {
    .pvTaskCode = net_task, .pcName = "net", .usStackDepth = 512,
    .pvParameters = NULL, .uxPriority = 3,      /* no portPRIVILEGE_BIT: unprivileged */
    .puxStackBuffer = net_stack,
    .xRegions = {
        { rx_buf, sizeof rx_buf, portMPU_REGION_READ_WRITE | portMPU_REGION_EXECUTE_NEVER },
        { 0, 0, 0 }, { 0, 0, 0 } } };
xTaskCreateRestricted(&net_params, &h);
```
The task can access its stack and its listed regions; other memory raises a MemManage fault.
With MPU wrappers enabled, `mpu_wrappers.h` redirects kernel API calls to `MPU_` wrapper
functions. `xTaskCreateRestricted` takes a `TaskParameters_t` (`pvTaskCode`, `pcName`,
`usStackDepth`, `pvParameters`, `uxPriority`, `puxStackBuffer`, `xRegions`); a task is
privileged only if `portPRIVILEGE_BIT` is set in `uxPriority`. Stack and region alignment
requirements are port-specific (see the examples in task.h).

## Granting kernel objects (v2 wrappers)
With v2 wrappers and `configENABLE_ACCESS_CONTROL_LIST 1`, unprivileged tasks may only use
kernel objects they were granted: `vGrantAccessToQueue(task, queue)`, `vGrantAccessToSemaphore`,
`vGrantAccessToTask`, `vGrantAccessToQueueSet` (mpu_wrappers.h).

## Gotchas
- Peripherals: unprivileged tasks can't touch peripheral registers unless a region grants it;
  better to route hardware access through a privileged driver task via queues.
- Region count is small: on the Cortex-M4 MPU port the configurable task regions are
  `configTOTAL_MPU_REGIONS - 5`, so 3 with 8 regions; design data layouts accordingly.
- Faults in restricted tasks: handle MemManage by deleting/restarting the offending task instead
  of resetting the whole system.

## Verify
- [ ] Deliberate out-of-region write from the restricted task triggers MemManage, other tasks
      keep running.
- [ ] Map file shows kernel code between the privileged-function start and end symbols.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: configENABLE_MPU (default 0, used by ARMv8-M ports) and configUSE_MPU_WRAPPERS_V1 (default 0) in FreeRTOS.h; vGrantAccessTo* are defined only for v2 wrappers with configENABLE_ACCESS_CONTROL_LIST == 1 (mpu_wrappers.h); TaskParameters_t fields, xTaskCreateRestricted and portPRIVILEGE_BIT (task.h); configSYSTEM_CALL_STACK_SIZE in words and configPROTECTED_KERNEL_OBJECT_POOL_SIZE required by the port headers; the v8-M port asserts configTOTAL_MPU_REGIONS is 8 or 16; the CM4 MPU port defines portNUM_CONFIGURABLE_REGIONS as configTOTAL_MPU_REGIONS - 5; port code uses __privileged_functions_start__/end__. Removed the privileged_data linker section, the alignment rules and the SVC claim, which the sources fetched do not confirm. 
Method: documentation only; no commands were run.
