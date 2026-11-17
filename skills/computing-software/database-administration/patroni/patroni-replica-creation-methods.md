---
id: computing-software.database-administration.patroni.patroni-replica-creation-methods
name: patroni-replica-creation-methods
category: computing-software
field: database-administration
product: patroni
tags: [patroni, replica, create-replica-methods, basebackup, wal-e]
level: practitioner
status: docs-checked
description: "Configure create_replica_methods with custom scripts, the parameters Patroni passes, and the no_leader, keep_data and no_params flags."
sources:
  - https://patroni.readthedocs.io/en/latest/replica_bootstrap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build replicas from something other than pg_basebackup against the leader.

```
postgresql:
  create_replica_methods:
    - pgbackrest
    - basebackup
  pgbackrest:
    command: /usr/bin/pgbackrest --stanza=<scope> --delta restore
    keep_data: True
    no_params: True
  basebackup:
    max-rate: '100M'
```

- `create_replica_methods` lists methods in execution order; Patroni stops at the first that returns 0. If all fail, it retries all in order on the next loop cycle.
- Each non-basebackup method has its own section with a `command` and extra parameters, passed as `--name=value`.
- Patroni also passes `--scope`, `--datadir`, `--role` (always `replica`) and `--connstring` (connection string to the member to clone from; the user can run SQL and replication commands).
- `no_leader`: allow calling the method even when no leader or replica is running; the connection string is empty. Useful for restoring from a binary backup.
- `keep_data`: do not clean PGDATA before the restore.
- `no_params`: do not pass parameters to the command.

`basebackup` is used when the list is empty. The backup comes from the leader unless replicas with the `clonefrom` tag exist, in which case one of them is the origin. Other tools shown in the docs include WAL-E (`patroni_wale_restore`) and Barman (`patroni_barman recover`).

## Checked

2026-11-03. Confirmed against the replica bootstrap page (create_replica_methods, command, keep_data, no_params, no_leader, parameters passed to the command, clonefrom behaviour) and Tools integration (WAL-E and Barman examples).

Method: documentation only; no commands were run.
