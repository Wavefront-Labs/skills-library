---
id: computing-software.firmware-embedded-development.bare-metal-programming.non-blocking-log-ring-buffer
name: non-blocking-log-ring-buffer
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [log-ring-buffer, semihosting, non-blocking-logging, isr-safe-logging, drop-counter, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Make logging non-blocking: queue messages in a RAM ring buffer, drain them to UART or RTT from the idle loop, count dropped messages, and flush on panic."
sources:
  - https://docs.zephyrproject.org/latest/services/logging/index.html
  - https://www.segger.com/products/debug-probes/j-link/technology/about-real-time-transfer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Non-blocking log ring buffer

Formatting and sending a message from the calling context is slow. At 115200 baud with 10 bit times per
character (8N1) a UART needs about 87 us per character, so a 60-character line blocks for about 5 ms
(derived arithmetic). Zephyr's logging documentation states the principle: deferred logging reduces the time
needed to log a message by moving time-consuming operations to a known context. Queue to RAM, transmit later.

## Zephyr's model as the reference design
- A fast **frontend** does immediate filtering and queueing; **backends** run later, format the message and
  send it to a destination such as UART, RTT or BLE.
- Deferred mode and immediate (synchronous) mode are both available; deferred uses a circular packet buffer
  whose size is configurable (`CONFIG_LOG_BUFFER_SIZE`).
- When a new message cannot be allocated, the overflow option discards the oldest messages
  (`CONFIG_LOG_MODE_OVERFLOW`); otherwise a thread can optionally block for a timeout
  (`CONFIG_LOG_BLOCK_IN_THREAD`). The design choice is therefore drop-oldest, drop-new or block.
- Processing can run in a dedicated thread woken when a threshold number of messages is buffered.
- Compile-time filtering by module and severity removes logs from the image, with independent runtime
  filtering per backend; severities are error, warning, info and debug. Rate-limited macros prevent flooding.
- Timestamps come from a user-provided function and can be 32 or 64 bits.
- In an error condition where the scheduler and interrupts can no longer be relied on, Zephyr's `log_panic()`
  notifies the backends and flushes all buffered messages, after which logs are processed in blocking mode.

## Bare-metal sketch
```c
#define LOG_BUF_SZ 4096u                     /* power of two */
static char     s_buf[LOG_BUF_SZ];
static volatile uint32_t s_head, s_tail;    /* free-running indices */
static volatile uint32_t s_dropped;

void log_write(const char *fmt, ...) {
    char line[128];
    va_list ap; va_start(ap, fmt);
    int n = vsnprintf(line, sizeof line, fmt, ap);   /* format outside the critical section */
    va_end(ap);
    if (n <= 0) return;
    if ((size_t)n >= sizeof line) n = sizeof line - 1;

    uint32_t key = irq_save();
    if (LOG_BUF_SZ - (s_head - s_tail) < (uint32_t)n) { s_dropped++; irq_restore(key); return; }
    for (int i = 0; i < n; i++) s_buf[(s_head + i) & (LOG_BUF_SZ - 1)] = line[i];
    s_head += n;
    irq_restore(key);
}
```
This is the skill's own illustration of drop-new with a drop counter (keeps the oldest context); report
`s_dropped` when space returns. `irq_save` and `irq_restore` are placeholders for your critical-section
primitives. The drain side (idle loop or low-priority task copying contiguous chunks to a UART DMA or RTT
and then advancing `s_tail`) is not covered by the sources.

## SEGGER RTT as the drain
- RTT sends target output to the host through the debug probe's background memory access, with SEGGER
  stating that it does not affect the target's real-time behaviour. It needs no extra pin and works on
  Cortex-M and RX targets with a J-Link.
- It uses a control block in target RAM that holds an ID, so J-Link can find it, and a ring buffer per
  channel; up (to host) and down (to target) buffers are configured separately, with channel 0 for terminal
  output and input and channel 1 usable for logging data.
- SEGGER gives the footprint as about 500 bytes of ROM, 24 bytes fixed plus (24 + buffer size) bytes per
  channel of RAM, with a recommended 1 KB for up channels. Its `SEGGER_RTT_Printf()` needs no heap and only a
  configurable amount of stack, and read and write can be made task-safe with lock and unlock routines.
- For RAM-only applications SEGGER notes J-Link can find the control block in the init section; set
  `SEGGER_RTT_IN_RAM` to 1 and call `SEGGER_RTT_Init()` first.

## Verify
- [ ] Logging 1000 lines in a burst never stalls the main loop longer than the format time (GPIO timing).
- [ ] Drop counter increments under overload and is reported.

## Checked
Checked 2026-11-09 against the Zephyr logging documentation and the SEGGER RTT technology page (searched for
and read the deferred logging, overflow, panic, buffer and footprint sections). The Memfault source returned
404 and was dropped. Removed: newlib reentrancy and mpaland/eyalroz printf advice, the `.noinit` crash-dump
recipe and its verify step, and the DMA transfer-complete drain advice, none of which a page read confirms.
Method: docs-checked 2026-11-09 against the Zephyr logging docs and the SEGGER RTT page.
