---
id: computing-software.systems-network-administration.linux.persistent-device-names
name: persistent-device-names
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, udev, persistent-device-names, by-id, by-uuid, by-path, by-label, by-partuuid, wwn, fstab, device-naming, rhcsa, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Refer to disks by names that don't change between boots: /dev/disk/by-uuid, by-label, by-id, by-path, by-partuuid and which to use for fstab, RAID, ZFS and scripts."
sources:
  - https://github.com/systemd/systemd/blob/main/rules.d/60-persistent-storage.rules.in
  - https://github.com/util-linux/util-linux/blob/master/misc-utils/findfs.8.adoc
  - https://github.com/util-linux/util-linux/blob/master/misc-utils/findmnt.8.adoc
  - https://github.com/util-linux/util-linux/blob/master/lsblk-cmd/lsblk.c
  - https://github.com/libvirt/libvirt/blob/master/docs/formatdomain.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Persistent device names

**Goal:** fstab, crypttab, RAID, ZFS and scripts keep pointing at the right disk even when
`sdb` becomes `sdc` after adding a controller, a USB stick, or just a different probe order.

## 1. What exists
```bash
ls -l /dev/disk/by-uuid/ /dev/disk/by-label/ /dev/disk/by-id/ /dev/disk/by-path/ /dev/disk/by-partuuid/ /dev/disk/by-partlabel/
lsblk -o NAME,SIZE,UUID,LABEL,PARTUUID,WWN,SERIAL,MODEL
blkid
```
| Link | Identifies | Changes when |
|---|---|---|
| `by-uuid` | filesystem UUID (also LUKS and swap) | reformat or UUID change |
| `by-label` | filesystem label | relabel; duplicates possible |
| `by-partuuid` / `by-partlabel` | GPT partition | repartition |
| `by-id` (`wwn-…`, `ata-MODEL_SERIAL`, `nvme-eui…`, `scsi-3…`) | the physical disk/LUN | disk replaced |
| `by-path` | controller port/slot position | moved to another port; same for the replacement disk |

## 2. Which for what
- **fstab / crypttab:** `UUID=` (or `LABEL=` if you control labels). `PARTUUID=` / `PARTLABEL=` for partitions.
- **Whole-disk members (pools, arrays):** `by-id` links built from WWN or serial identify the physical disk.
- **Hardware bay mapping / JBOD slots:** `by-path` — "whatever disk is in slot 3".
- **Scripts:** never `sdX`; resolve with `findfs UUID=…` or `blkid -U`.
```bash
findfs LABEL=data; blkid -U 1c2e…; readlink -f /dev/disk/by-id/wwn-0x5000c500a1b2c3d4
```

## 3. NVMe and virtual disks
Virtio disks (`vdX`) get `by-id` links only when the hypervisor provides a serial (`<serial>` in the libvirt disk definition);
otherwise use `by-path` or `by-uuid`.

## Gotchas
- Cloned disks/snapshots share filesystem UUIDs → wrong one mounted; regenerate the UUID with your filesystem's tools.
- `LABEL=` duplicates (two "data" disks) mount whichever is found first.
- After replacing a disk, `by-id` changes: update anything that referenced the old link.

## Verify
- [ ] `grep -E '^/dev/sd|^/dev/vd|^/dev/nvme' /etc/fstab /etc/crypttab` returns nothing.
- [ ] `findmnt --verify` (the recommended fstab check) passes; reboot with an extra USB disk attached still mounts everything correctly.

## Checked

2026-10-26. systemd main 60-persistent-storage rules: by-id, by-uuid, by-label, by-partuuid, by-path link families and virtio serial handling; util-linux findfs (LABEL=, UUID=, PARTUUID=, PARTLABEL=) and findmnt --verify; lsblk columns UUID, LABEL, PARTUUID, WWN, SERIAL, MODEL; libvirt disk <serial>. Removed unconfirmed recommendations for ZFS, mdadm, Ceph, multipath, NVMe enumeration order, root=, tune2fs and xfs_admin commands. Table rows for by-path and by-id describe the rule sources and were not independently re-derived.

Method: documentation only; no commands were run.
