---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mpm-prefork-and-worker
name: mpm-prefork-and-worker
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mpm, prefork, worker, minspareservers, minsparethreads, serverlimit]
level: practitioner
status: docs-checked
description: "Configure prefork and worker MPMs: when to choose each, spare server and thread settings, ServerLimit and ThreadLimit relations, and the sample worker config."
sources:
  - https://httpd.apache.org/docs/2.4/mod/prefork.html
  - https://httpd.apache.org/docs/2.4/mod/worker.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MPM prefork and worker
## prefork
Non-threaded: choose it for non-thread-safe libraries or per-request isolation. It is self-regulating.
```apache
LoadModule mpm_prefork_module modules/mod_mpm_prefork.so
MinSpareServers 5
MaxSpareServers 10
```
- `MinSpareServers` default 5: spawns 1, 2, 4... up to 32 per second.
- `MaxSpareServers` default 10; if set at or below MinSpareServers it becomes MinSpareServers + 1.
- `MaxRequestWorkers` should fit physical RAM to avoid swapping; over 256 may need `ServerLimit`.
- The parent starts as root to bind port 80; children use `User`/`Group`.

## worker
Hybrid process/thread: a listener hands connections to worker threads. The server keeps idle threads between `MinSpareThreads` and `MaxSpareThreads`. Max processes = `MaxRequestWorkers / ThreadsPerChild`. `ServerLimit` must be at least that; `ThreadLimit` at least `ThreadsPerChild`; changing them needs a full restart.
```
ServerLimit         16
StartServers         2
MaxRequestWorkers  150
MinSpareThreads     25
MaxSpareThreads     75
ThreadsPerChild     25
```
150 / 25 = 6 processes, within ServerLimit 16.

## Checked
2026-11-04. Confirmed against the prefork and worker MPM pages: self-regulation and RAM advice, spare-server defaults and the exponential spawn up to 32 per second, MinSpareServers + 1 adjustment, root parent with User/Group children, process arithmetic, hard limits needing a full restart, and the sample configuration. Nothing removed.
Method: documentation only; no commands were run.
