---
id: computing-software.database-administration.patroni.patroni-standby-cluster-pitfalls
name: patroni-standby-cluster-pitfalls
category: computing-software
field: database-administration
product: patroni
tags: [patroni, standby-cluster, replication-slots, pg-rewind, member-names]
level: advanced
status: docs-checked
description: "Slots, multiple hosts, pg_rewind and member-name uniqueness for standby clusters."
sources:
  - https://patroni.readthedocs.io/en/latest/standby_cluster.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid the documented traps of standby clusters.

- Replication slots: if you use slots on the standby cluster, you must create the matching slot on the primary cluster yourself; it is not automatic. Use Patroni permanent replication slots on the primary cluster to maintain a slot named like `primary_slot_name`, or its default value when it is not provided.
- Multiple source hosts: if the remote site has no single primary endpoint, list all hosts comma-separated in `standby_cluster.host`. Patroni then adds `target_session_attrs=read-write` to `primary_conninfo` on the standby leader and uses it when checking or running pg_rewind on all standby cluster nodes.
- pg_rewind needs the cluster initialized with `--data-checksums` and/or `wal_log_hints` set to `on`.
- Cascading from another standby cluster or a standby member of the primary cluster is possible with a single host in `standby_cluster.host`, but pg_rewind will then fail on the standby cluster.
- Member names (the `name` setting) must be unique across the primary cluster and all connected standby clusters. Patroni sets `synchronous_standby_names` using member names, which become `application_name` in `pg_stat_replication`. A shared name lets PostgreSQL satisfy synchronous replication with the standby cluster's connection and acknowledge commits prematurely. This is a silent failure: no errors are logged and it risks data loss if the primary fails.

## Checked

2026-11-08. Confirmed every bullet against the Patroni standby cluster page (read in full). Only wording of the slot default was tightened.

Method: documentation only; no commands were run.
