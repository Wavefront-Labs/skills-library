---
id: computing-software.cloud-infrastructure-engineering.longhorn.node-space-usage
name: node-space-usage
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [space-usage, allocable, over-provisioning, schedulable, disk]
level: practitioner
status: docs-checked
description: "Read Longhorn dashboard and node space figures: Size, Allocated, Allocable, and the ScheduledTotal versus ProvisionedLimit rule that makes a disk unschedulable."
sources:
  - https://longhorn.io/docs/1.13.0/nodes-and-volumes/nodes/node-space-usage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand why a disk will or will not accept replicas.

Dashboard (cluster):
- Schedulable: space usable for volume scheduling
- Reserved: space set aside for other applications and the system
- Used: space used by Longhorn, the system and other applications
- Disabled: total space on disks or nodes where scheduling is not allowed

Node page:
- Size = total disk space minus reserved space; the maximum real space Longhorn volumes can use.
- Allocated (left number) = space already assigned to volume scheduling; not actual data usage.
- Allocated (right number) = Size x Storage Over Provisioning Percentage; the scheduling maximum.
- Allocable space = right number minus left number; a replica can be scheduled only if this is sufficient.
- Used = current used space (left part of the bar) out of total node space.

With over-provisioning above 100%, allocable space can exceed the node's actual available space.

Disk unschedulable condition: shown from `node.diskStatus[x].conditions[Schedulable]` when it is `False`.
- ScheduledTotal = Size + StorageScheduled, covering existing and pending replicas; not actual disk usage.
- ProvisionedLimit = (StorageMax - StorageReserved) x Storage Over Provisioning Percentage.
- The disk is unschedulable when ScheduledTotal > ProvisionedLimit, and accepts no new replicas until disk or cluster settings change.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/nodes-and-volumes/nodes/node-space-usage/

No claim needed changing.

Method: documentation only; no commands were run.
