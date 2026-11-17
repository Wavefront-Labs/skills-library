---
id: computing-software.database-administration.dragonfly.promote-replica
name: promote-replica
category: computing-software
field: database-administration
product: dragonfly
tags: [replicaof-no-one, failover, promotion, dragonfly]
level: practitioner
status: docs-checked
description: "Promote a Dragonfly replica to primary with REPLICAOF NO ONE after the primary fails, keeping its replicated dataset."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/replication.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/replicaof.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To turn a replica back into a primary run:

```bash
dragonfly> REPLICAOF NO ONE
OK
```

Behaviour:

- Replication stops and the server becomes a master.
- The dataset already replicated is **kept** (unlike pointing at a new primary, which discards it).
- Useful when the original primary fails: promote a replica, switch applications to it for read/write, and give it its own replicas as a failsafe.
- When the old server is fixed, it can be reconfigured to work as a replica.

Steps for a manual failover:

1. Confirm the primary is down.
2. On the chosen replica, check `INFO replication` (link status, lag).
3. Run `REPLICAOF NO ONE`.
4. Confirm `ROLE` returns `master`.
5. Repoint application connection strings or service.
6. Run `REPLICAOF new_primary_host port` on the other replicas.

On Kubernetes the Dragonfly Operator performs promotion and updates the service automatically.

## Checked

2026-11-04. Confirmed in the Replication page (REPLICAOF NO ONE keeps the dataset, REPLICAOF host port discards it, useful when the primary fails) and the High Availability page (Operator failover). Nothing removed.

Method: documentation only; no commands were run.
