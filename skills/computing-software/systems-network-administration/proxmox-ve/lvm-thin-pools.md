---
id: computing-software.systems-network-administration.proxmox-ve.lvm-thin-pools
name: lvm-thin-pools
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [lvm-thin, thin-pool, vgcreate, lvcreate, lvresize]
level: practitioner
status: docs-checked
description: "Create LVM volume groups and thin pools, and resize a thin pool and its metadata on Proxmox VE."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
  - https://pve.proxmox.com/pve-docs/chapter-pvesm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The installer's default layout uses volume group `pve` with three logical volumes: `root` (ext4), `swap`, and `data`, an LVM-thin pool for guest images. LVM-thin is preferred for images because it supports efficient snapshots and clones. Since version 4.2, `/var/lib/vz` is just a directory on the root filesystem.

Create a volume group on an empty disk (this destroys data on it):

```
sgdisk -N 1 /dev/sdb
pvcreate --metadatasize 250k -y -ff /dev/sdb1
vgcreate vmdata /dev/sdb1
```

Create a thin pool on the volume group:

```
lvcreate -L 80G -T -n vmstore vmdata
```

Grow it. When extending the data pool you must also extend its metadata:

```
lvresize --size +<size[M,G,T]> --poolmetadatasize +<size[M,G]> <VG>/<LVThin_pool>
```

Extra thin LV for `/var/lib/vz`:

```
lvcreate -n vz -V 10G pve/data
mkfs.ext4 /dev/pve/vz
echo '/dev/pve/vz /var/lib/vz ext4 defaults 0 2' >> /etc/fstab
```

Make sure `/var/lib/vz` is empty before mounting, which it is not on a default install.

The default install registers its pool in `/etc/pve/storage.cfg` as `lvmthin: local-lvm` with `thinpool data` and `vgname pve`. For a new pool, add a matching `lvmthin` stanza with your `vgname` and `thinpool`. Hardware RAID with a battery-backed cache is recommended underneath LVM.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-sysadmin.html, https://pve.proxmox.com/pve-docs/chapter-pvesm.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
