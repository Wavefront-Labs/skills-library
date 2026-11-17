---
id: computing-software.cloud-infrastructure-engineering.longhorn.replica-scheduling
name: replica-scheduling
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [scheduling, anti-affinity, over-provisioning, zones, minimal-available]
level: advanced
status: docs-checked
description: "How Longhorn places replicas in two stages: node and zone anti-affinity, then disk rules, space formulas and balance scoring, with the related settings."
sources:
  - https://longhorn.io/docs/1.13.0/nodes-and-volumes/nodes/scheduling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: predict where replicas land and why scheduling fails.

Two stages; stage 2 runs only if stage 1 succeeds.

Stage 1, node and zone:
- Node tags: tagged volumes only use matching nodes; untagged volumes follow Allow Empty Node Selector Volume (default `true`).
- Cordoned nodes are excluded when Disable Scheduling On Cordoned Node is `true` (default).
- Preference: new node in new zone, then new node in existing zone, then existing node in existing zone.
- Soft anti-affinity: zone false and node false uses a new node in a new zone only; zone true and node false allows a new node in an existing zone; zone true and node true allows an existing node as a last resort; other combinations do not schedule.

Stage 2, disk:
- Disk tags, with Allow Empty Disk Selector Volume (default `true`).
- Hard anti-affinity: no two replicas of a volume on one disk; soft prefers an empty disk but may share.
- Actual Space Usage: `(Available - Actual Size) > (Maximum x Minimal Available %) / 100`.
- Scheduling Space: `(Size + Scheduled) <= ((Maximum - Reserved) x Over Provisioning %) / 100`; over-provisioning defaults to 100%.

Balance: usable storage per disk is `(Available - Reserved) - Scheduled`; score is `(max - min) / mean` and the lowest wins; the node is chosen first, then the disk.

Settings: Replica Node, Zone and Disk Level Soft Anti-Affinity, Storage Minimal Available Percentage, Storage Over Provisioning Percentage. Zones come from `topology.kubernetes.io/zone` or `topology.kubernetes.io/region` node labels.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/nodes-and-volumes/nodes/scheduling/

No claim needed changing.

Method: documentation only; no commands were run.
