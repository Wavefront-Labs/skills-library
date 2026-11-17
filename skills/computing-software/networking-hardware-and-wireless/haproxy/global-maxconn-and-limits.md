---
id: computing-software.networking-hardware-and-wireless.haproxy.global-maxconn-and-limits
name: global-maxconn-and-limits
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, maxconn, ulimit-n, file-descriptors, global-section]
level: practitioner
status: docs-checked
description: "Size global maxconn, per-frontend maxconn and ulimit so HAProxy does not silently cap connections or run out of file descriptors."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
  - https://docs.haproxy.org/3.0/management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# global maxconn and limits
`maxconn` in `global` is the per-process ceiling on concurrent connections; proxies stop accepting connections when it is reached. `maxconn` in a frontend caps that listener (default 0 = use the global value; it should not exceed the global one; excess connections wait in the socket's listen queue). Server `maxconn` and backend `fullconn` shape backend queues.

```
global
    maxconn 50000
frontend fe_web
    bind :443 ssl crt /etc/haproxy/certs/
    maxconn 40000
```
HAProxy adjusts the process's soft file-descriptor limit from `maxconn` itself. The management guide's estimate: double `maxconn` and add a few tens (it also counts listeners, servers with health checks, agent checks, peers and loggers). The `ulimit-n` setting is a vestige of old versions and should be removed. The adjustment normally needs HAProxy started as root; run as an unprivileged user, the OS limit must be raised for that user and checked with `ulimit -n` before starting, and the docs advise against unprivileged production use.

If `maxconn` is not set, it is computed from the file-descriptor limit (the larger of hard and soft, per `ulimit -nH`), reduced by `fd-hard-limit` and the memory limit given with `-m`, and it depends on buffer size, compression memory and the SSL cache. The per-proxy default of `-N` is usually 2000; if clients stall at such a figure, check it.

Memory: each established connection uses about 33 kB with the default `tune.bufsize` (16384 bytes, two buffers per connection), so 1 GB of RAM supports roughly 20000-25000 connections when tuned. If you raise `tune.bufsize`, lower `maxconn` by the same factor; HTTP/2 needs `tune.bufsize` of at least 16384.

Symptoms of FD exhaustion are `accept()` or `socket()` failing with EMFILE (process limit; raise the limit) or ENFILE (system-wide limit, `fs.file-max`; the per-process hard limit is `fs.nr_open`).

Verify: `show info` on the runtime socket reports `Maxconn`, `Ulimit-n` and `CurrConns`; `Ulimit-n` should be about twice `Maxconn` plus overhead (the sample shows `Ulimit-n: 120032` with `Maxconn: 60000`).

## Checked
2026-11-03. Confirmed against configuration.html (global `maxconn`, `ulimit-n`, `tune.bufsize`, frontend `maxconn` and its 33 kB per connection note) and management.html (file-descriptor section, `show info` sample). Removed: `LimitNOFILE` and `systemctl edit` advice, the "Cannot raise FD limit" log message, "lowers maxconn if the OS limit is smaller", "MaxconnReached", the "confirm" marker, and the "tens of KB plus TLS state" estimate.
Method: documentation only; no commands were run.
