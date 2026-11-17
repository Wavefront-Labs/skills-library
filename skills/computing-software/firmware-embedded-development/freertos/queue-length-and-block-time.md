---
id: computing-software.firmware-embedded-development.freertos.queue-length-and-block-time
name: queue-length-and-block-time
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [queue-length, block-time, uxqueuemessageswaiting, uxqueuespacesavailable, queue-sizing, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Size FreeRTOS queues and pick send/receive block times from producer burst rates, measure high-water marks, and handle a full queue deliberately instead of by accident."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues
  - https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement
  - https://github.com/FreeRTOS/FreeRTOS-Kernel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue length and block time

## Sizing the length
Length must absorb the worst burst the producer can generate while the consumer is not
running:

```
length >= max_producer_rate * worst_consumer_latency + margin
```
Example: UART at 115200 baud delivers about 11.5 bytes/ms. If the consumer can be delayed 8 ms
by higher-priority tasks, a byte queue needs at least 92 entries; round to 128.

RAM cost is `length * item_size` plus the queue control block, so for large items queue
pointers or indices instead (see queuing by reference).

## Measuring instead of guessing
Add a debug high-water mark at the consumer:
```c
UBaseType_t used = uxQueueMessagesWaiting(q);
if (used > q_hwm) q_hwm = used;      /* log q_hwm periodically */
```
Run worst-case load (all interrupts active, flash writes, logging) and keep the length at
least 25 percent above the observed maximum. `uxQueueSpacesAvailable(q)` gives the inverse.

## Choosing block times
| Side | Typical choice | Why |
|---|---|---|
| Consumer receive | `portMAX_DELAY`, or a timeout equal to the watchdog/health period | Task sleeps until data; timeout lets it report liveness |
| Producer send (task) | Small finite (e.g. `pdMS_TO_TICKS(10)`) | Back-pressure without deadlock |
| Producer send (ISR) | Always 0 (`FromISR` cannot block) | Count drops |

Always check the return value: `errQUEUE_FULL` / `pdFALSE` on send, `pdFALSE` on receive
timeout.

```c
if (xQueueSendFromISR(q, &b, &woken) != pdPASS) {
    rx_overflow++;          /* visible counter beats a silent drop */
}
portYIELD_FROM_ISR(woken);
```

## Full-queue policy
Decide explicitly per queue:
- **Drop newest** (default with block time 0): fine for telemetry.
- **Drop oldest:** receive one item with timeout 0, then send.
- **Latest value only:** length-1 queue plus `xQueueOverwrite`.
- **Back-pressure:** producer blocks; only acceptable when the producer is a task that may wait.

## Gotchas
- `portMAX_DELAY` means "forever" only when `INCLUDE_vTaskSuspend` is 1; otherwise it is a long
  finite timeout.
- Block times are in ticks; use `pdMS_TO_TICKS` and remember it truncates (1 ms at 100 Hz is 0).
- A queue filling permanently means the consumer rate is too low; a longer queue only delays
  the failure.

## Verify
- [ ] Each queue length is justified by a burst calculation or a measured high-water mark.
- [ ] Every send/receive return value is checked; drop counters are exposed.

## Checked
2026-11-01. Confirmed against the FreeRTOS-Kernel source (tasks.c, queue.c, include/projdefs.h, include/queue.h):
`portMAX_DELAY` blocks indefinitely only when `INCLUDE_vTaskSuspend` is 1, `pdMS_TO_TICKS` is an integer
multiply-divide that truncates, `xQueueOverwrite` exists for the length-1 pattern, `uxQueueMessagesWaiting`
and `uxQueueSpacesAvailable` are queue APIs. The sizing arithmetic and the 25 percent margin are engineering
guidance, not documented limits. Nothing was removed.
Method: documentation only; no commands were run.
