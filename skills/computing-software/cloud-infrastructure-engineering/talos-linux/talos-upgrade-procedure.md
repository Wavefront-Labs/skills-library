---
id: computing-software.cloud-infrastructure-engineering.talos-linux.talos-upgrade-procedure
name: talos-upgrade-procedure
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [talosctl, upgrade, installer-image, image-factory, rollback, a-b-image]
level: practitioner
status: docs-checked
description: "Upgrade a Talos node with talosctl upgrade and a factory installer image: supported paths, A-B rollback, the cordon and drain sequence, quorum protection, and what to watch."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/lifecycle-management/upgrading-talos.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
OS upgrades are an API call sent with `talosctl`. The call passes the node an installer image. From Talos 1.14 the `ghcr.io/siderolabs/installer` image is no longer published; installers come from Image Factory as `factory.talos.dev/metal-installer/<schematic-id>:<version>`. Use the schematic ID of the image the node was installed from (it carries the system extensions), or the empty schematic `376567988ad370138ad8b2698212367b8edcb69b5fd68c80be1f2ec7d603b4ba` for an unmodified machine.

```sh
talosctl upgrade --nodes 10.20.30.40 \
  --image factory.talos.dev/metal-installer/376567988ad370138ad8b2698212367b8edcb69b5fd68c80be1f2ec7d603b4ba:<version>
```

`--image` defaults to the installer of the `talosctl` version in use, so it can be omitted for a machine without extensions. Use a `talosctl` matching the running cluster version.

**Paths:** migration is tested only between adjacent minor releases, so upgrade to the latest patch of every intermediate minor (1.0 to 1.0.6, then 1.1.2, then 1.2.4). An OS upgrade does not upgrade Kubernetes (since v1.0).

**Sequence:** the node cordons and drains itself, stops services, unmounts filesystems, writes the new image, sets the bootloader to boot the new kernel once, reboots via `kexec`, verifies itself, makes the boot change permanent, rejoins and uncordons. Workloads sensitive to ungraceful stops need a `lifecycle.preStop` hook.

**Safety:** A-B images keep the previous kernel and OS; a failed boot rolls back automatically, and `talosctl rollback` reverts manually. Talos refuses a control plane upgrade that would lose etcd quorum and lets only one control plane node upgrade at a time. Do not upgrade every node at once if quorum-based software such as Rook/Ceph runs on them. Observe with `talosctl dmesg -f` or `talosctl upgrade --wait --debug`.

## Checked

Whole page read; command, installer scheme, path rule, sequence and FAQ answers confirmed.

Method: docs-checked 2026-11-09 against Talos v1.15 docs upgrading-talos.mdx (read in full).
