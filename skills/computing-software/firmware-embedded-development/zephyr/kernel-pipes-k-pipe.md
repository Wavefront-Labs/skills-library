---
id: computing-software.firmware-embedded-development.zephyr.kernel-pipes-k-pipe
name: kernel-pipes-k-pipe
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [k-pipe, k-pipe-write, k-pipe-read, byte-stream, zephyr-data-passing, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Stream bytes between Zephyr threads with k_pipe: the 4.1+ k_pipe_write/k_pipe_read API vs the old put/get, partial transfers, timeouts, reset and close."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/data_passing/pipes.html
  - https://docs.zephyrproject.org/latest/releases/migration-guide-4.1.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/kernel.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipes (k_pipe)

A pipe is a kernel byte stream with an internal ring buffer: variable-length writes and reads,
blocking on full/empty.

## Zephyr 4.1+ API
```c
K_PIPE_DEFINE(log_pipe, 512, 4);          /* 512-byte buffer, 4-byte alignment */

/* writer */
int n = k_pipe_write(&log_pipe, data, len, K_MSEC(10));
if (n < 0) { /* -EAGAIN timeout with nothing written, -EPIPE closed, -ECANCELED reset */ }
else if (n < len) { /* partial write of n bytes: send the rest in a loop */ }

/* reader */
uint8_t buf[64];
int got = k_pipe_read(&log_pipe, buf, sizeof buf, K_FOREVER);
```
- Both calls may transfer "in whole or in part": `k_pipe_write` writes up to `len` bytes and returns the
  number written; on a full (or absent) ring buffer it blocks until space appears or the timeout
  expires. Loop on the return value until everything is sent, as the docs' producer example does.
- `k_pipe_read` returns the number of bytes read (up to `len`) and blocks while the pipe is empty.
- Errors for both: `-EAGAIN` (nothing transferred before the timeout), `-ECANCELED` (interrupted by
  `k_pipe_reset`), `-EPIPE` (closed), `-EOVERFLOW` (`len` above `INT_MAX`).
- `k_pipe_reset(&p)`: discards unread data, wakes waiters with `-ECANCELED`; the pipe stays open.
- `k_pipe_close(&p)`: wakes blocked threads with an error; further access is refused, but data
  already in the pipe stays readable until it is emptied. `k_pipe_init` reopens a closed pipe.
- Runtime init: `k_pipe_init(&p, buffer, size)`; a size of 0 with a NULL buffer gives a pipe without a
  ring buffer (direct hand-over between writer and reader).

## Pre-4.1 API (deprecated; replaced in 4.1)
```c
size_t written;
k_pipe_put(&p, data, len, &written, min_xfer, K_MSEC(10));
size_t read;
k_pipe_get(&p, buf, sizeof buf, &read, 1 /*min*/, K_FOREVER);
```
The 4.1 migration guide: `min_xfer` was removed (threshold-based partial transfers are no longer
supported) and the byte count is now the return value. `k_pipe_flush` / `k_pipe_buffer_flush` became
`k_pipe_reset`; `k_pipe_alloc_init`, `k_pipe_cleanup`, `k_pipe_read_avail` and `k_pipe_write_avail`
were removed. The new API is enabled by default when `CONFIG_MULTITHREADING` is set; `CONFIG_PIPES`
now refers to the deprecated API.

## When to use
| Need | Better choice |
|---|---|
| Fixed-size messages | `k_msgq` |
| ISR producer, thread consumer, bytes | `ring_buf` + semaphore/`k_poll_signal` |
| Variable-size thread to thread stream | `k_pipe` |
| Zero-copy large blocks | `k_fifo` of buffers |

## Gotchas
- Size the buffer for bursts; a full pipe blocks writers until the timeout.
- One pipe with many writers can interleave their bytes; frame messages or serialise writers.

## Verify
- [ ] Return values distinguish timeout, partial write, closed and reset.
- [ ] Code compiles against the API of the pinned Zephyr version (4.1 changed it).

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- `k_pipe_write` / `k_pipe_read` / `k_pipe_reset` / `k_pipe_close` / `k_pipe_init` / `K_PIPE_DEFINE` signatures and return
  codes (`include/zephyr/kernel.h`); partial transfer wording (doc: kernel/services/data_passing/pipes).
- Old-to-new API mapping, removed functions and data availability after close (doc/releases/migration-guide-4.1).
- Wrong in the draft: `k_pipe_write` was said to return only after all bytes were written (it may write in part); the
  claim that 4.1 removed a Kconfig gate was reworded to the migration guide text.
- Removed: ISR-with-`K_NO_WAIT` rule for pipes and the "copied twice" remark (no source).

Method: documentation only; no commands were run.
