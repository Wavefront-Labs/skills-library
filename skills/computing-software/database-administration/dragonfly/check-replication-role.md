---
id: computing-software.database-administration.dragonfly.check-replication-role
name: check-replication-role
category: computing-software
field: database-administration
product: dragonfly
tags: [role, replication-state, stable-sync, info-replication, dragonfly]
level: intro
status: docs-checked
description: "Tell whether a Dragonfly instance is primary or replica with ROLE and INFO REPLICATION, and read the replication state values."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/role.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/replication.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/info.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ROLE` (O(1), `@admin`, `@fast`, `@dangerous`) returns the instance role and replication state.

On a primary it returns `master` then, per connected replica, an array of IP, port and state:

```
1) "master"
2) 1) 1) "172.19.0.4"
      2) "6379"
      3) "stable_sync"
```

On a replica it returns `replica`, the master IP, the master port, and the state.

Replica states:

- `connecting`: trying to form a network link
- `preparation`: initial connection made
- `full_sync`: master and replica performing a full synchronisation
- `stable_sync`: the replica is online

`INFO replication` also shows `role`, `connected_slaves` and `master_replid`. On a replica it adds `master_host`, `master_port`, `master_link_status` (up/down), `master_last_io_seconds_ago` and `master_sync_in_progress`. On the primary each replica appears as `slaveN:ip=...,port=...,state=...,lag=...`.

The `INFO` role field is "master" or "slave"; the `ROLE` example output on a replica shows `replica`.

## Checked

2026-11-04. Confirmed in the ROLE page (ACL categories, output format, states), the INFO page (replication fields) and the Replication page (`slave0:ip=...,state=...,lag=` line). Softened the role-name note, because the ROLE page itself lists both `slave` and `replica`.

Method: documentation only; no commands were run.
