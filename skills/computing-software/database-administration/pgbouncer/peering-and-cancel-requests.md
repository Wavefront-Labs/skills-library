---
id: computing-software.database-administration.pgbouncer.peering-and-cancel-requests
name: peering-and-cancel-requests
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, peers, peer-id, cancel-requests, load-balancer]
level: sme
status: docs-checked
description: "peer_id and the [peers] section: forwarding cancel requests between PgBouncer processes behind one TCP load balancer."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make query cancellation work with several PgBouncer processes behind one load balancer.

Cancel requests arrive on a different TCP connection than the query they cancel, so a TCP load balancer may deliver them to a different process. Peering forwards them to the originating process.

Steps: give each process a unique `peer_id` (global setting, default 0 meaning peering disabled, maximum 16383) and add a [peers] section with an entry for each peer id:

```
[peers]
1 = host=host1.example.com
2 = host=/tmp/pgbouncer-2 port=5555
```

[peers] keys: `host` (name, IP, `/` for a Unix socket, `@` for abstract), `port` (default 6432) and `pool_size` (maximum cancel requests in flight to that peer; defaults to default_pool_size). Bursts of cancels are normal when the backing server is slow or down, so do not set it too low.

Notes from the docs:

- An entry for the process's own peer_id is allowed but ignored, so one [peers] section can be shared by all configs.
- A hostname resolving to several IPs is not recommended; a cancel may still go to the wrong node and be forwarded again, allowed only up to three times.
- Cross-version peering works only when all peers are on the same side of v1.21.0, whose cancellation token encoding changed.

Inspect with SHOW PEERS and SHOW PEER_POOLS (columns cl_active_cancel_req, cl_waiting_cancel_req, sv_active_cancel, sv_login).

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
