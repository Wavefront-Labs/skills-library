---
id: computing-software.cloud-infrastructure-engineering.garage.known-issue-consistency-limits
name: known-issue-consistency-limits
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [known-issues, conditional-writes, createbucket-race, worm]
level: advanced
status: docs-checked
description: "Understand that missing consensus rules out if-none-match writes, object lock and race-free CreateBucket."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/known-issues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Garage has no consensus algorithm, a core design choice, which causes several documented limits.

Conditional writes, locking and WORM (such as `if-none-match`) cannot be implemented safely. A partial, unsafe version could guarantee non-overwrite only after the first write completes or a lock is set; an overwrite arriving simultaneously cannot be rejected consistently. So many practical uses, such as mutual exclusion between concurrent writers, cannot be supported.

CreateBucket race: concurrent CreateBucket requests with the same name are not mutually exclusive.

Same replication for data and metadata: the single `replication_factor` covers both, so `replication_factor = 1` is especially vulnerable to metadata corruption, because there is a single copy of each object's metadata even in multi-node clusters. Mitigation: do not use `replication_factor = 1`. The long-term aim is separate replication of metadata and data.

LMDB corruption: reports of corruption after forced shutdown or power loss, usually unrecoverable. Mitigation: `replication_factor` of at least 2 plus `metadata_auto_snapshot_interval`. Filesystem snapshots may be inconsistent, so prefer Garage's.

## Checked

2026-11-04. Read the Known issues page in full. Confirmed the conditional-write limit, the CreateBucket race, the shared replication factor issue, the LMDB corruption report and their mitigations. Nothing removed.
Method: documentation only; no commands were run.
