---
id: computing-software.database-administration.cloudnative-pg.replication-slots-ha-and-user-defined
name: replication-slots-ha-and-user-defined
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [replication-slots, high-availability, synchronizereplicas, slotprefix, updateinterval, failover]
level: advanced
status: docs-checked
description: "Use cluster-managed replication slots so standbys keep WAL after failover: HA slots, user-defined slot sync with excludePatterns, update interval, max_slot_wal_keep_size."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A replication slot lives only on the instance that created it, so after failover the new primary lacks the old primary's slots. CloudNativePG synchronises physical slots from primary to standbys:

- **Primary HA slot**: managed by the current primary, maps to one standby, lives only on the primary.
- **Standby HA slot**: managed by another standby from `pg_replication_slots` on the primary, advanced with `pg_replication_slot_advance()`.

HA slots are on by default. Options: `.spec.replicationSlots.highAvailability.enabled` (default `true`), `.slotPrefix` (default `_cnpg_`), and `.spec.replicationSlots.updateInterval` (seconds, default 30). Disable with:

```yaml
  replicationSlots:
    highAvailability:
      enabled: false
```

Slow the sync to every five minutes with `updateInterval: 300`.

**User-defined slots.** The operator does not create them declaratively (you do it via SQL), but synchronises any physical slot you create, by default all of them:

```yaml
  replicationSlots:
    synchronizeReplicas:
      enabled: true
      excludePatterns:
      - "^foo"
```

Setting `enabled: false` makes the operator remove slots it previously created on standbys. Monitor user slots so they do not interfere with failover.

**Disk safety.** Slots can pin WAL until the disk fills (a down or lagging standby, or an orphan slot). PostgreSQL 13+ offers `max_slot_wal_keep_size`, default `-1` (unlimited), so set it explicitly:

```ini
  postgresql:
    parameters:
      max_slot_wal_keep_size: "10GB"
```

The Prometheus exporter ships a `pg_replication_slots` metric with slot name, type, active state and lag.

## Checked

2026-11-04. HA slot defaults, synchronizeReplicas options, updateInterval, max_slot_wal_keep_size advice and the pg_replication_slots metric confirmed on the Replication page.

Method: documentation only; no commands were run.
