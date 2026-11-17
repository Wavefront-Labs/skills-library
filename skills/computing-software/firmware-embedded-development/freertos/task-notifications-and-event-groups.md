---
id: computing-software.firmware-embedded-development.freertos.task-notifications-and-event-groups
name: task-notifications-and-event-groups
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos, task-notification, xtasknotify, xtasknotifywait, ultasknotifytake, event-group, xeventgroupsetbits, xeventgroupwaitbits, stream-buffer, message-buffer, one-to-one-signaling, one-to-many-signaling, lightweight-ipc, firmware-embedded-development]
level: advanced
status: draft
description: "Pick the cheapest FreeRTOS IPC primitive: task notifications as a lightweight queue/semaphore swap, event groups for many-to-one condition waits, stream/message buffers for byte streams."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-RTOS-task-notifications/01-Task-notifications
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/08-Event-groups/01-RTOS-event-groups
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FreeRTOS task notifications and event groups

**Goal:** pick the lightest IPC primitive that correctly expresses the
signaling pattern, instead of defaulting to a queue (covered for the
general case in
`computing-software.firmware-embedded-development.freertos.task-and-queue-design`)
for every one-to-one wakeup.

## Task notifications: when a queue is overkill
Every task has one built-in 32-bit notification value, no separate kernel
object to create. For a single producer signaling a single consumer task with
no payload (or a small value that fits in 32 bits), this is cheaper in RAM and
faster than a queue or binary semaphore:
```c
// producer (can be an ISR): xTaskNotifyFromISR(handle, 0, eNoAction, &woken);
// consumer: ulTaskNotifyTake(pdTRUE, portMAX_DELAY);  // binary-semaphore style
// or: xTaskNotifyWait(0, 0xFFFFFFFF, &value, portMAX_DELAY); // value/bitmask style
```
`eIncrement`/`ulTaskNotifyTake` gives counting-semaphore-like behavior;
`eSetBits`/`xTaskNotifyWait` lets the value act as an event-bits register for
exactly one task (cheaper than an event group if only one task needs the
bits). **The limitation that matters**: a task has exactly one notification
slot — if two independent producers need to signal the same task for two
different reasons without clobbering each other's pending value, use
`eSetBits` with distinct bit patterns (each producer ORs in its own bit) and
have the consumer mask-check which bits are set, rather than two producers
racing to overwrite a single scalar.

## Event groups: many-to-one or many-to-many condition waits
`xEventGroupWaitBits(group, bitsToWaitFor, clearOnExit, waitForAllBits, timeout)`
lets one or more tasks block until a particular combination of bits is set —
e.g. "proceed once both Wi-Fi is connected AND NVS config is loaded", which
needs two independent setters and one (or more) waiters: naturally an event
group, not a notification (which only has one slot per task, not a shared
settable register multiple tasks can both set and wait on). `waitForAllBits`
(AND) vs clearing on exit matters: if `clearOnExit=pdTRUE` and multiple tasks
wait on the same bits, the first to wake clears them for everyone else still
waiting — a common bug when porting code written assuming only one waiter.

## Stream/message buffers: byte-stream or variable-length-message IPC
When the payload is a continuous byte stream (e.g. UART RX bytes) rather than
discrete fixed-size items, a **stream buffer** (`xStreamBufferSend`/`Receive`)
is the right primitive — a queue of `uint8_t` items works but has much higher
per-byte overhead. For variable-length discrete messages (not a continuous
stream, but not fixed-size either), a **message buffer** (built on stream
buffers) preserves message boundaries. Both are single-reader/single-writer
by design — a shared stream buffer with multiple writers calling
`xStreamBufferSend` needs external serialization (a mutex) despite being
otherwise ISR-safe for the single-writer case.

## Choosing quickly
One producer → one consumer, no payload or small value: **notification**.
One or more setters → one or more waiters on a condition made of several
independent flags: **event group**. Continuous bytes or variable-length
messages, single writer/reader: **stream/message buffer**. Anything needing
multiple independent producers queuing discrete fixed-size items for one or
more consumers: **queue** (the general-purpose default).

## Verify
- [ ] If using notifications, confirmed only one producer-pattern per task's single notification slot, or bit-masked correctly if more than one.
- [ ] Event group `clearOnExit` behavior checked against how many tasks actually wait on the same bits.
- [ ] Stream/message buffer writer count matches the primitive's single-writer assumption, or is externally serialized.
- [ ] Measured (not assumed) that the chosen primitive's RAM/latency cost is actually lower than the queue-based alternative it replaced, for at least one hot path.
