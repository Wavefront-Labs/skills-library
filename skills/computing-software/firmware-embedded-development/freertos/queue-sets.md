---
id: computing-software.firmware-embedded-development.freertos.queue-sets
name: queue-sets
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [queue-set, xqueuecreateset, xqueueaddtoset, xqueueselectfromset, multi-queue-wait, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Block one FreeRTOS task on several queues and semaphores at once with queue sets: sizing, the read-exactly-once rule, and when an event group or notification is better."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/queue.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/FreeRTOS.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue sets

**Goal:** a task that waits on, say, a UART RX queue, a command queue and a binary semaphore
together, without polling.

## Setup
```c
/* configUSE_QUEUE_SETS 1 */
#define RX_LEN  16
#define CMD_LEN 4
QueueHandle_t     qRx  = xQueueCreate(RX_LEN, sizeof(uint8_t));
QueueHandle_t     qCmd = xQueueCreate(CMD_LEN, sizeof(cmd_t));
SemaphoreHandle_t sTick = xSemaphoreCreateBinary();

/* Set length: queue.h says it should be the combined length of all members (binary semaphore = 1). */
QueueSetHandle_t set = xQueueCreateSet(RX_LEN + CMD_LEN + 1);
xQueueAddToSet(qRx, set);
xQueueAddToSet(qCmd, set);
xQueueAddToSet(sTick, set);
```

## Consuming
```c
for (;;) {
    QueueSetMemberHandle_t m = xQueueSelectFromSet(set, portMAX_DELAY);
    if (m == qRx)        { uint8_t b; xQueueReceive(qRx, &b, 0); handle_byte(b); }
    else if (m == qCmd)  { cmd_t c;  xQueueReceive(qCmd, &c, 0); handle_cmd(&c); }
    else if (m == sTick) { xSemaphoreTake(sTick, 0); handle_tick(); }
}
```
Rules:
- Each handle returned **must** be read exactly once, with timeout 0. The set holds one entry
  per item posted. Skipping a read leaves the set and queue out of step; reading without a
  select steals an item whose set entry is still pending.
- Don't read members anywhere except right after selecting them.
- Remove a member with `xQueueRemoveFromSet`.
- `xQueueSelectFromSetFromISR` exists for the rare ISR consumer.

## Gotchas
- Undersized set: posts to members fail even though the member queue has space. Always size
  with the sum formula and recompute when a member's length changes.
- Mutexes in a set: blocking on the set does **not** cause priority inheritance. Don't add mutexes.

## Simpler alternatives first
| Need | Use |
|---|---|
| Wake on any of several events, no payload | event group or notification bits |
| Several producers, one consumer, payloads | one queue of a tagged union `{type; union{...}}` |
| Existing driver APIs that each give you a queue | queue set |

The single tagged-union queue is usually smaller, faster and keeps ordering across sources,
which a queue set does not.

## Verify
- [ ] Set length computed from member lengths in code (not a magic number).
- [ ] Flood all members at once; no send fails while member queues have space.
- [ ] Every `xQueueSelectFromSet` branch reads its member with timeout 0.

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: `xQueueCreateSet`, `xQueueAddToSet`, `xQueueSelectFromSet`, `xQueueRemoveFromSet` exist and `configUSE_QUEUE_SETS` defaults to 0; set length should cover all member events; blocking on a set containing a mutex gives no priority inheritance; counting semaphores with high max count should not be added (queue.h, FreeRTOS.h). Removed or rewritten: the 'members must be empty', 'one set only' and 'last resort' claims, and the guarantee wording on set length.
Method: documentation only; no commands were run.
