---
id: computing-software.cloud-infrastructure-engineering.talos-linux.architecture-and-components
name: architecture-and-components
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [architecture, apid, machined, trustd, containerd, partitions, immutable, grpc]
level: intro
status: docs-checked
description: "How Talos Linux is built: atomic image, gRPC components (apid, machined, trustd, udevd), partition labels, the read-only squashfs root and what survives reboot, upgrade and reset."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/overview/what-is-talos.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/learn-more/architecture.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/learn-more/components.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Talos is a Kubernetes-optimised distro with four stated traits: API managed, immutable file system, minimal packages, secure by default. It is **atomic** in deployment (one versioned, signed, immutable image) and **modular** in composition (components talk gRPC over a local socket).

Components:

- `apid`: the gRPC endpoint `talosctl` talks to; routes requests to the right node and forwards to `machined`.
- `machined`: replaces init. It does not allow arbitrary user services; only containerd, etcd, kubelet, networkd, trustd, udevd. It also handles machine configuration, API handling, resources and controllers.
- `trustd`: establishes trust (root of trust) so PKI material can be distributed during control plane bootstrap.
- `udevd`: eudev inside `machined`.
- `containerd`: Talos services live in the `system` namespace, Kubernetes in `k8s.io`.
- The kernel follows the Kernel Self Protection Project recommendations.

Routing example from the docs: `talosctl -e cluster.talos.dev -n node02 memory`. `-e/--endpoints` picks the node whose `apid` takes the connection; `-n/--nodes` picks who answers (default: first endpoint).

Partitions: EFI, BIOS, BOOT, META, STATE (machine config, node identity, KubeSpan info), EPHEMERAL (mounted at `/var`).

Root file system: read-only squashfs loop-mounted in memory, tmpfs layers (`/dev`, `/proc`, `/run`, `/sys`, `/tmp`, `/system`), and only specific files such as `/etc/hosts` made writable by bind-mounting from `/system`. `/system` is recreated every boot. Persistent paths such as `/etc/kubernetes` are `overlayfs` on the XFS `/var`, which survives reboots and upgrades but is wiped on reset unless `--system-labels-to-wipe` is used.

## Checked

2026-11-04. What-is-Talos, Architecture and Components pages confirm the traits, component roles, partition labels and layered root file system described.

Method: documentation only; no commands were run.
