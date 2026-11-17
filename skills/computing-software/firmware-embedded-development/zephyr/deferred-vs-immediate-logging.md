---
id: computing-software.firmware-embedded-development.zephyr.deferred-vs-immediate-logging
name: deferred-vs-immediate-logging
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-logging, log-mode-deferred, log-mode-immediate, log-buffer-size, log-process-thread, dropped-messages, log-panic, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Choose Zephyr deferred vs immediate logging, size the log buffer and processing thread, deal with dropped messages, and make logs flush on panic."
sources:
  - https://docs.zephyrproject.org/latest/services/logging/index.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/logging/Kconfig.mode
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/logging/Kconfig.processing
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/kernel/fatal.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deferred vs immediate logging (Zephyr)

**Goal:** logging that doesn't wreck timing in normal operation and still gets the last
messages out when the system crashes.

## The modes
| Mode | Behaviour | Use |
|---|---|---|
| `CONFIG_LOG_MODE_DEFERRED` (default) | messages are buffered and processed later, by a logging thread by default; least impact on the application | production, timing-sensitive code |
| `CONFIG_LOG_MODE_IMMEDIATE` | processed in the context of the call; backends must support exclusive access because one log call can interrupt another | debugging crashes early in boot, ordering-sensitive debug |
| `CONFIG_LOG_MODE_MINIMAL` | printk-based, build-time filtering only (no runtime filtering), no timestamps | tiny targets |
Immediate mode does the formatting and output in the caller, for example in a high-priority
interrupt. At 115200 baud an 80-character line takes about 7 ms to send (10 bits per character),
which is why it suits debugging only. The default mode is `IMMEDIATE` on the POSIX architecture.

## Sizing deferred mode
- `CONFIG_LOG_BUFFER_SIZE` (default 1024 bytes): holds pending messages. Bursts beyond it cause
  messages to be dropped according to the overflow policy below.
- `CONFIG_LOG_PROCESS_THREAD_CUSTOM_PRIORITY` with `CONFIG_LOG_PROCESS_THREAD_PRIORITY` (default
  priority is `K_LOWEST_APPLICATION_THREAD_PRIO`), `CONFIG_LOG_PROCESS_THREAD_SLEEP_MS` (default
  1000) and `CONFIG_LOG_PROCESS_TRIGGER_THRESHOLD` (default 10 buffered messages) control how
  quickly the internal thread drains it.
- `CONFIG_LOG_MODE_OVERFLOW` (default y) drops the oldest message when there is no space for a
  new one; when disabled, the current message is dropped.
- If drops persist: raise the buffer, lower verbosity, or use a faster backend (RTT instead of
  UART).
- The backend's bandwidth is the real limit: average log rate must be below what the UART/RTT
  can carry.

## Panic and crash
The default fatal error handler calls `LOG_PANIC()` (`log_panic()`): all active backends are
notified of panic mode, buffered messages are flushed, and from then on logs are processed in a
blocking way, so the last lines before a crash appear. Make sure your backend handles the panic
notification. You can call `log_panic()` yourself before an intentional reset.

## Ordering
Each message carries a timestamp (from `k_cycle_get_32()`/`k_cycle_get()` unless the application
provides a timestamp function). `printk()` and logging compete for the same output and can
interleave; `CONFIG_LOG_PRINTK` (default y when `PRINTK` is enabled) redirects printk to the
logging subsystem as level 0 messages that cannot be disabled, so logging manages the output.
In deferred mode printk output is then delayed until the logging thread processes it.

## Verify
- [ ] Burst test (100 log lines from a loop) shows either no drops or the intended overflow policy.
- [ ] Forced fault prints the final log lines before the fault dump.

## Checked

Checked 2026-10-25 against the Zephyr source (main, post-4.4; latest release v4.4.2): doc/services/logging/index.rst, subsys/logging/Kconfig.mode, Kconfig.processing, include/zephyr/logging/log_ctrl.h and kernel/fatal.c.
Confirmed: `CONFIG_LOG_MODE_DEFERRED` (default; IMMEDIATE is the POSIX default), `_IMMEDIATE`, `_MINIMAL` semantics; `CONFIG_LOG_BUFFER_SIZE` default 1024; `LOG_PROCESS_THREAD` options and defaults (sleep 1000 ms, threshold 10, lowest application priority); `CONFIG_LOG_MODE_OVERFLOW` default y; `log_panic()`/`LOG_PANIC()` behaviour and the call in the default fatal error handler; timestamping; `CONFIG_LOG_PRINTK` default y and its effect.

Method: documentation only; no commands were run.
