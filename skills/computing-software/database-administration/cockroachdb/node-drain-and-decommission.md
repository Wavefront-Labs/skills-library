---
id: computing-software.database-administration.cockroachdb.node-drain-and-decommission
name: node-drain-and-decommission
category: computing-software
field: database-administration
product: cockroachdb
tags: [node-shutdown, drain, decommission, graceful-shutdown, server-shutdown-initial-wait]
level: advanced
status: docs-checked
description: "Drain a CockroachDB node for maintenance or decommission it permanently: drain phases, load balancer settings, cockroach node commands and timeouts."
sources:
  - https://www.cockroachlabs.com/docs/stable/node-shutdown
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop nodes without latency spikes or lost availability.

Pick the operation:
- Drain: temporary stop (maintenance). Clients are disconnected, leases and Raft leaderships move to other nodes; replicas and data are not moved off the node.
- Decommission: permanent removal. Replicas are rebalanced to other nodes; the node is drained automatically afterward, but you can drain it manually first to avoid query-performance disruption. Membership goes `decommissioning` then `decommissioned`.

Drain phases, in order: unready (the `/health?ready=1` endpoint returns 503 so load balancers reroute), SQL wait (no new connections), SQL drain (active statements finish), DistSQL drain, lease transfer. Wait at least 60 seconds after drain completes before sending `SIGTERM`; terminating before all drain phases finish risks latency spikes until leases settle.

Settings and flags:
```sql
SET CLUSTER SETTING server.shutdown.initial_wait = '8s';
```
`server.shutdown.initial_wait` (default `0s`, alias `server.shutdown.drain_wait`) is a fixed wait in the unready phase; it must exceed your load balancer's detection time (HAProxy defaults `inter 2000 fall 3`). `server.shutdown.connections.timeout` (default `0s`) is the maximum for the connection phase; set it above client pool max lifetime. Manual drain must finish within `--drain-wait` (default `10m`).

Commands:
```shell
cockroach node drain 1 --host={address of any live node} --drain-wait=15m --certs-dir=certs
cockroach node decommission <ids> --host={address} --certs-dir=certs
cockroach node status --decommission --certs-dir=certs --host={address}
```
`--shutdown` on `cockroach node drain` terminates the process after draining.

Check membership with `cockroach node status --decommission`.

## Checked

2026-11-03. Confirmed against the node shutdown page: drain phases and order, `/health?ready=1` 503, 60-second wait, `SIGTERM`, `--shutdown`, `server.shutdown.initial_wait` and alias, `server.shutdown.connections.timeout`, HAProxy example, `--drain-wait`. Removed: store-retention and network-traffic claims, and the verification outcome.
Method: documentation only; no commands were run.
