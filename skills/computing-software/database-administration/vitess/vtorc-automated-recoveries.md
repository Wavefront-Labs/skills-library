---
id: computing-software.database-administration.vitess.vtorc-automated-recoveries
name: vtorc-automated-recoveries
category: computing-software
field: database-administration
product: vitess
tags: [vtorc, recovery, failover, cells-no-recovery, clusters-to-watch, fault-detection]
level: practitioner
status: docs-checked
description: "Run VTOrc: what it detects and fixes, an example invocation with polling flags, the required --cell flag, cell denylists, and coordination via shard locks."
sources:
  - https://vitess.io/docs/25.0/user-guides/configuration-basic/vtorc/
  - https://vitess.io/docs/25.0/reference/vtorc/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VTOrc (a fork of Orchestrator custom-fitted to Vitess) polls vttablets every `--instance-poll-time` and refreshes desired state from the topology every `--topo-information-refresh-duration`, finds problems and fixes them by RPCs to vttablets. It elects a primary for a new shard, so `InitShardPrimary` is unnecessary.

Recoveries include: `ClusterHasNoPrimary` (runs PlannedReparentShard); `DeadPrimary` (EmergencyReparentShard); `IncapacitatedPrimary` (PRS, falling back to ERS); primary config fixes (`PrimaryIsReadOnly`, `PrimarySemiSyncMustBeSet`/`MustNotBeSet`); replica fixes (`NotConnectedToPrimary`, `ConnectedToWrongPrimary`, `ReplicationStopped`, `ReplicaIsWritable`, semi-sync flags); and `StaleTopoPrimary` (demote the stale primary and repoint it).

Example from the page:

```sh
vtorc --topo-implementation etcd2 \
  --topo-global-server-address "localhost:2379" \
  --topo-global-root /vitess/global \
  --cell zone1 --port 15000 \
  --recovery-period-block-duration "10m" \
  --instance-poll-time "1s" \
  --topo-information-refresh-duration "30s"
```

`--clusters_to_watch` takes keyspaces or `keyspace/shard` values. `--cell` is required: VTOrc fails to start with FAILED_PRECONDITION if the cell is missing or unknown. `--cells-no-recovery zone1,zone2` suppresses recovery in those cells (counted as `SkippedRecoveries`/`CellNoRecovery`) but not discovery, and needs a restart to change; `ClusterHasNoPrimary` is suppressed only if every cell in the shard is listed. It does not stop promotion of replicas there; use `--prevent-cross-cell-failover` for that. `--cells-to-watch` was removed.

Run several VTOrc instances: each takes the shard lock before fixing and refreshes its data after acquiring it, so only one actor changes the cluster and stale reads are avoided. All failovers honour the keyspace durability policy.

## Checked

2026-11-04. Recovery table, example invocation, cell flags and locking behaviour confirmed on the VTOrc user guide and Architecture pages.

Method: documentation only; no commands were run.
