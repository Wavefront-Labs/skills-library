---
id: computing-software.database-administration.dragonfly.monitor-replication-lag
name: monitor-replication-lag
category: computing-software
field: database-administration
product: dragonfly
tags: [replication-lag, lag-records, info-replication, prometheus, dragonfly]
level: practitioner
status: docs-checked
description: "Read Dragonfly replication lag from INFO REPLICATION and the dragonfly_connected_replica_lag_records Prometheus metric."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/replication.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/monitoring.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dragonfly defines replication lag as the maximal amount of unacknowledged database among all shards. The primary calculates it.

Two places to read it:

1. `INFO REPLICATION` on the primary, the `lag` field of each replica line:

```bash
dragonfly> INFO REPLICATION
# Replication
role:master
connected_slaves:1
slave0:ip=127.0.0.1,port=6380,state=stable_sync,lag=0
```

2. The Prometheus metric `dragonfly_connected_replica_lag_records` on the `/metrics` endpoint, which also exposes the replication role, connected replicas and replication backlog.

Action list:

- Alert on sustained nonzero `lag` and on state other than `stable_sync` (see `ROLE`).
- If lag stays high or replicas often resync fully, review the replication backlog flags (`shard_repl_backlog_time_ms`, `shard_repl_backlog_max_bytes`).
- Before decommissioning an old primary during migration, verify lag is zero and the replica link is `up`.

## Checked

2026-11-04. Confirmed in the Replication page (lag definition, `INFO REPLICATION` `lag` field, Prometheus metric name) and the Monitoring page (replication metrics on `/metrics`). The `up` link value comes from the INFO page (`master_link_status`). The action list is operational advice built on those fields.

Method: documentation only; no commands were run.
