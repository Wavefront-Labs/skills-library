---
id: computing-software.database-administration.vitess.durability-policies
name: durability-policies
category: computing-software
field: database-administration
product: vitess
tags: [durability-policy, semi-sync, setkeyspacedurabilitypolicy, promotion-rules, cross-cell]
level: practitioner
status: docs-checked
description: "Choose a keyspace durability policy (none, semi_sync, cross_cell variants) and set it with CreateKeyspace or SetKeyspaceDurabilityPolicy."
sources:
  - https://vitess.io/docs/25.0/user-guides/configuration-basic/durability_policy/
  - https://vitess.io/docs/25.0/reference/vtorc/architecture/
  - https://vitess.io/docs/25.0/user-guides/configuration-basic/vtorc/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A durability policy defines which tablets may be promoted to primary, how many semi-sync acknowledgements are required and which tablets may send them. It implements a `Durabler` interface with `PromotionRule`, `SemiSyncAckers`, `IsReplicaSemiSync` and `HasSemiSync`. PlannedReparentShard and EmergencyReparentShard use it to choose a candidate, and so does VTOrc, so the policy limits what VTOrc can fix without manual help.

Policies listed:
- `none` (default): no semi-sync configuration.
- `semi_sync`: 1 required ack, only REPLICA tablets may ack.
- `semi_sync_with_rdonly_ack`: 1 ack, REPLICA and RDONLY may ack.
- `cross_cell`: 1 ack, only REPLICA tablets from a different cell than the current primary may ack.
- `cross_cell_with_rdonly_ack`: 1 ack, REPLICA and RDONLY from a different cell may ack.

In all of them REPLICA tablets get NeutralPromoteRule and everything else MustNotPromoteRule, so only replicas can become primary.

The policy lives in the keyspace record in the topology server. Set it when creating the keyspace with `CreateKeyspace` or later with `SetKeyspaceDurabilityPolicy` (both `vtctldclient` commands). VTOrc instances and vtctld coordinate by taking a shard lock in the topology server before running any fix.

## Checked

2026-11-08. Read in full: Durability Policy page, VTOrc Architecture page and VTOrc user guide (vitess.io docs 25.0, via the website repo markdown). Confirmed: the five policies, ack and promotion rules, the `Durabler` interface, storage in the keyspace record and the two commands (Durability Policy page); shard-lock coordination (Architecture page); VTOrc honouring durability policies (VTOrc page). Fixed: the lock sentence now says VTOrc and vtctld lock the shard before fixes, as the page states.

Method: documentation only; no commands were run.
