---
id: computing-software.database-administration.memcached.proxy-stats-and-watch
name: proxy-stats-and-watch
category: computing-software
field: database-administration
product: memcached
tags: [stats-proxy, watch-proxyevents, proxy-monitoring, proxyreqs, backend-errors]
level: advanced
status: docs-checked
description: "Observe a proxy with stats proxy counters and watch proxyevents/proxyreqs for backend disconnects and markedbad events."
sources:
  - https://docs.memcached.org/features/proxy/run/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`stats proxy` returns config limits and counters: `active_req_limit`, `buffer_memory_limit`, `buffer_memory_used`, `vm_gc_runs`, `vm_memory_kb`, and per-command counts `cmd_mg`, `cmd_get`, `cmd_set`, `cmd_delete`, and so on.

`stats` also carries `proxy_conn_requests`, `proxy_conn_errors`, `proxy_conn_oom`, `proxy_req_active`.

`watch proxyevents` -> `OK`, then lines like `ts=... gid=4 type=proxy_backend error=disconnected name=127.0.0.1 port=11213 ...`. A flapping backend shows `disconnected`, `reading`, `connecting` and finally `markedbad retry=3`. Other streams: `proxyreqs` (request timings), `proxyuser` (Lua logs).

Config reload errors also appear in `proxyevents`.

## Checked

2026-11-04. Confirmed against the Run page (stats proxy output, watch proxyevents sample incl. markedbad) and protocol.txt (proxy_conn_* stats, watch streams). Removed: the closing proxy_enabled tip.

Method: documentation only; no commands were run.
