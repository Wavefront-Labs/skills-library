---
id: computing-software.database-administration.cloudnative-pg.cluster-services-rw-ro-r-read-write-split
name: cluster-services-rw-ro-r-read-write-split
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [services, rw, ro, read-only, hot-standby, failover, managed-services]
level: intro
status: docs-checked
description: "Know what the -rw, -ro and -r services of a CloudNativePG cluster route to, how they follow failover, and where to trim them with managed.services."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every cluster exposes up to three services, named after the cluster:

- `-rw`: only the current primary. Use for read-write workloads.
- `-ro`: only hot standby replicas, for read-only workloads (optional).
- `-r`: any instance, for read-only workloads (optional).

The operator keeps them correct as topology changes. On failover it repoints `-rw` at the promoted primary so application traffic is redirected without configuration changes.

Applications using `-ro` or `-r` must understand [PostgreSQL Hot Standby](https://www.postgresql.org/docs/current/hot-standby.html) limitations before using these services.

The recommended shared-nothing layout is: instances on different worker nodes sharing only the network, using node-local volumes where possible, spread across availability zones in the same region.

You can reduce the number of services and pick their type (default `ClusterIP`) through `managed.services` in the `Cluster` configuration; see the Service Management page. For connection pooling in front of these services, see the PgBouncer `Pooler` resource.

## Checked

2026-11-08. Read in full: docs/src/architecture.md. Service roles and automatic -rw update on failover confirmed on the Architecture page; trimming via managed.services is only referenced there, with detail on the Service Management page. Removed: the claims about which services drop a failed pod, the statement that standbys cancel conflicting queries, and the round-robin remark (none stated in the text).

Method: documentation only; no commands were run.
