---
id: computing-software.firmware-embedded-development.freertos.passive-idle-tasks-smp
name: passive-idle-tasks-smp
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [passive-idle, vapplicationpassiveidlehook, configuse-passive-idle-hook, smp-idle-task, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Understand FreeRTOS SMP idle tasks: one active idle task doing cleanup, passive idle tasks per extra core, their hooks, memory, and low-power entry per core."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/tasks.c
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/FreeRTOS.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passive idle tasks (SMP)

With `configNUMBER_OF_CORES > 1` (SMP build), the kernel creates one idle task per core
so every core always has something to run:
- **One active idle task** (named `IDLE` unless `configIDLE_TASK_NAME` is set): performs housekeeping (freeing deleted task memory,
  calling `vApplicationIdleHook`).
- **`configNUMBER_OF_CORES - 1` passive idle tasks**: just occupy a core; they do no cleanup.


## Hooks
```c
#define configUSE_IDLE_HOOK          1
#define configUSE_PASSIVE_IDLE_HOOK  1   /* called from the passive idle task; must not block */

void vApplicationIdleHook(void)        { /* cleanup-adjacent work, WFI */ }
void vApplicationPassiveIdleHook(void) { __WFI(); }
```
The kernel comment says the passive hook is meant for core-activity management such as disabling
cores that go idle, and it must not call anything that might block.

## Static memory
With static allocation, provide `vApplicationGetPassiveIdleTaskMemory(..., BaseType_t
xPassiveIdleTaskIndex)` in addition to the idle hook (or set
`configKERNEL_PROVIDED_STATIC_MEMORY 1`). The index runs 0..cores-2.

## Implications
- `configIDLE_SHOULD_YIELD` applies to all idle tasks.
- Low power: each core can `WFI` in its own idle hook. Tickless idle on SMP ports is
  port-specific; check your port before assuming `portSUPPRESS_TICKS_AND_SLEEP` is used.

## Verify
- [ ] Both hooks provided when enabled, using kernel 11 names.
- [ ] A task listing shows one idle task per core.
- [ ] Deleted-task memory returns after deletions under typical load.

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: `configUSE_PASSIVE_IDLE_HOOK`, `vApplicationPassiveIdleHook` and its no-block rule, `configNUMBER_OF_CORES - 1` passive idle tasks, default idle name `IDLE`, `vApplicationGetPassiveIdleTaskMemory` with the passive index, and `configKERNEL_PROVIDED_STATIC_MEMORY` (tasks.c, FreeRTOS.h). Removed or rewritten: `IDLE1`/`IDLE2` names, pre-11 `vApplicationMinimalIdleHook` rename, the 'idle tasks are not pinned' claim, the active-idle-only wording for `configUSE_IDLE_HOOK`, the starvation and time-slicing bullets, RP2040 reference and run-time-stats arithmetic.
Method: documentation only; no commands were run.
