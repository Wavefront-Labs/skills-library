---
id: computing-software.firmware-embedded-development.freertos.mailbox-with-xqueueoverwrite
name: mailbox-with-xqueueoverwrite
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [queue-mailbox, xqueueoverwrite, xqueuepeek, latest-value, length-one-queue, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Publish a latest-value mailbox in FreeRTOS with a length-1 queue, xQueueOverwrite and xQueuePeek, so readers always get the newest sample and writers never block."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/queue.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/queue.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mailbox with xQueueOverwrite

**Goal:** share "the current value" (latest sensor reading, current setpoint, system mode)
between tasks. Readers want the newest value, not a backlog, and the writer must never block.

## Pattern
```c
typedef struct { TickType_t ts; float temp_c; } sample_t;
static QueueHandle_t mbox;

void init(void) { mbox = xQueueCreate(1, sizeof(sample_t)); }  /* length MUST be 1 */

/* writer (task) */
sample_t s = { xTaskGetTickCount(), read_temp() };
xQueueOverwrite(mbox, &s);                      /* never blocks, always succeeds */

/* writer (ISR) */
BaseType_t woken = pdFALSE;
xQueueOverwriteFromISR(mbox, &s, &woken);
portYIELD_FROM_ISR(woken);

/* readers: peek leaves the value for other readers */
sample_t cur;
if (xQueuePeek(mbox, &cur, pdMS_TO_TICKS(100)) == pdTRUE) { use(&cur); }
```

## Semantics
- `xQueueOverwrite` is only for queues of length one (queue.c asserts this). It overwrites the
  held value if the queue is already full.
- `xQueuePeek` copies without removing, so any number of readers see the same value and it
  stays until overwritten. Use `xQueueReceive` instead if the value should be consumed once
  ("new data" flag behaviour).
- A blocked peek wakes when the first value arrives, so readers can wait for initial data.
- Items are queued by copy, so readers get a consistent copy of a multi-word struct rather than
  a pointer to shared data. That is the advantage over a shared global.

## Staleness
The mailbox holds the last value forever. Put a timestamp in the struct and have readers
reject old data:
```c
if (xTaskGetTickCount() - cur.ts > pdMS_TO_TICKS(500)) { sensor_fault(); }
```

## When not to use it
- Every sample matters (logging, counting): use a normal queue or stream buffer.
- One reader that only needs a 32-bit value: a task notification with `eSetValueWithOverwrite`.
- Large structs at high rate: copy cost is paid twice per transfer. Use a double buffer
  with a pointer mailbox instead.

## Verify
- [ ] Queue created with length 1 (assert on create).
- [ ] Writer at high rate, slow reader: reader always sees a recent timestamp and never blocks the writer.
- [ ] Staleness check fires when the writer is stopped.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: xQueueOverwrite is only for queues of length one and overwrites a full queue (queue.h); queue.c asserts length one for queueOVERWRITE sends; xQueuePeek does not remove the item; eSetValueWithOverwrite is an eNotifyAction (task.h). Removed the critical-section and overhead claims. 
Method: documentation only; no commands were run.
