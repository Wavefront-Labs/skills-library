---
id: computing-software.database-administration.cloudnative-pg.streaming-replication-and-streaming-replica-user
name: streaming-replication-and-streaming-replica-user
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [streaming-replication, streaming-replica, instances, restore-command, hot-standby, tls-client-cert]
level: practitioner
status: docs-checked
description: "How CloudNativePG builds streaming replicas from spec.instances, the streaming_replica TLS user, and restore_command fallback."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CloudNativePG builds high availability on PostgreSQL native physical replication (application-level replication, not storage-level) and exposes it declaratively:

```
replicas = instances - 1 (where  instances > 0)
```

After initialisation the operator creates the replication user:

```sql
CREATE USER streaming_replica WITH REPLICATION;
-- NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB NOBYPASSRLS
```

Streaming happens over an encrypted channel and the user must authenticate with a TLS client certificate, enforced by these `pg_hba.conf` lines:

```
hostssl postgres streaming_replica all cert map=cnpg_streaming_replica
hostssl replication streaming_replica all cert map=cnpg_streaming_replica
```

Certificate management is covered on the separate Certificates page.

When continuous backup is configured, replicas also get a `restore_command`, so the WAL archive becomes a fallback whenever pulling WAL by streaming fails.

If cluster-managed replication slots are on, the operator maintains slots for all replicas so the primary retains the WAL each standby needs, even after a failover or switchover.

This page is only about replication inside one `Cluster` in one Kubernetes cluster. Replication to another `Cluster`, including across Kubernetes clusters, is the replica cluster feature. The history table on the page runs from warm standby (8.2) through hot standby (9.0), synchronous (9.1) and cascading (9.2) to logical publisher/subscriber (10).

## Checked

2026-11-08. replicas = instances - 1, streaming_replica creation and pg_hba rules, and restore_command integration confirmed on the Replication page.

Method: documentation only; no commands were run.
