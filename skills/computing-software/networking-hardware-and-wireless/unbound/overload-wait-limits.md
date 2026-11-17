---
id: computing-software.networking-hardware-and-wireless.unbound.overload-wait-limits
name: overload-wait-limits
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, wait-limit, jostle-timeout, discard-timeout, sock-queue-timeout, overload]
level: sme
status: docs-checked
description: "Keep Unbound responsive under load: wait-limit per IP and netblock, jostle-timeout, discard-timeout, sock-queue-timeout and the counters that show drops."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# overload and wait limits
- `num-queries-per-thread` (2048 libevent, 512 minievent, 24 windows): queries a thread services at once before dropping new ones.
- `jostle-timeout` (200 ms): how long a waiting query may run before being replaced when the server is busy.
- `discard-timeout` (1900 ms): recursion requests older than this are dropped; 0 disables.
- `wait-limit` (1000): maximum replies waiting for recursion per IP; 0 disables. `wait-limit-cookie` (10000) applies to clients with a valid DNS Cookie.
- `wait-limit-netblock` and `wait-limit-cookie-netblock`: per-netblock overrides; -1 disables for that netblock.
- `sock-queue-timeout` (0, disabled): drop UDP queries that waited in the socket buffer longer than this many seconds (Linux and FreeBSD).

Counters: `num.queries_discard_timeout`, `num.queries_wait_limit`, `num.queries_replyaddr_limit`, `num.queries_timed_out`, `requestlist.overwritten` (jostle replacement) and `requestlist.exceeded` (new query dropped).

`unbound-control dump_requestlist` shows in-progress queries for the first thread; `flush_requestlist` drops them.

## Checked
2026-11-04. Confirmed against the unbound.conf manual and unbound-control manual: num-queries-per-thread, jostle-timeout, discard-timeout, wait-limit options and defaults, sock-queue-timeout, and dump_requestlist. Nothing removed.
Method: documentation only; no commands were run.
