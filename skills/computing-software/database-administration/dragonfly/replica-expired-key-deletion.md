---
id: computing-software.database-administration.dragonfly.replica-expired-key-deletion
name: replica-expired-key-deletion
category: computing-software
field: database-administration
product: dragonfly
tags: [replica-delete-expired, expired-keys, ttl, replication, dragonfly]
level: advanced
status: docs-checked
description: "Control whether Dragonfly replicas delete expired keys on read with --replica_delete_expired, trading replica memory against extra work."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Dragonfly replicas proactively delete expired keys when those keys are read.

To disable, start the replica with:

```bash
dragonfly --replica_delete_expired=false
```

The replica then waits for the primary to propagate deletions instead.

Trade-off from the docs: keeping the default can reduce memory usage on replicas that hold many keys with TTLs, at the cost of a small amount of additional work on the replica.

Practical use:

1. Leave the default for TTL-heavy datasets where replica memory matters.
2. Set `false` only if you need the replica to strictly follow the primary's deletion stream.
3. Apply the flag at replica startup.

Expired key counts appear in `INFO stats` as `expired_keys`, and as the `dragonfly_expired_keys_total` Prometheus counter (always exported from v2.0.0).

## Checked

2026-11-04. Confirmed in the Replication page (expired key deletion section), the INFO page (`expired_keys`), the Monitoring page (`dragonfly_expired_keys_total`, v2.0.0) and the flags page (`replica_delete_expired`). Nothing removed.

Method: documentation only; no commands were run.
