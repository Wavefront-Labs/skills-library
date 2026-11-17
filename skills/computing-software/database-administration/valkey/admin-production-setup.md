---
id: computing-software.database-administration.valkey.admin-production-setup
name: admin-production-setup
category: computing-software
field: database-administration
product: valkey
tags: [admin, production, overcommit, transparent-huge-pages, maxmemory, upgrade, zero-downtime]
level: practitioner
status: docs-checked
description: "Valkey production setup checklist: Linux overcommit and THP, swap, maxmemory headroom, replication backlog, and zero-downtime upgrade via replica."
sources:
  - https://valkey.io/topics/admin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Linux host settings: set `vm.overcommit_memory = 1` (in `/etc/sysctl.conf`, or `sysctl vm.overcommit_memory=1` live) so background-save `fork()` does not fail. Disable Transparent Huge Pages with `echo never > /sys/kernel/mm/transparent_hugepage/enabled`.

Memory: enable swap sized equal to RAM so an overshoot shows up as detectable latency instead of a crash or OOM-killer kill. Always set `maxmemory`, leaving room for non-data overhead and fragmentation; with 10 GB free, set 8 or 9 GB. During an RDB save or AOF rewrite a write-heavy instance can use up to 2x its normal memory, proportional to pages modified meanwhile.

Replication: size the replication backlog in proportion to dataset memory so replicas resync easily. With replication, RDB saves happen even if persistence is off (except diskless replication), so enable diskless replication when the primary has no disk use. Never let a primary with persistence disabled auto-restart on crash: it comes back empty and wipes its replicas.

Defaults are open: no authentication, all interfaces, so secure it. Under daemontools use `daemonize no`.

Zero-downtime upgrade (single instance): start the new instance as a replica (different port if same host), wait for initial sync, compare key counts in `INFO`, run `CONFIG SET replica-read-only no`, point clients at it (optionally `CLIENT PAUSE` the old primary), confirm the old primary is idle via `MONITOR`, then `REPLICAOF NO ONE` and shut the old one down. With Sentinel or Cluster, upgrade replicas one at a time, manually fail over, then upgrade the last.

## Checked
2026-11-03. Confirmed against the Valkey Administration page (valkey.io/topics/admin/): overcommit and THP settings, swap equal to RAM, maxmemory headroom (10 GB free means 8 or 9), up to 2x memory during save or rewrite, backlog sizing, RDB saves under replication unless diskless, the auto-restart warning, `daemonize no` under daemontools, and the zero-downtime upgrade steps. The page itself carries an under-review notice, so re-read it before relying on details. Nothing removed.
Method: documentation only; no commands were run.
