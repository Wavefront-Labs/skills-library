---
id: computing-software.firmware-embedded-development.freertos.queuing-by-reference-vs-copy
name: queuing-by-reference-vs-copy
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [queue-by-reference, queue-by-copy, buffer-ownership, pointer-queue, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Decide between copying data into FreeRTOS queues and queuing pointers: buffer ownership rules, pool allocators, and the dangling-pointer bugs reference passing causes."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/queue.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queuing pointers vs copies

FreeRTOS queues always **copy** `uxItemSize` bytes. "By reference" means the item you copy is
a pointer.

## Decision
| Item | Use |
|---|---|
| Small items (events, sensor samples, commands) | Copy the struct |
| Large buffers (network frames, audio blocks) | Queue a pointer to a buffer from a pool |
| Variable-length bytes | Stream or message buffer instead of either |

Copying is simpler and has no ownership bugs; the copy cost grows with the item size.

## Reference passing done right
Ownership transfers with the pointer: after sending, the producer must not touch the buffer;
the consumer must return it.

```c
#define NBUF 8
static uint8_t pool[NBUF][256];
static QueueHandle_t qFree, qFull;          /* both hold uint8_t* */

void init(void) {
    qFree = xQueueCreate(NBUF, sizeof(uint8_t *));
    qFull = xQueueCreate(NBUF, sizeof(uint8_t *));
    for (int i = 0; i < NBUF; i++) { uint8_t *p = pool[i]; xQueueSend(qFree, &p, 0); }
}

void producer(void) {
    uint8_t *p;
    if (xQueueReceive(qFree, &p, pdMS_TO_TICKS(5)) == pdPASS) {
        fill(p);
        xQueueSend(qFull, &p, portMAX_DELAY);   /* ownership -> consumer */
    }
}

void consumer(void) {
    uint8_t *p;
    xQueueReceive(qFull, &p, portMAX_DELAY);
    process(p);
    xQueueSend(qFree, &p, 0);                  /* return to pool */
}
```
Note `&p`: you pass the address of the pointer variable, and the queue copies the pointer.

## Classic bugs
- Queuing the address of a **stack** buffer: the producer returns or reuses it before the
  consumer reads it.
- Queuing `&buffer` instead of `&p`, so the queue copies the first `sizeof(uint8_t *)` bytes of the data.
- Producer keeps writing into the buffer after sending (no ownership discipline).
- Pool exhaustion when a consumer path forgets to return the buffer; watch
  `uxQueueMessagesWaiting(qFree)` reach 0.
- Heap allocation per message: works but can fragment the heap over time; prefer a fixed
  pool.

## Verify
- [ ] Every queued pointer points to static or pool memory, never a stack local.
- [ ] Free-pool level is monitored and returns to `NBUF` when idle.
- [ ] Code review confirms no access to a buffer after it is sent.

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: queues copy `uxItemSize` bytes per item; `xQueueCreate`, `xQueueSend`, `xQueueReceive` and `uxQueueMessagesWaiting` exist (queue.h); stream/message buffers are separate kernel objects (FreeRTOS.h). Removed or rewritten: the 16-32 byte threshold, the critical-section memcpy claim, the heap_2/heap_4 names and the 4-byte figure.
Method: documentation only; no commands were run.
