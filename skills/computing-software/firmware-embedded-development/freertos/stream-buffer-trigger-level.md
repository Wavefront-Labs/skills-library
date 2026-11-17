---
id: computing-software.firmware-embedded-development.freertos.stream-buffer-trigger-level
name: stream-buffer-trigger-level
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [trigger-level, xstreambuffersettriggerlevel, stream-buffer, xstreambuffercreate, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Tune a FreeRTOS stream buffer trigger level to trade wake-up rate against latency, and handle partial reads, timeouts, and the single-reader single-writer rule."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Stream-buffers/01-xStreamBufferCreate
  - https://www.freertos.org/Documentation/02-Kernel/04-API-references/09-Stream-buffers/13-xStreamBufferSetTriggerLevel
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stream buffer trigger level

```c
StreamBufferHandle_t sb = xStreamBufferCreate(512 /*bytes*/, 32 /*trigger level*/);
```
The trigger level is how many bytes must be in the buffer before a reader blocked in
`xStreamBufferReceive` is woken. It does **not** limit how many bytes a read returns.

## Behaviour
- Reader blocks with `xStreamBufferReceive(sb, buf, 64, pdMS_TO_TICKS(20))`.
- It wakes when either: bytes available >= trigger level, **or** the block time expires.
- On return it gets `min(available, 64)` bytes, possibly fewer than the trigger level (after a
  timeout) or more.
- Trigger level 1 (the minimum; 0 is treated as 1) wakes on every byte.

## Choosing the level
| Data | Level | Block time |
|---|---|---|
| Interactive console | 1 | `portMAX_DELAY` |
| Fixed-size frames (e.g. 48-byte sensor packets) | frame size | a few frame periods |
| Bulk UART/DMA logging | large chunk (64-256) | max acceptable latency, e.g. 10-50 ms |

The block time acts as a flush timer: a partial chunk is still delivered when data stops
arriving, so a large trigger level doesn't strand the tail of a message.

```c
for (;;) {
    size_t n = xStreamBufferReceive(sb, buf, sizeof buf, pdMS_TO_TICKS(20));
    if (n) write_to_flash(buf, n);       /* n may be anything from 1 to sizeof buf */
}
```
Change it at runtime with `xStreamBufferSetTriggerLevel(sb, lvl)`; returns `pdFALSE` if
`lvl` is not smaller than the buffer size (0 is treated as 1).

## Rules
- Exactly one writer and one reader (task or ISR) at a time, by design; there is no internal
  lock. Multiple writers need a mutex around sends (and senders must not block inside an
  ISR critical section), or one gatekeeper writer.
- Writers and readers from ISRs use the `FromISR` variants with block time 0.
- Reading is a copy; for zero-copy DMA, use a ring buffer of DMA blocks instead.
- Stream buffers use a task notification index internally (`tskDEFAULT_INDEX_TO_NOTIFY` by
  default; change it with `vStreamBufferSetStreamBufferNotificationIndex`). Don't use that
  index for anything else on the reader or writer task.

## Verify
- [ ] Wake rate measured (trace or counter) matches the expected burst size.
- [ ] Tail of a message arrives within the block time when input stops.
- [ ] Only one writer and one reader touch each stream buffer.

## Checked

2026-11-01. Confirmed against FreeRTOS-Kernel stream_buffer.c: trigger level 0 becomes 1 in create and in `xStreamBufferSetTriggerLevel`; set-trigger-level returns pdFALSE unless the level is smaller than the buffer length; the default notification index and its setter. Corrected the set-trigger-level limit and removed an invented config macro.
Method: documentation only; no commands were run.
