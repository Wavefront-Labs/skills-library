---
id: computing-software.database-administration.patroni.patroni-standby-cluster-setup
name: patroni-standby-cluster-setup
category: computing-software
field: database-administration
product: patroni
tags: [patroni, standby-cluster, cascading-replication, disaster-recovery, dcs]
level: practitioner
status: docs-checked
description: "Configure a standby cluster that replicates from a remote primary through a standby leader."
sources:
  - https://patroni.readthedocs.io/en/latest/standby_cluster.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run cascading replication to a remote datacenter.

A standby cluster has a standby leader, which behaves like a regular leader (holding and updating a leader lock in DCS) but replicates from a remote node, and cascade replicas replicating from it. If the leader lock expires, the cascade replicas elect another leader.

```
bootstrap:
  dcs:
    standby_cluster:
      host: 1.2.3.4
      port: 5432
      primary_slot_name: patroni
      create_replica_methods:
        - basebackup
```

Facts:
- The standby cluster has no further relationship with the source cluster, must not share the same DCS scope if it uses the same DCS, and does not appear in `patronictl list` or `topology` of the source.
- `standby_cluster.create_replica_methods` is distinct from `postgresql.create_replica_methods` (used when detached). Both reference keys in the `postgresql` section.
- These options apply only at bootstrap; afterwards change them through the DCS.
- Patroni expects `postgresql.conf` or `postgresql.conf.backup` in PGDATA of the remote primary and will not start if missing after a basebackup. Copy it if the remote keeps it elsewhere.

## Checked

2026-11-08. Confirmed against the Patroni standby cluster page (read in full). Removed the list of other `standby_cluster` keys and the FAQ remark, which that page does not state.

Method: documentation only; no commands were run.
