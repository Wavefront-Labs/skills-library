---
id: computing-software.cloud-infrastructure-engineering.openebs.rawfile-architecture-and-when-to-use
name: rawfile-architecture-and-when-to-use
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, rawfile, loop-device, architecture, node-local, capacity-tracking, daemonset]
level: practitioner
status: docs-checked
description: "How Local PV Rawfile works: raw files in a pool directory attached as loop devices, node-local volumes with permanent affinity, DaemonSet plugin, and listed advantages."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-rawfile/rawfile-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Local PV Rawfile provisions volumes as raw files on the host filesystem, exposed to pods as independent block devices through Linux loop devices. Each volume is a thick or thin file with its own filesystem (`ext4`, `btrfs` or `xfs`).

How it works: when a PVC is created, the driver allocates a raw file in the configured storage pool directory on the chosen node, attaches it to a loop device, formats it with the requested filesystem and mounts it into the pod. The driver is a DaemonSet node plugin on every eligible node and handles both CSI Node and Controller operations locally. When resize is enabled, a separate controller Deployment handles cluster-wide resize requests. Long-running operations, such as volume and snapshot creation, run as background tasks.

Volumes are strictly node-local. The scheduler uses **storage capacity tracking** to place pods only on nodes with enough pool space, and once a PV exists its node affinity is permanent.

Advantages the docs claim:

- near-bare-metal performance through direct I/O on loop devices;
- hard-enforced size limits, enforced by the OS rather than advisory quotas;
- per-volume usage via `df` plus Prometheus metrics per pool and node;
- a different filesystem and format and mount options per volume;
- block-level copy-on-write snapshots and same-node cloning, with CoW efficiency depending on the pool filesystem;
- online expansion on ext4, btrfs and xfs;
- multiple named storage pools per node.

The page adds that it also provides dynamic provisioning (volumes created on demand) and that, because each volume is its own block device, usage is readable in O(1) via `df`. Long-running operations are handled asynchronously by a built-in Task Manager that persists state so they survive driver restarts and are retried on failure. The page positions it as addressing the core limitations of HostPath-based provisioning and points to the OpenEBS installation guide for setup.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for rawfile-overview) in full. Removed the claim that it is disabled by default in the Helm chart, which the page does not state. Other claims match the page.
