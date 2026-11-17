---
id: computing-software.cloud-infrastructure-engineering.longhorn.node-maintenance-and-drain
name: node-maintenance-and-drain
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [maintenance, drain, node-drain-policy, cordon, node-removal]
level: advanced
status: docs-checked
description: "Maintain, remove and upgrade Kubernetes nodes under Longhorn: cordon and drain steps, the five Node Drain Policies, disk and node removal."
sources:
  - https://longhorn.io/docs/1.13.0/maintenance/maintenance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: take nodes out of service without losing volumes.

Maintenance (OS or runtime update):
1. Cordon the node; Longhorn disables scheduling on it.
2. Drain with `--ignore-daemonsets`, since Longhorn DaemonSets would block it. Engines migrate with workload pods; replicas stay or are evicted per the Node Drain Policy. Volumes attached outside CSI (for example via the UI) must be detached manually.
3. Perform the maintenance, such as a reboot.
4. Uncordon; Longhorn re-enables scheduling and may reuse existing replicas. The Replica Replenishment Wait Interval controls how long it waits.

Remove a disk: disable scheduling, evict all replicas, delete the disk. Remove a node: disable disk scheduling, evict replicas, detach volumes, then delete the node in the Node tab or with `kubectl delete node`.

In-place Kubernetes upgrades: cordon and drain each node; set the drain timeout long enough for rebuilds (0 means none); upgrade fewer nodes at a time than the per-volume replica count; consider `allow-if-replica-is-stopped`.

Node Drain Policies:
- Block If Contains Last Replica (default): blocks while the node holds a volume's last healthy replica.
- Allow If Last Replica Is Stopped: blocks only for the last running healthy replica; data is lost if the node never returns.
- Always Allow: never blocks; not for production.
- Block For Eviction: blocks until all replicas are auto-evicted; slow; enable only for planned maintenance.
- Block For Eviction If Contains Last Replica: auto-evicts only last healthy copies; also for planned maintenance.

Longhorn cannot tell cordon from drain, so auto-evicting policies may act on any cordon.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/maintenance/maintenance/

No claim needed changing.

Method: documentation only; no commands were run.
