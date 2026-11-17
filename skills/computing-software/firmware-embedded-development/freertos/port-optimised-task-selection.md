---
id: computing-software.firmware-embedded-development.freertos.port-optimised-task-selection
name: port-optimised-task-selection
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [port-optimised-task-selection, configuse-port-optimised-task-selection, clz-instruction, configmax-priorities, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Enable configUSE_PORT_OPTIMISED_TASK_SELECTION to pick the next FreeRTOS task with a count-leading-zeros instruction, its 32-priority limit, and when it is unavailable."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/tasks.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Port-optimised task selection

```c
#define configUSE_PORT_OPTIMISED_TASK_SELECTION  1
#define configMAX_PRIORITIES                     8   /* must be <= 32 with the option on */
```

## What it changes
The scheduler keeps one ready list per priority. To find the highest-priority ready task:
- **Generic method (0):** walk down from `uxTopReadyPriority` until a non-empty list is found.
  Portable C, time grows with the number of empty priority levels, any `configMAX_PRIORITIES`.
- **Port-optimised (1):** maintain a 32-bit bitmap of non-empty ready lists and find the top bit
  with one instruction (`CLZ` on ARMv7-M/ARMv8-M Mainline, equivalent on some RISC-V and other
  ports). Constant time, slightly faster context switches.

## Constraints
- Max 32 priorities (bitmap width). A build with `configMAX_PRIORITIES > 32` stops with a
  `#error` in the port's `portmacro.h`.
- Only ports that define `portRECORD_READY_PRIORITY`, `portRESET_READY_PRIORITY` and
  `portGET_HIGHEST_PRIORITY` support it. The Cortex-M0 GCC port's `portmacro.h` does not mention
  the option, so it does not offer it.
- On SMP builds (`configNUMBER_OF_CORES` > 1) the option must be 0; `FreeRTOS.h` stops with an
  `#error` otherwise.
- A wrapper layer that needs more than 32 priorities forces the generic method. Remap priorities
  or accept generic selection.

## Is it worth it
Gains are tens of cycles per switch; significant only at very high switch rates or with many
priority levels in use. Mainly useful because it also caps priorities at 32, nudging toward fewer
levels; most systems need fewer than 10.

## Verify
- [ ] Port supports the option (check `portmacro.h` for the macros).
- [ ] `configMAX_PRIORITIES` <= 32 and SMP disabled when the option is 1.
- [ ] Context switch cycle count measured with DWT before and after, if performance is the reason.

## Checked
2026-11-01. Confirmed in FreeRTOS-Kernel source: tasks.c (generic walk versus port macros), FreeRTOS.h (default 0,
SMP `#error`), portable/GCC/ARM_CM4F/portmacro.h and RISC-V/portmacro.h (`clz` bitmap helper, 32-priority `#error`,
the three port macros). Removed: the CMSIS-RTOS 56-priority claim and the M23 claim, which the source does not
confirm. The cycle-count claim ("tens of cycles") is not documented; kept only as the advice to measure.
Method: documentation only; no commands were run.
