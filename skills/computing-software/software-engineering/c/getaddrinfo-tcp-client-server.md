---
id: computing-software.software-engineering.c.getaddrinfo-tcp-client-server
name: getaddrinfo-tcp-client-server
category: computing-software
field: software-engineering
product: c
tags: [c, c-sockets, getaddrinfo, tcp-client, tcp-server, ipv6-dual-stack, so-reuseaddr]
level: practitioner
status: docs-checked
description: "Write protocol-independent TCP clients and servers with getaddrinfo, bind, listen and accept."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://pubs.opengroup.org/onlinepubs/9799919799/", "https://man7.org/linux/man-pages/", "https://beej.us/guide/bgnet/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Getaddrinfo tcp client server

Goal: IPv4/IPv6-agnostic socket code with correct setup and cleanup.

- Client: `getaddrinfo(host, port, &hints, &res)` with `hints.ai_socktype = SOCK_STREAM`, `hints.ai_family = AF_UNSPEC`; loop the results trying `socket` then `connect` until one works; `freeaddrinfo(res)`. Report errors with `gai_strerror(rc)` (not errno).
- Server: `hints.ai_flags = AI_PASSIVE`; `socket`, set `SO_REUSEADDR` (`setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one)`) before `bind` (see socket(7) for the port-reuse rules); `listen(fd, backlog)`; `accept` in a loop, closing the connection fd per client.
- Use `sockaddr_storage` for address buffers; `getnameinfo` with `NI_NUMERICHOST` for printing.
- Set timeouts (`SO_RCVTIMEO`, `SO_SNDTIMEO`) or use `poll` to avoid infinite blocking.

Verify: run the server, then `nc localhost <port>` and `curl` to it; check with `ss -ltnp`.

## Checked

2026-11-02. Confirmed in getaddrinfo(3), getnameinfo(3), accept(2), socket(7): `gai_strerror`, `AI_PASSIVE`, `freeaddrinfo`, `NI_NUMERICHOST`, `sockaddr_storage`, `SO_REUSEADDR`, `SO_RCVTIMEO`. Removed: the `IPV6_V6ONLY` dual-stack bullet, the Windows Winsock bullet and the TIME_WAIT claim (not stated in the fetched pages).

Method: documentation only; no commands were run.
