---
id: computing-software.firmware-embedded-development.freertos.run-time-statistics
name: run-time-statistics
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-debugging, run-time-stats, configgenerate-run-time-stats, vtaskgetruntimestats, cpu-usage-per-task, runtime-counter, idle-time, freertos, firmware-embedded-development]
level: practitioner
status: draft
description: "Measure CPU time per FreeRTOS task with run-time stats: configure a fast counter, read uxTaskGetSystemState or vTaskGetRunTimeStats, and compute load over windows."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-RTOS-run-time-stats
  - https://www.freertos.org/Documentation/02-Kernel/04-API-references/03-Task-utilities/02-uxTaskGetSystemState
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FreeRTOS run-time statistics

**Goal:** know which tasks use the CPU and how much headroom is left, in the field, without a
trace probe.

## Configuration
```c
#define configGENERATE_RUN_TIME_STATS 1
#define configUSE_TRACE_FACILITY 1
#define configUSE_STATS_FORMATTING_FUNCTIONS 1        /* for vTaskGetRunTimeStats text */
#define portCONFIGURE_TIMER_FOR_RUN_TIME_STATS() runtime_counter_init()
#define portGET_RUN_TIME_COUNTER_VALUE() (DWT->CYCCNT)  /* or a free-running timer CNT */
```
The counter must tick **10-100x faster than the RTOS tick**, otherwise short tasks show 0 %.
DWT CYCCNT at core clock is ideal on M3+ (wraps in tens of seconds at high clocks: use
`configRUN_TIME_COUNTER_TYPE uint64_t` in recent kernels or a 32-bit timer at 10-100 kHz).

## Reading
Text table (needs a buffer of ~40 bytes per task):
```c
static char buf[1024];
vTaskGetRunTimeStats(buf);   /* "Task  AbsTime  %Time" per line */
```
Structured, for logs/telemetry:
```c
UBaseType_t n = uxTaskGetNumberOfTasks();
TaskStatus_t *st = pvPortMalloc(n * sizeof *st);
configRUN_TIME_COUNTER_TYPE total;
n = uxTaskGetSystemState(st, n, &total);
for (UBaseType_t i = 0; i < n; i++)
    printf("%-12s %3u%% stack_free=%u\n", st[i].pcTaskName,
           (unsigned)(st[i].ulRunTimeCounter * 100ULL / total), st[i].usStackHighWaterMark);
vPortFree(st);
```
These are **cumulative since boot**. For current load, snapshot twice and diff counters over
the window (e.g. every 5 s). `ulTaskGetIdleRunTimePercent()` gives idle percentage directly.

## Interpreting
- Idle task % = headroom. Below ~20-30 % in normal operation leaves little margin for bursts.
- A task with steady high % that should be event-driven usually polls; look for
  `vTaskDelay(0)`/busy loops.
- ISR time is attributed to whichever task was interrupted; heavy interrupt load shows up as
  inflated percentages on random tasks. Use trace tools for ISR accounting.

## Costs
`uxTaskGetSystemState` suspends the scheduler while walking task lists: fine for debug and
periodic telemetry, not for a 1 ms loop. Counter read happens at every context switch: keep
`portGET_RUN_TIME_COUNTER_VALUE` a single register read.

## Verify
- [ ] Busy-loop test task shows close to its expected share.
- [ ] Percentages sum to ~100 % over a window.
- [ ] Counter does not wrap within the measurement window (or 64-bit counter used).
