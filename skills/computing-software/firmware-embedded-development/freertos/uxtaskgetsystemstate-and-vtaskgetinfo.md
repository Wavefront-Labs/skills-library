---
id: computing-software.firmware-embedded-development.freertos.uxtaskgetsystemstate-and-vtaskgetinfo
name: uxtaskgetsystemstate-and-vtaskgetinfo
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [uxtaskgetsystemstate, vtaskgetinfo, taskstatus-t, configuse-trace-facility, task-introspection, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Collect structured per-task data with uxTaskGetSystemState and vTaskGetInfo (state, priorities, stack high-water, runtime) for telemetry and health checks."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/02-uxTaskGetSystemState
  - https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/03-vTaskGetInfo
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uxTaskGetSystemState and vTaskGetInfo

Unlike `vTaskList`, which formats a text table, these return a `TaskStatus_t` struct per task,
suitable for binary telemetry, health checks and watchdog decisions.

Requires `configUSE_TRACE_FACILITY 1`. Runtime counters also need
`configGENERATE_RUN_TIME_STATS 1`.

## All tasks
```c
#define MAX_TASKS 24
static TaskStatus_t ts[MAX_TASKS];

void dump_tasks(void)
{
    configRUN_TIME_COUNTER_TYPE total;
    UBaseType_t n = uxTaskGetSystemState(ts, MAX_TASKS, &total);
    if (n == 0) { /* array too small: returns 0, not a partial list */ return; }
    for (UBaseType_t i = 0; i < n; i++) {
        printf("%-12s st=%d pri=%lu/%lu hwm=%u rt=%lu%%\n",
               ts[i].pcTaskName, ts[i].eCurrentState,
               (unsigned long)ts[i].uxCurrentPriority, (unsigned long)ts[i].uxBasePriority,
               (unsigned)ts[i].usStackHighWaterMark,
               total ? (unsigned long)(ts[i].ulRunTimeCounter * 100ULL / total) : 0UL);
    }
}
```
Size the array with `uxTaskGetNumberOfTasks()` plus slack; if tasks outnumber it, you get 0.
Use a static array: `TaskStatus_t` is a multi-word struct, too much for a small stack times 24.

## One task
```c
TaskStatus_t s;
vTaskGetInfo(hWorker, &s, pdTRUE /*compute stack HWM*/, eInvalid /*query state*/);
```
- `xGetFreeStackSpace = pdFALSE` skips the stack scan (it walks the stack looking for the fill
  pattern, slow for big stacks).
- Passing a known state instead of `eInvalid` skips the state lookup.

## Fields worth using
| Field | Use |
|---|---|
| `usStackHighWaterMark` | minimum free stack ever, in **words**; alarm below a threshold |
| `uxCurrentPriority` vs `uxBasePriority` | differs while the task inherits via a mutex |
| `eCurrentState` | stuck-task detection |
| `ulRunTimeCounter` | CPU share; diff two snapshots for recent usage |
| `xTaskNumber` | stable id for correlating snapshots |
| `uxCoreAffinityMask` | SMP builds only |

## Cost and safety
`uxTaskGetSystemState` suspends the scheduler while it walks every list, and with stack HWM
it scans every stack. Call it from a low-priority task at a slow rate (seconds), never from an
ISR, and not in time-critical paths.

## Verify
- [ ] Array sized from task count with headroom; zero return handled.
- [ ] Health task alarms on low stack HWM and on any task with zero runtime delta when it should
      be running.

## Checked
2026-11-01. Confirmed in FreeRTOS-Kernel tasks.c and include/task.h: `uxTaskGetSystemState` calls `vTaskSuspendAll`
and returns 0 when the array is smaller than the task count, `TaskStatus_t` fields (`xTaskNumber`, `uxCurrentPriority`,
`uxBasePriority`, `ulRunTimeCounter`, `usStackHighWaterMark`, `uxCoreAffinityMask` in SMP), `vTaskGetInfo`
signature with `xGetFreeStackSpace` and a state argument, `configRUN_TIME_COUNTER_TYPE`. Removed the byte size of
`TaskStatus_t` and the claim that the docs flag the call as debug-only.
Method: documentation only; no commands were run.
