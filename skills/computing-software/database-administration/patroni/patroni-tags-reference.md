---
id: computing-software.database-administration.patroni.patroni-tags-reference
name: patroni-tags-reference
category: computing-software
field: database-administration
product: patroni
tags: [patroni, tags, nofailover, noloadbalance, clonefrom]
level: practitioner
status: docs-checked
description: "All predefined Patroni node tags, their defaults and effects, plus custom tags."
sources:
  - https://patroni.readthedocs.io/en/latest/yaml_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: steer failover, sync, cloning and load balancing per node.

Set under `tags:` in the local configuration.

- `nofailover` (default false): if true, the node does not participate in leader races. Equivalent to `failover_priority: 0`.
- `failover_priority`: integer; higher wins among nodes with equal WAL. 0 or negative excludes the node. Do not set together with `nofailover`.
- `noloadbalance` (default false): if true, `GET /replica` returns 503.
- `clonefrom` (default false): if true, other nodes may prefer this node for pg_basebackup. Several candidates are chosen at random.
- `replicatefrom`: name of another replica to replicate from, for cascading replication.
- `nosync`: never selected as a synchronous replica.
- `sync_priority`: integer; higher is preferred when `synchronous_mode` is on; 0 or negative excludes it from `synchronous_standby_names`.
- `nostream`: when true, the node does not use the replication protocol to stream WAL; it relies on archive recovery (if `restore_command` is set) and `pg_wal` polling. It also disables copying and syncing permanent logical slots on that node and its cascading replicas. No effect on a primary.

Custom tags are allowed, for example:

```
tags:
  key1: true
  key3: 1.4
  key4: "RandomString"
```

Tags are visible in the REST API and `patronictl list`. Health checks can filter on them; an undefined tag or mismatched value returns 503.

## Checked

2026-11-03. Confirmed against YAML Configuration Settings (tags section): nofailover, failover_priority, noloadbalance, clonefrom, replicatefrom, nosync, sync_priority, nostream and custom tags.

Method: documentation only; no commands were run.
