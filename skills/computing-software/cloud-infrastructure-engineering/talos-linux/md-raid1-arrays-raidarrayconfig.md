---
id: computing-software.cloud-infrastructure-engineering.talos-linux.md-raid1-arrays-raidarrayconfig
name: md-raid1-arrays-raidarrayconfig
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [raid, raidarrayconfig, raid1, md, mdadm, boot, unattendedinstallconfig, kernelmoduleconfig]
level: advanced
status: docs-checked
description: "Create Linux MD RAID1 arrays on Talos with RAIDArrayConfig: metadata 1.0 versus 1.2, bootable mirrored install disks, user volume on top, status values, no member removal."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/storage-and-disk-management/raid.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`RAIDArrayConfig` provisions Linux MD software RAID; in Talos v1.14 only `raid1` is supported. The array appears at a stable path such as `/dev/disk/by-id/md-name-talos:data`. `name` is 1-32 characters; `provisioning.volumeSelector.match` is a CEL expression over `volume` (and `disk`). The system disk is never eligible for data arrays.

```yaml
apiVersion: v1alpha1
kind: RAIDArrayConfig
name: data
level: raid1
metadata: "1.2"
provisioning:
  volumeSelector:
    match: disk.transport == "nvme" && disk.size > 100u * GiB
```

`metadata` is `"1.0"` (default, superblock at the end of each member, suitable for boot) or `"1.2"` (near the start, for non-boot data arrays).

Provisioning is additive: Talos creates the array once enough members match and adds new matches, but never removes members or destroys arrays when config changes. In v1.14 there is no way to shrink an array or detach or replace a failed member via config or `talosctl`; recover by wiping and reprovisioning (or `talosctl debug`).

Booting from RAID1 needs a `raid1` array with metadata `"1.0"`, an `UnattendedInstallConfig` selecting the MD device, and a kernel module document:

```yaml
apiVersion: v1alpha1
kind: UnattendedInstallConfig
provisioning:
  diskSelector:
    match: '"/dev/disk/by-id/md-name-talos:boot" in disk.symlinks'
---
apiVersion: v1alpha1
kind: KernelModuleConfig
name: raid1
```

A user volume can use `'"/dev/disk/by-id/md-name-talos:data" in disk.symlinks'` as its `diskSelector`. Inspect with `talosctl --nodes <NODE> get mdarrayspecs` and `get mdarraystatuses` (states `unknown`, `waiting`, `rebuilding`, `ready`, `error`). Remove by deleting the document, then:

```bash
talosctl --nodes <NODE> wipe md /dev/disk/by-id/md-name-talos:data
```

That stops the array and clears each member superblock, destructively.

## Checked

2026-11-04. Fields, metadata guidance, additive provisioning limits, boot example, statuses and wipe command confirmed on the RAID page.

Method: documentation only; no commands were run.
