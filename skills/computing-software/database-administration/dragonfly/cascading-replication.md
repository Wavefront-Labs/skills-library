---
id: computing-software.database-administration.dragonfly.cascading-replication
name: cascading-replication
category: computing-software
field: database-administration
product: dragonfly
tags: [cascaded-replication, experimental, partial-sync, replication-chain, dragonfly]
level: advanced
status: docs-checked
description: "Enable experimental cascading replication in Dragonfly so a replica can feed downstream replicas with partial sync."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/replication.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Status: **experimental**. Available from Dragonfly v1.40.0 behind a flag that is off by default.

Enable:

```bash
dragonfly --experimental_cascaded_partial_sync=true
```

Start **every node in the replication chain** with this flag. Then a replica can act as the upstream for downstream replicas, and partial synchronisation works across the chain.

Behaviour to plan for: if an intermediate replica performs a full synchronisation after its upstream primary changes, it forces its downstream replicas to fully resynchronise so the whole chain converges to the new dataset.

Caution: it is flagged experimental in both the replication guide and the flag reference, so test failover and resync before production use.

## Checked

2026-11-04. Confirmed in the Replication page (cascading caution block) and the flags page (`experimental_cascaded_partial_sync`, default false). Removed the unsourced downstream REPLICAOF example; the docs describe the chain but show no cascade setup commands.

Method: documentation only; no commands were run.
