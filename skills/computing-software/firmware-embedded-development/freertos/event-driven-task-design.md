---
id: computing-software.firmware-embedded-development.freertos.event-driven-task-design
name: event-driven-task-design
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [event-driven-task, active-object, event-loop, polling-elimination, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Structure FreeRTOS tasks as event-driven loops that block on one input (queue or notification) instead of polling: active-object pattern, timeouts as events, and CPU savings."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/queue.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event-driven task design

**Principle:** a task should be Blocked unless it has work. Polling loops (`for(;;){ if (flag)
...; vTaskDelay(10); }`) waste CPU, add up to one poll period of latency, and starve
lower priorities if the delay is forgotten.

## Active-object pattern
One task per subsystem, one input queue of events, one state machine:
```c
typedef enum { EV_BTN, EV_RX_FRAME, EV_TIMEOUT, EV_SHUTDOWN } ev_type_t;
typedef struct { ev_type_t type; uint32_t arg; } event_t;

static QueueHandle_t qComms;
static TimerHandle_t tmrRetry;

static void retry_cb(TimerHandle_t t) {
    event_t e = { EV_TIMEOUT, 0 };
    xQueueSend(qComms, &e, 0);               /* timeouts become events too */
}

static void vCommsTask(void *pv) {
    comms_state_t st = ST_IDLE;
    event_t e;
    for (;;) {
        xQueueReceive(qComms, &e, portMAX_DELAY);     /* the ONLY blocking point */
        st = comms_dispatch(st, &e);                   /* run to completion, never block */
    }
}
```
ISRs and other tasks post events with `xQueueSendFromISR` / `xQueueSend`. The dispatcher
handles each event fully and returns; it never waits inside a handler.

## Rules
- **Single blocking point** per task. A handler that calls `vTaskDelay` or waits on another queue
  makes the task deaf to its own events; use a timer that posts an event instead.
- **Timeouts as events:** software timers or a receive timeout (`xQueueReceive(q, &e, next_deadline)`
  returning `pdFALSE` -> handle `EV_TIMEOUT`).
- **Lightweight variant:** when events are just flags, senders call `xTaskNotify` with `eSetBits`
  and the task blocks in `xTaskNotifyWait` instead of using a queue.
- **Queue length** sized for the worst event burst; count dropped events.
- Shared data between active objects travels inside events, so most mutexes disappear.

## Benefits
- The idle task gets real time, which low-power hooks can use.
- Latency to an event is the scheduling latency, not a poll period.
- State machines are testable on host: feed events, check states.

## When polling is still right
Hardware with no interrupt and a slow rate (e.g. reading an I2C sensor every 100 ms) is fine as a
periodic task using `xTaskDelayUntil`; that's time-triggered, not busy polling.

## Verify
- [ ] Each task has one blocking call in its main loop (grep for extra waits in handlers).
- [ ] Run-time stats show idle time dominates when the system is quiescent.
- [ ] Event-queue high-water marks recorded under burst load.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: eSetBits is an eAction value for xTaskNotify (the sender), with the receiver blocking in xTaskNotifyWait (task.h); xTaskDelayUntil exists for fixed-frequency tasks (task.h); xQueueReceive with a timeout returns pdFALSE on expiry (queue.h). Removed the tickless-idle claim and corrected the notification wording. 
Method: documentation only; no commands were run.
