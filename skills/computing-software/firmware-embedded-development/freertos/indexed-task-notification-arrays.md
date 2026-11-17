---
id: computing-software.firmware-embedded-development.freertos.indexed-task-notification-arrays
name: indexed-task-notification-arrays
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [notification-index, configtask-notification-array-entries, xtasknotifyindexed, ultasknotifytakeindexed, xtasknotifywaitindexed, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Give a FreeRTOS task several independent notification channels with indexed notification arrays, keeping index 0 free for stream buffers and legacy APIs."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/FreeRTOS.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/tasks.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/stream_buffer.c
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/History.txt
  - https://github.com/FreeRTOS/FreeRTOS-Kernel-Book/blob/main/ch10.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Indexed task notification arrays

Before FreeRTOS V10.4.0 (September 2020) each task had **one** notification value. If a driver used it as a
binary semaphore and the application also used it for event bits, they overwrote each other.
Indexed notifications give each task an array of independent value+state pairs.

## Config
```c
#define configTASK_NOTIFICATION_ARRAY_ENTRIES 3   /* default 1; must be at least 1; 5 bytes per entry per task */
```

## Allocate indices like resources
```c
/* notify_idx.h: one table for the whole project */
#define NOTIFY_IDX_RESERVED   0   /* legacy xTaskNotify*, stream/message buffers */
#define NOTIFY_IDX_SPI_DONE   1   /* SPI driver: binary semaphore style */
#define NOTIFY_IDX_APP_EVENTS 2   /* application event bits */
```
Index 0 is what the non-indexed API uses (`xTaskNotify` = `xTaskNotifyIndexed(..., 0, ...)`),
and stream and message buffers signal tasks through index 0 by default
(`tskDEFAULT_INDEX_TO_NOTIFY`; `vStreamBufferSetStreamBufferNotificationIndex` changes it per
buffer). Don't hand index 0 to a driver unless you have changed that.

## API
```c
/* ISR: SPI DMA complete */
vTaskNotifyGiveIndexedFromISR(hTask, NOTIFY_IDX_SPI_DONE, &woken);

/* driver, in the task */
if (ulTaskNotifyTakeIndexed(NOTIFY_IDX_SPI_DONE, pdTRUE, pdMS_TO_TICKS(10)) == 0) timeout();

/* application event bits */
xTaskNotifyIndexed(hTask, NOTIFY_IDX_APP_EVENTS, EVT_BUTTON, eSetBits);
uint32_t bits;
xTaskNotifyWaitIndexed(NOTIFY_IDX_APP_EVENTS, 0, UINT32_MAX, &bits, portMAX_DELAY);
```
Housekeeping: `xTaskNotifyStateClearIndexed` clears a pending notification without reading it
(use it before starting a transfer so a stale completion doesn't satisfy the next wait), and
`ulTaskNotifyValueClearIndexed` clears bits in the notification value.

## Semantics to remember
- A task blocks on **one** index at a time. It can't wait on index 1 *or* 2; for that, use
  bits within one index or an event group.
- Indices are per task: index 1 in task A and index 1 in task B are unrelated, but sharing one
  project-wide table keeps drivers portable between tasks.
- An index at or above `configTASK_NOTIFICATION_ARRAY_ENTRIES` fails a `configASSERT` in the kernel.

## Verify
- [ ] Single index table in a header; no magic numbers at call sites.
- [ ] No driver uses index 0 if the task also uses stream/message buffers (at their default index) or the non-indexed notify APIs.
- [ ] Each driver clears its index state before starting an operation it will wait on.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: indexed notifications introduced in V10.4.0 (History.txt); configTASK_NOTIFICATION_ARRAY_ENTRIES defaults to 1 and must be at least 1 (FreeRTOS.h), RAM cost is that value times 5 bytes per task (Kernel Book 10.2.2); stream buffers default to tskDEFAULT_INDEX_TO_NOTIFY and can be changed with vStreamBufferSetStreamBufferNotificationIndex; xTaskNotifyStateClearIndexed and out-of-range index asserts (tasks.c). Removed the pending-notification claim as unconfirmed. 
Method: documentation only; no commands were run.
