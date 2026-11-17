---
id: computing-software.systems-network-administration.incus.storage-btrfs-driver
name: storage-btrfs-driver
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, storage, btrfs, subvolume, qgroups, quotas, compression, nested]
level: advanced
status: docs-checked
description: "Run Incus on Btrfs: subvolume model, qgroup quota weaknesses, why VMs on Btrfs are discouraged, the size.state workaround and btrfs.compression=none."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/reference/storage_btrfs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Btrfs driver

- Needs `btrfs-progs`. Incus makes one subvolume per instance, image and snapshot; launching an instance takes a Btrfs snapshot.
- Nested Incus: the parent container must also use Btrfs, and quotas are not inherited.

Quotas use qgroups. New subvolumes are not added to their parent's qgroups, so quotas can be bypassed. Extents are immutable, so a quota can be hit even when current files are smaller. For strict quotas use ZFS with `refquota`, or LVM with Btrfs on top.

VMs: Btrfs cannot hold block devices, so Incus uses a large file. This is inefficient and troublesome for snapshots; the page says never use VMs on Btrfs pools. If you must, set the root disk's `size.state` to twice the root disk size. The `btrfs.compression` volume option eases the quota problem but disables turning off COW; set `btrfs.compression=none` to keep COW disabled.

Local-pool buckets need `core.storage_buckets_address`.

## Checked

2026-11-04: confirmed against the Incus Btrfs storage driver reference page (subvolume model, qgroup quota caveats, VM note, `size.state`, `btrfs.compression=none`, bucket address setting). Nothing removed.

Method: documentation only; no commands were run.
