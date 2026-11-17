---
id: computing-software.cloud-infrastructure-engineering.longhorn.auto-balance-replicas
name: auto-balance-replicas
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [auto-balance, replicas, least-effort, best-effort, rebalancing]
level: practitioner
status: docs-checked
description: "Longhorn replica auto-balance modes disabled, least-effort and best-effort, the per-volume override, disk pressure migration and healthy-only rule."
sources:
  - https://longhorn.io/docs/1.13.0/high-availability/auto-balance-replicas/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: spread replicas evenly after nodes change.

Global setting (default `disabled`):
- `disabled`: no auto-balancing
- `least-effort`: balance for minimal redundancy
- `best-effort`: balance for even redundancy

Per volume: `volume.spec.replicaAutoBalance` overrides the global value. `ignored` (default) inherits the global setting; `disabled`, `least-effort` and `best-effort` mean the same as above. In a StorageClass use `replicaAutoBalance: "least-effort"` alongside `numberOfReplicas`, `staleReplicaTimeout` and `fromBackup`.

Behaviour:
- After adding node-2 to a volume with 4 off-balanced replicas, `least-effort` moves 1 replica and `best-effort` moves 2.
- `best-effort` does not force replicas into a zone without enough nodes for even balance; it balances at node level.
- Disk pressure threshold applies to `best-effort` only: at the set percentage (for example 75%) Longhorn migrates replicas to another disk on the same node. Node and zone balance take priority.
- Only `Healthy` volumes are rebalanced; unhealthy or detached volumes need manual action.
- The global setting is only a default and does not change existing volumes; volumes created without it get `ignored`.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/high-availability/auto-balance-replicas/

No claim needed changing.

Method: documentation only; no commands were run.
