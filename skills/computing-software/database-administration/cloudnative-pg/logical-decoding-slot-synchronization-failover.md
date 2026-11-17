---
id: computing-software.database-administration.cloudnative-pg.logical-decoding-slot-synchronization-failover
name: logical-decoding-slot-synchronization-failover
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [logical-decoding, replication-slots, synchronizelogicaldecoding, sync-replication-slots, hot-standby-feedback, subscription]
level: advanced
status: docs-checked
description: "Keep logical slots across failover: enable synchronizeLogicalDecoding, set sync_replication_slots and hot_standby_feedback on PG 17+."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Logical decoding slot synchronisation is **disabled by default**. It stops logical replication clients losing data or slots after a failover or switchover. Two steps:

1. Enable it on the cluster:

```yaml
  replicationSlots:
    highAvailability:
      synchronizeLogicalDecoding: true
```

2. Configure PostgreSQL according to version.

**PostgreSQL 17 and later.** The operator transparently manages the `synchronized_standby_slots` parameter. You must enable both GUCs:

```yaml
postgresql:
  parameters:
    hot_standby_feedback: 'on'
    sync_replication_slots: 'on'
```

and create the logical replication `Subscription` with the `failover` option, for example `spec.parameters.failover: 'true'` on the CloudNativePG `Subscription` resource.

With this in place logical WAL senders send decoded changes only after the listed physical slots confirm they have received and flushed the WAL. Consequently logical slots do not consume changes before the publisher's replicas have them, and clients can reconnect to a promoted standby without missing data.

**PostgreSQL 16 and earlier.** CloudNativePG relies on the `pg_failover_slots` extension to keep logical slots synchronised across failovers.

The PostgreSQL manual chapter on logical replication failover has the upstream semantics.

## Checked

2026-11-08. Two-step enablement and the PostgreSQL 17+ versus 16-and-earlier behaviour confirmed on the Replication page, section Logical Decoding Slot Synchronization.

Method: documentation only; no commands were run.
