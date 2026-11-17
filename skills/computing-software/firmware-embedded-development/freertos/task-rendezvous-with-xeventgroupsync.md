---
id: computing-software.firmware-embedded-development.freertos.task-rendezvous-with-xeventgroupsync
name: task-rendezvous-with-xeventgroupsync
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [xeventgroupsync, task-rendezvous, barrier-synchronisation, event-group, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Synchronise several FreeRTOS tasks at a barrier with xEventGroupSync: bit allocation, why separate set-then-wait races, timeouts, and repeating rendezvous cycles."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/08-xEventGroupSync
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/06-Event-groups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task rendezvous with xEventGroupSync

**Goal:** N tasks each reach a point (e.g. "my peripheral is initialised", "my half of the frame
is processed") and none proceeds until all have arrived.

```c
#define SYNC_SENSOR  (1u << 0)
#define SYNC_RADIO   (1u << 1)
#define SYNC_STORAGE (1u << 2)
#define SYNC_ALL     (SYNC_SENSOR | SYNC_RADIO | SYNC_STORAGE)

static EventGroupHandle_t egSync;   /* created before the tasks run */

void vSensorTask(void *pv) {
    sensor_init();
    EventBits_t b = xEventGroupSync(egSync, SYNC_SENSOR, SYNC_ALL, pdMS_TO_TICKS(2000));
    if ((b & SYNC_ALL) != SYNC_ALL) {
        report_init_timeout(b);     /* b shows who did NOT arrive */
    }
    for (;;) { /* normal operation */ }
}
```
Each task sets its own bit and waits for all of them in one atomic call. When the last task
arrives, every waiter unblocks and the kernel **clears the sync bits automatically**, so the
same bits can be reused for the next cycle.

## Why not set then wait
```c
xEventGroupSetBits(eg, MY_BIT);                         /* last task sets bit...        */
xEventGroupWaitBits(eg, ALL, pdTRUE, pdTRUE, t);       /* ...and clears ALL on exit     */
```
With two separate calls, the first task to unblock clears the bits before the others observe
them, and they wait forever. `xEventGroupSync` performs set-and-wait atomically.

## Repeating barrier
For lock-step processing loops, call `xEventGroupSync` at the end of every iteration. Because
bits auto-clear on success, no extra reset is needed. On timeout the bits that were set are
**not** cleared; clear them yourself (`xEventGroupClearBits`) before retrying, or the next cycle
starts with stale arrivals.

## Constraints
- Not callable from ISRs (it blocks).
- Usable bits: 24 when `TickType_t` is 32-bit (top 8 bits are kernel-reserved); 8 with 16-bit
  ticks. On 64-bit tick builds, 56.
- Each participant needs a distinct bit; the waited mask must equal the union of participants.
- Event group operations from tasks run with the scheduler suspended, so they are not
  deterministic in the number of waiters; avoid huge numbers of participants.

## Verify
- [ ] Bit definitions in one header; the "all" mask derived from them.
- [ ] Timeout path logs the missing bits and clears partial arrivals.
- [ ] Repeat the rendezvous thousands of times under load without a hang.

## Checked

2026-11-01. Confirmed against FreeRTOS-Kernel include/event_groups.h and event_groups.c: control bytes `eventEVENT_BITS_CONTROL_BYTES` reserve the top 8 bits (usable 8, 24 or 56 bits for 16, 32 or 64-bit event bits) and the bit-argument asserts. Nothing removed.
Method: documentation only; no commands were run.
