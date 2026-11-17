---
id: computing-software.cloud-infrastructure-engineering.openebs.hostpath-xfs-quota-prerequisites
name: hostpath-xfs-quota-prerequisites
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, hostpath, xfs, quota, pquota, prjquota, grub, fstab, xfsprogs]
level: advanced
status: docs-checked
description: "Prepare a node for Local PV Hostpath XFS quotas: install xfsprogs, confirm the BasePath filesystem is XFS, and mount with pquota via GRUB rootflags or fstab."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-hostpath/advanced-operations/xfs-quota/xfs-quota-pre
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
XFS quota enforcement needs the `xfsprogs` package, an XFS filesystem under the BasePath, and project quota enabled at mount time.

1. **Install xfsprogs** with apt on Ubuntu or Debian, yum on RHEL or CentOS, or dnf on Fedora.
2. **Check the filesystem.** Run `df -Th /var/openebs/local` (the default BasePath). If the path does not exist yet, the page gives a loop that walks up to the nearest existing parent directory and runs `df -Th` on it.
3. **Check mount options** with `mount | grep` on the device. You need `pquota` or `prjquota`; the page's example output for a device without it shows `noquota`.
4. **Enable it.** For the **root filesystem**, add `rootflags=pquota` to `GRUB_CMDLINE_LINUX` in `/etc/default/grub` (append to an existing `rootflags`), back up `grub.cfg` (the location varies by OS, for example under `/boot/grub2` or `/boot/efi/EFI/<distro>`), regenerate it with `grub2-mkconfig`, reboot, and recheck for `prjquota`. For a **data disk**, unmount it, mount with `-o rw,pquota`, verify, and add `pquota` to its `/etc/fstab` entry so it survives reboots.

The page warns that `pquota` cannot be applied with `remount`. The page also links an XFS Quota with Loop Device guide.

## Checked

2026-11-04. Confirmed against the XFS Quota Prerequisites page: xfsprogs install, the `df -Th` check and loop, `pquota` or `prjquota`, `rootflags=pquota`, grub steps, the data-disk mount and fstab entry, and the remount caution. Removed the description of the loop-device guide, which is not on this page.

Method: documentation only; no commands were run.
