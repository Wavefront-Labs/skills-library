---
id: computing-software.database-administration.memcached.proxy-batching-behaviour
name: proxy-batching-behaviour
category: computing-software
field: database-administration
product: memcached
tags: [proxy-internals, batching, worker-threads, iothread, lua-vm]
level: sme
status: docs-checked
description: "How the proxy batches client and backend requests, why time to first byte equals the slowest backend, and iothread effects."
sources:
  - https://docs.memcached.org/features/proxy/arch/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

- A listen thread hands connections round-robin to workers; each worker has its own Lua VM and TCP connection to each backend (or, with `iothread = true`, a single IO thread batches requests and uses fewer sockets).
- Client batching: a client sending `get foo`, `get bar`, `get baz` in one write is read (up to 16 kB), requests dispatch to their backends in parallel, then the client is suspended until all return. Time to first byte is the slowest backend. New requests on that socket wait.
- Backend batching: requests queued for a backend go out in one write; responses are read up to 16 kB and returned to their clients immediately. If a backend breaks, the queue is drained with error responses.
- Config load: a separate config thread runs `mcp_config_pools`, copies to workers one at a time; keep `mcp_config_routes` lightweight.

## Checked

2026-11-04. Confirmed against the proxy architecture page (round-robin workers, per-worker Lua VM, 16kb reads, suspension, backend batching, queue drain, config thread, iothread). Removed: the closing implication line.

Method: documentation only; no commands were run.
