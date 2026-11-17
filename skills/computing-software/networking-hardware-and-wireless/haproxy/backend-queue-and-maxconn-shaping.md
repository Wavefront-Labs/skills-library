---
id: computing-software.networking-hardware-and-wireless.haproxy.backend-queue-and-maxconn-shaping
name: backend-queue-and-maxconn-shaping
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, server-maxconn, maxqueue, timeout-queue, fullconn, http-request-set-priority]
level: practitioner
status: docs-checked
description: "Protect slow servers with server maxconn, backend fullconn, timeout queue, maxqueue and priority queues in HAProxy."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
  - https://docs.haproxy.org/3.0/management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# backend queue and maxconn shaping
A server with `maxconn` never exceeds that many concurrent connections; extra requests wait in a queue inside HAProxy rather than being pushed onto the app.

```
backend be_app
    timeout queue 5s
    fullconn 2000
    default-server maxconn 100 maxqueue 200
    server a 10.0.0.11:8080 check
    server b 10.0.0.12:8080 check
```
HAProxy keeps per-server queues and a backend (global) queue. A request pending longer than `timeout queue` is dropped with a 503 (termination flags `sQ`; if unset, `timeout queue` falls back to `timeout connect`). `maxqueue` is the most connections that may wait for one server (default 0 = unlimited); when reached, further requests are redispatched to other servers, which breaks persistence.

With `minconn` on the server, `maxconn` becomes a dynamic limit: at least `minconn`, at most `maxconn`, ramping up while the backend has fewer than `fullconn` concurrent connections. If `fullconn` is unset HAProxy uses 10% of the sum of the maxconns of the frontends that can branch to the backend.

Priority: lower values go first, and the default is 0, so to favour payments use a negative class: `http-request set-priority-class int(-1) if { path_beg /pay }` (range -2047..2047). `set-priority-offset` (range -524287..524287 ms) reorders within a class; keep `timeout queue` plus the offset under 524,287 ms.

Gotcha: long-lived connections (websockets) hold `maxconn` slots for their whole life, so keep them in a separate backend with its own limits and `timeout tunnel`.

Verify: run a burst load test and read `qcur`, `qmax` and `qtime` from `show stat` (management guide, stats columns).

## Checked
2026-11-03. Confirmed against configuration.html (`timeout queue`, `fullconn`, server `maxconn`/`minconn`/`maxqueue`, `set-priority-class`/`set-priority-offset`, termination flag Q) and management.html (`qcur`, `qmax`, `qtime` columns). Fixed: the example used `int(1)`, which gives LOWER priority than the default 0. Removed: "maxqueue makes the server look full", the persistence explanation of server queues, "1.8+ confirm", the "backend maxconn" gotcha wording, and the stats page `Q` claim.
Method: documentation only; no commands were run.
