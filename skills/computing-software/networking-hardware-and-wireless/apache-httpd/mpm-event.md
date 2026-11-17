---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mpm-event
name: mpm-event
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mpm, event, asyncrequestworkerfactor, keepalive, maxrequestworkers, threads]
level: practitioner
status: docs-checked
description: "Understand mpm_event: listener thread and async keep-alive, AsyncRequestWorkerFactor, connection capacity formulas, graceful restart behaviour and limitations."
sources:
  - https://httpd.apache.org/docs/2.4/mod/event.html
  - https://httpd.apache.org/docs/2.4/mod/mpm_common.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MPM event
A hybrid multi-process, multi-threaded model like worker, but each process has a listener thread that also watches keep-alive and finished sockets, so workers are not tied up waiting. It uses non-blocking sockets (epoll, kqueue, event ports) and needs no `mpm-accept` mutex.

## Async handling
After a response the listener waits for the next request and closes the socket at `KeepAliveTimeout`. Full TCP send buffers hand the socket to the listener. Lingering closes go to workers; from 2.4.28 timeouts do too.

## AsyncRequestWorkerFactor
Default 2 (may be non-integer). A process accepts a new connection while open connections are below `ThreadsPerChild + (factor x idle workers)`.

## Capacity
- Active processes = `MaxRequestWorkers / ThreadsPerChild`; `ServerLimit` caps total including gracefully stopping ones.
- Max connections ~ `(ThreadsPerChild + factor x idle_workers) x ServerLimit`; all idle: `(factor + 1) x MaxRequestWorkers`.
- Example: ThreadsPerChild=10, ServerLimit=4, MaxRequestWorkers=40, factor 2 gives 120 with all workers idle (72 with an average of 4 idle workers per process).
- `MaxRequestWorkers` must be a multiple of `ThreadsPerChild`.

## Graceful (2.4.24+)
Old processes may use all scoreboard slots; stopping processes close keep-alive connections; mod_status shows "Yes (old gen)".

## Limits
Filters incompatible with event make it fall back to worker behaviour. Output filters needing the whole body (FCGI, CGI, proxy) hold a thread until sent. It needs APR atomic compare-and-swap.

## Checked
2026-11-04. Confirmed against the event MPM page: keep-alive, writing and closing handling (2.4.28 timeouts), AsyncRequestWorkerFactor default and formulas, graceful-termination changes from 2.4.24 and the "Yes (old gen)" status, limitations and requirements. Clarified the worked example (120 all idle, 72 with 4 idle).
Method: documentation only; no commands were run.
