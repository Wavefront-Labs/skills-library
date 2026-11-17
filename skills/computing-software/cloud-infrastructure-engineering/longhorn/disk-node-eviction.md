---
id: computing-software.cloud-infrastructure-engineering.longhorn.disk-node-eviction
name: disk-node-eviction
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [eviction, eviction-requested, scheduling-disabled, replicas, drain]
level: practitioner
status: docs-checked
description: "Evict Longhorn replicas from a disk or node with Eviction Requested after disabling scheduling, including behaviour on errors and how to cancel."
sources:
  - https://longhorn.io/docs/1.13.0/nodes-and-volumes/nodes/disks-or-nodes-eviction/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move replicas off a disk or node before maintenance or removal.

Eviction auto-moves replicas from a selected disabled disk or node to other suitable ones, keeping the same level of high availability.

Prerequisites: scheduling must be disabled on the disk or node first. Once eviction is on, the disk or node cannot be re-enabled for scheduling. `Eviction Requested` defaults to `false`.

Behaviour:
- Works for attached and detached volumes; detached volumes are attached automatically and detached afterwards.
- One replica per volume is evicted only after that volume's replica rebuild succeeds.
- On error (no space, no schedulable disk) eviction pauses until space is freed or it is cancelled; errors show in the Event log.

Disk (UI):
1. Node tab, select a node, Edit Node and Disks.
2. Set Scheduling to Disable for the disk.
3. Set Eviction Requested to `true` and save.

Node (UI):
1. Node tab, select one or more nodes, Edit Node.
2. Set Scheduling to Disable.
3. Set Eviction Requested to `true` and save.

Cancel by setting Eviction Requested to `false`; replicas already left stay where they are.

Check progress: the Replicas count on the disk or node drops to 0 when eviction succeeds; click the count to list replica names and open each volume.

The page documents the UI only, not kubectl.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/nodes-and-volumes/nodes/disks-or-nodes-eviction/

No claim needed changing.

Method: documentation only; no commands were run.
