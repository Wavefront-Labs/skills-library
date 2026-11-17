---
id: computing-software.firmware-embedded-development.freertos.timer-ids-pvtimergettimerid
name: timer-ids-pvtimergettimerid
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [pvtimergettimerid, vtimersettimerid, timer-id, shared-timer-callback, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use FreeRTOS timer IDs (pvTimerGetTimerID, vTimerSetTimerID) to share one callback across many timers and keep per-timer state such as expiry counts."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/timers.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/timers.c
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/FreeRTOS.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timer IDs

The `pvTimerID` argument of `xTimerCreate` is an opaque `void *` stored in the timer. The
kernel never reads it; it exists so callbacks can tell timers apart and carry state.

## One callback, many timers
```c
typedef struct { uint8_t channel; uint32_t timeouts; } chan_watch_t;
static chan_watch_t watch[4];

static void vChanTimeoutCb(TimerHandle_t t)
{
    chan_watch_t *w = pvTimerGetTimerID(t);
    w->timeouts++;
    channel_reset(w->channel);
}

for (int i = 0; i < 4; i++) {
    watch[i].channel = i;
    tmr[i] = xTimerCreate("chwd", pdMS_TO_TICKS(100), pdFALSE, &watch[i], vChanTimeoutCb);
}
```

## Counter stored directly in the ID
For a small integer, store it in the pointer itself:
```c
static void vBlinkCb(TimerHandle_t t)
{
    uint32_t n = (uint32_t)(uintptr_t)pvTimerGetTimerID(t);
    if (++n >= 10) xTimerStop(t, 0);               /* block time 0 inside callbacks */
    vTimerSetTimerID(t, (void *)(uintptr_t)n);
}
```

## Rules
- `vTimerSetTimerID` and `pvTimerGetTimerID` are plain task-context functions (no `FromISR` variants), so call them from tasks and timer callbacks.
- Pointer IDs must reference memory that outlives the timer (static or owned heap).
- Comparing handles (`if (t == tmrA)`) also works for a few timers, but IDs scale better and
  avoid globals.
- `pcTimerGetName` returns the name string, handy for logging, but don't use it to dispatch.

## Verify
- [ ] Shared callback distinguishes timers via the ID, not global flags.
- [ ] No ISR code calls the ID accessors (they have no `FromISR` variants).

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: `pvTimerGetTimerID`, `vTimerSetTimerID`, `pcTimerGetName` and `xTimerCreate` exist (timers.h, FreeRTOS.h). Removed or rewritten: the FreeRTOS-book attribution and the critical-section/command-queue claim.
Method: documentation only; no commands were run.
