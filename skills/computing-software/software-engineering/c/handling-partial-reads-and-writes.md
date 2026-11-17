---
id: computing-software.software-engineering.c.handling-partial-reads-and-writes
name: handling-partial-reads-and-writes
category: computing-software
field: software-engineering
product: c
tags: [c, partial-io, send-all, recv-framing, eintr, length-prefix]
level: practitioner
status: docs-checked
description: "Loop over partial send/recv, handle EINTR and frame messages on the TCP byte stream."
sources: ["https://man7.org/linux/man-pages/man2/send.2.html", "https://man7.org/linux/man-pages/man2/recv.2.html", "https://man7.org/linux/man-pages/man2/write.2.html", "https://man7.org/linux/man-pages/man2/shutdown.2.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling partial reads and writes

Goal: reliable message exchange over a stream with no message boundaries.

- `send`/`write` may transmit fewer bytes than requested; loop until all sent: advance the pointer by the returned count, retry on `EINTR`, treat `EAGAIN`/`EWOULDBLOCK` as "wait for writability" on non-blocking sockets.
- `recv` returns 0 on orderly peer shutdown, -1 on error; it returns whatever is available, not a whole message. Write a `read_exact(fd, buf, n)` helper.
- Framing: length-prefix (fixed-size big-endian header then payload) or delimiter. Validate the length against a maximum before allocating (otherwise remote memory exhaustion).
- Use `MSG_NOSIGNAL` on `send` (Linux) or ignore `SIGPIPE` to avoid dying on a closed peer.
- `shutdown(fd, SHUT_WR)` signals EOF while still reading the reply.
- Never assume one `send` equals one `recv`.

Verify: test with a peer that sends one byte at a time and with a 10 MB payload.

## Checked

- Date: 2026-11-02
- Confirmed in man7: write(2) may transfer fewer bytes than requested; recv(2) returns 0 on orderly shutdown and can fail with EINTR; send(2) EAGAIN/EWOULDBLOCK on non-blocking sockets and `MSG_NOSIGNAL` (since Linux 2.2); shutdown(2) `SHUT_WR`. Removed: the claim that `close` alone may reset the connection with unread data.
Method: documentation only; no commands were run.
