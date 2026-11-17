---
id: computing-software.software-engineering.c.poll-and-epoll-event-loops
name: poll-and-epoll-event-loops
category: computing-software
field: software-engineering
product: c
tags: [c, epoll, poll, non-blocking-io, event-loop, level-triggered]
level: advanced
status: docs-checked
description: "Build a single-threaded event loop with poll or epoll and non-blocking sockets."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://pubs.opengroup.org/onlinepubs/9799919799/", "https://man7.org/linux/man-pages/", "https://beej.us/guide/bgnet/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Poll and epoll event loops

Goal: serve many connections without a thread per client.

- Make sockets non-blocking: `fcntl(fd, F_SETFL, fcntl(fd, F_GETFL) | O_NONBLOCK)` or `SOCK_NONBLOCK` at creation.
- `poll(struct pollfd *fds, nfds, timeout_ms)`: simple and portable. Check `revents` for `POLLIN`, `POLLOUT`, `POLLHUP`, `POLLERR`.
- Linux `epoll`: `epoll_create1(0)`, `epoll_ctl(ep, EPOLL_CTL_ADD, fd, &ev)`, `epoll_wait`. Level-triggered (default) is simplest; edge-triggered (`EPOLLET`) requires reading/writing until `EAGAIN`.
- Per-connection state in a struct stored in `ev.data.ptr`; write buffers queue output and enable `EPOLLOUT` only while data is pending.
- Remove fds from the set before `close`; handle `EPOLLRDHUP`/0-byte read as disconnect.
- Accept in a loop until `EAGAIN` when edge-triggered. Add timeouts for idle connections.

Verify: open several hundred `nc` connections in a loop and confirm CPU stays low and each connection echoes correctly.

## Checked

2026-11-02. Confirmed in epoll(7), epoll_create(2), epoll_ctl(2), poll(2), open(2), socket(2): `epoll_create1`, `EPOLL_CTL_ADD`, `EPOLLET`, `EPOLLOUT`, `EPOLLRDHUP`, `O_NONBLOCK`, `SOCK_NONBLOCK`. Removed: the poll linear-cost claim and the kqueue remark.

Method: documentation only; no commands were run.
