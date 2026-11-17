---
id: computing-software.cloud-infrastructure-engineering.nginx.sendfile-tcp-tuning
name: sendfile-tcp-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, sendfile, tcp-nopush, tcp-nodelay, static-performance]
level: practitioner
status: docs-checked
description: "Static-file tuning in nginx: sendfile, sendfile_max_chunk, tcp_nopush, tcp_nodelay and open_file_cache, with the documented defaults."
sources: ["https://nginx.org/en/docs/http/ngx_http_core_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

```nginx
sendfile on;                   # default off
sendfile_max_chunk 512k;       # default 2m
tcp_nopush on;                 # default off; takes effect only with sendfile
tcp_nodelay on;                # default on
open_file_cache max=2000 inactive=20s;
open_file_cache_valid 60s;
open_file_cache_min_uses 2;
open_file_cache_errors on;
```

- `sendfile_max_chunk` limits the data per `sendfile()` call; without a limit one fast connection may seize the worker. Before 1.21.4 there was no default limit.
- `tcp_nopush` sets `TCP_CORK` on Linux (`TCP_NOPUSH` on FreeBSD), only when `sendfile` is used. It lets nginx send the response header and the beginning of a file in one packet, and send a file in full packets.
- `tcp_nodelay` (`TCP_NODELAY`) is enabled when a connection moves to keep-alive, and also on SSL connections, for unbuffered proxying and for WebSocket proxying.
- `open_file_cache` can cache open file descriptors with sizes and modification times, directory existence and lookup errors. `max` is the element limit (least recently used removed on overflow), `inactive` defaults to 60 seconds, the cache is off by default. Errors are cached only with `open_file_cache_errors on` (default off). `open_file_cache_valid` (default 60s) is how often entries are revalidated; `open_file_cache_min_uses` (default 1) is the number of accesses within `inactive` needed to keep a descriptor open.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_http_core_module page: all defaults and semantics above.
Removed as unconfirmed: kernel TLS bypass note, claims about network or virtual file systems, the `limit_rate` interaction, the stale-after-deploy remark, and the strace/wrk verify step.
Method: documentation only; no commands were run.
