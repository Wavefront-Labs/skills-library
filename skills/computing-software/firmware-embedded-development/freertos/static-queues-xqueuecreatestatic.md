---
id: computing-software.firmware-embedded-development.freertos.static-queues-xqueuecreatestatic
name: static-queues-xqueuecreatestatic
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [xqueuecreatestatic, staticqueue-t, static-allocation, queue-storage-area, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Create FreeRTOS queues with xQueueCreateStatic so no heap is used: storage sizing, StaticQueue_t lifetime, linker placement, and mixing with dynamic objects."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/04-API-references/06-Queues/02-xQueueCreateStatic
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static queues

```c
/* FreeRTOSConfig.h */
#define configSUPPORT_STATIC_ALLOCATION 1

#define CMD_QUEUE_LEN   8
typedef struct { uint8_t id; uint32_t arg; } cmd_t;

static StaticQueue_t qCmdCtrl;                                 /* control block */
static uint8_t       qCmdStorage[CMD_QUEUE_LEN * sizeof(cmd_t)];/* item storage */
static QueueHandle_t qCmd;

void app_init(void)
{
    qCmd = xQueueCreateStatic(CMD_QUEUE_LEN, sizeof(cmd_t), qCmdStorage, &qCmdCtrl);
    configASSERT(qCmd != NULL);
}
```

## Rules
- Storage must be exactly `uxQueueLength * uxItemSize` bytes, or larger. Tie both to the same
  macros so a length change cannot desynchronise them.
- Both buffers need static lifetime (file-scope `static` or global). Never use locals.
- The returned handle is just `&qCmdCtrl` cast; you still use the normal queue API.
- `vQueueDelete` on a static queue frees nothing (queue.c checks `ucStaticallyAllocated`); the memory is yours
  to reuse only after no task can reference the queue.
- For a zero-size item queue (pure signalling) pass `NULL` storage and item size 0; queue.c asserts that
  storage and item size agree.

## Why bother
- Failure moves from runtime (NULL handle when heap is low) to link time (RAM overflow).
- `size`/map file shows exact RAM per object, which certification reviews want.
- Systems with `configSUPPORT_DYNAMIC_ALLOCATION 0` can drop the heap entirely; then also
  implement `vApplicationGetIdleTaskMemory` (and the timer-task equivalent).

## Placement
Put large storage in a specific RAM region with a section attribute when the part has
several RAM banks (e.g. keep DMA-unreachable CCM RAM for control blocks only):
```c
static uint8_t qBig[64 * 32] __attribute__((section(".ram_d2")));
```
Check the linker script actually defines and zero-initialises that section.

## Related static creators
`xSemaphoreCreateBinaryStatic`, `xSemaphoreCreateMutexStatic`, `xEventGroupCreateStatic`,
`xStreamBufferCreateStatic`, `xMessageBufferCreateStatic`, `xTimerCreateStatic`,
`xQueueCreateSetStatic`. Same pattern: caller supplies a `Static*_t` and any
storage.

## Verify
- [ ] Map file shows the queue storage in the intended RAM section.
- [ ] Storage size expression references the same length and item-size macros as the call.
- [ ] Build with `configSUPPORT_DYNAMIC_ALLOCATION 0` if the goal is zero heap; it links.

## Checked
2026-11-01. Confirmed in FreeRTOS-Kernel source: queue.c (`vQueueDelete` skips freeing static queues, NULL storage
with zero item size, storage/size consistency assert), include/queue.h (`xQueueCreateStatic`, `xQueueCreateSetStatic`),
include/task.h and timers.h (`vApplicationGetIdleTaskMemory`, `vApplicationGetTimerTaskMemory`). Removed the "kernel 11"
version note. The linker-placement section is toolchain advice, not a documented claim.
Method: documentation only; no commands were run.
