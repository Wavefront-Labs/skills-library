---
id: computing-software.firmware-embedded-development.freertos.one-shot-vs-auto-reload-timers
name: one-shot-vs-auto-reload-timers
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [auto-reload-timer, one-shot-timer, xtimercreate, xtimerreset, vtimersetreloadmode, timeout-watchdog, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Choose and drive FreeRTOS one-shot vs auto-reload software timers: reset-as-timeout, period changes, drift behaviour and the command-queue pitfalls."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/timers.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/timers.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel-Book/blob/main/ch06.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# One-shot vs auto-reload timers

`xTimerCreate(name, period, xAutoReload, id, callback)`. The third argument picks the type:
`pdFALSE` one-shot, `pdTRUE` auto-reload. Timers are created **dormant**; nothing happens
until `xTimerStart`.

## One-shot: timeouts and debouncing
Fires once, then goes dormant. The idiom is "reset = restart the countdown":
```c
static TimerHandle_t idle_tmr;
idle_tmr = xTimerCreate("idle", pdMS_TO_TICKS(30000), pdFALSE, NULL, on_idle);
/* on every user activity: */
xTimerReset(idle_tmr, 0);      /* starts it if dormant, restarts if running */
```
Uses: inactivity sleep, button debounce (reset on each edge, act on expiry), protocol
response timeout, retry backoff (change period, then start).

## Auto-reload: periodic work
```c
TimerHandle_t led = xTimerCreate("led", pdMS_TO_TICKS(500), pdTRUE, NULL, toggle_led);
xTimerStart(led, 0);
```
The next expiry is computed from the **scheduled** expiry time, not from when the callback
ran, so the period doesn't drift with callback latency. If the next expiry has already passed,
the kernel advances the expiry time, calls the callback again and retries, so missed periods are
caught up one callback at a time (`prvReloadTimer` in timers.c).

## Switching and inspecting
- `vTimerSetReloadMode(t, pdTRUE/pdFALSE)` changes type at run time; `uxTimerGetReloadMode`
  reads it.
- `xTimerChangePeriod(t, newPeriod, 0)` can transition a dormant timer into the active state
  (timers.h lists it with start and reset). Don't call it on a timer you meant to keep stopped.
- `xTimerIsTimerActive(t)`, `xTimerGetExpiryTime(t)`.
- Calling `xTimerStop` on a one-shot from its own callback is unnecessary; it's already dormant.
- One callback for many timers: use `pvTimerGetTimerID(t)` to tell them apart.

## Command-queue pitfalls
Start/stop/reset/change calls post commands to the timer daemon's queue
(`configTIMER_QUEUE_LENGTH`); they don't act immediately.
- `xTicksToWait = 0` from a task can fail when the queue is full. Check the return value.
- From ISRs use the `FromISR` variants and yield.
- Commands are processed at `configTIMER_TASK_PRIORITY`. If that's below a busy task, a
  `xTimerReset` meant to postpone a timeout may be processed **after** the expiry has fired.
  Keep the daemon priority above the tasks that reset timers.
- Callbacks run in the daemon task: never block in them. Defer slow work to a worker task.

## Picking the right tool
| Need | Use |
|---|---|
| Sub-tick or jitter-critical period | hardware timer |
| Periodic task with state and real work | task with `xTaskDelayUntil` |
| Light periodic or timeout action | software timer |

## Verify
- [ ] Return values of start/reset/change are checked (or the call uses a non-zero timeout).
- [ ] Reset-as-timeout tested: activity just before expiry really postpones it under CPU load.
- [ ] No blocking calls inside timer callbacks.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: xTimerCreate(pcTimerName, xTimerPeriodInTicks, xAutoReload, pvTimerID, pxCallbackFunction), with timers created dormant and xTimerStart, xTimerReset, xTimerChangePeriod able to activate them (timers.h); vTimerSetReloadMode exists; prvReloadTimer calls the callback again for each already-passed expiry (timers.c); timer commands go through the timer command queue (timers.h, Kernel Book 6). Corrected the parameter name uxAutoReload to xAutoReload and removed the V10.2 version claim. 
Method: documentation only; no commands were run.
