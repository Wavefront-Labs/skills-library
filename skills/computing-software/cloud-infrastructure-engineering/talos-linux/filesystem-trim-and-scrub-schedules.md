---
id: computing-software.cloud-infrastructure-engineering.talos-linux.filesystem-trim-and-scrub-schedules
name: filesystem-trim-and-scrub-schedules
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [filesystemtrimconfig, filesystemscrubconfig, fstrim, xfs-scrub, xfs, volumes, allowdiscards]
level: advanced
status: docs-checked
description: "Schedule periodic filesystem trim and XFS scrub on Talos: global interval documents, per-volume overrides, eligibility rules, hashed offsets, and status resources."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/storage-and-disk-management/filesystem-trim.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/storage-and-disk-management/filesystem-scrub.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both features use the same model: a global interval document plus an optional per-volume section. Both apply without a reboot.

**Trim** (`fstrim` equivalent; helps SSD wear levelling and thin-provisioned pools). Clusters created with Talos v1.14 or later get this document from `talosctl gen config`; upgraded clusters do not have it, so trimming stays off until you add it:

```yaml
apiVersion: v1alpha1
kind: FilesystemTrimConfig
interval: 168h0m0s
```

Removing the document or `interval: 0s` disables it for volumes that do not enable it explicitly. A volume is trimmed if it is `disk` or `partition` type, `ready`, uses `xfs`, `ext4` or `btrfs`, and, if encrypted, has `allowDiscards` set (opt-in, because discards leak how many and which blocks are used).

**Scrub** (online metadata check via `xfs_scrub`, built into the base image, XFS only) is disabled by default and never emitted by `talosctl gen config`:

```yaml
apiVersion: v1alpha1
kind: FilesystemScrubConfig
interval: 168h0m0s
```

Minimum interval is `10s`. A document without `interval` does nothing.

**Per volume**, `VolumeConfig`, `UserVolumeConfig` and `ExistingVolumeConfig` accept a `trim` or `scrub` section. A section enables the feature unless `enabled: false`. With no global trim document the volume must set `interval` too; a scrub section with no interval falls back to one week.

```yaml
scrub:
  enabled: true
  interval: 24h0m0s
```

**Schedule.** Each volume's offset is a hash of node ID and volume ID: stable across reboots, staggered across the cluster. The slot in progress at boot is skipped. Scrub runs at nice 19, idle I/O class, one volume at a time; unrepairable damage needs `xfs_repair`, which Talos does not run.

**Inspect:** `talosctl --nodes <NODE> get volumetrimschedules`, `get fsscrubschedules`, `get fsscrubstatuses`, `logs fs_scrub`.

## Checked

2026-11-04. Documents, defaults, eligibility lists, schedule hashing and status resources confirmed on the Filesystem Trim and Filesystem Scrub pages.

Method: documentation only; no commands were run.
