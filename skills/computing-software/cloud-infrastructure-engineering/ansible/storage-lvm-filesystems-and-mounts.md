---
id: computing-software.cloud-infrastructure-engineering.ansible.storage-lvm-filesystems-and-mounts
name: storage-lvm-filesystems-and-mounts
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, storage, lvm, lvg, lvol, filesystem, filesystems, mount, parted, partitions, fstab, mkfs, resizefs, xfs, ext4, swap, nfs-mount, community-general, ansible-posix, storage-role, rhel-system-roles-storage, ansible-devices, disk-facts, uuid-mounts]
level: practitioner
status: docs-checked
description: "Provision disks with Ansible: parted partitions, lvg/lvol, filesystem with resizefs, ansible.posix.mount by UUID, swap, NFS, growing volumes and the storage system role."
sources:
  - "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/parted.py"
  - "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/lvg.py"
  - "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/lvol.py"
  - "https://github.com/ansible-collections/community.general/blob/main/plugins/modules/filesystem.py"
  - "https://github.com/ansible-collections/ansible.posix/blob/main/plugins/modules/mount.py"
  - "https://github.com/linux-system-roles/storage/blob/main/README.md"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage: LVM, filesystems and mounts

**Goal:** data disks partitioned, in LVM, formatted and mounted by UUID on every host,
re-runnable, and growable without downtime.

## 1. Find the disk, not the device name
`/dev/sdb` can become `/dev/sdc` after a reboot. Prefer a stable path such as
`/dev/disk/by-id/<serial>`, or select the disk from gathered facts (size, model, serial).

## 2. Partition, VG, LV, filesystem, mount
```yaml
- community.general.parted:
    device: "{{ data_disk }}"
    number: 1
    state: present
    label: gpt
    flags: [lvm]
    part_end: 100%
- community.general.lvg: {vg: vg_data, pvs: "{{ data_disk }}1"}      # whole disk as PV: pvs: "{{ data_disk }}", skip parted
- community.general.lvol: {vg: vg_data, lv: lv_pg, size: 100%FREE, shrink: false}
- community.general.filesystem: {fstype: xfs, dev: /dev/vg_data/lv_pg, resizefs: true}
- ansible.posix.mount:
    path: /var/lib/pgsql
    src: /dev/vg_data/lv_pg          # or UUID=... via a blkid step
    fstype: xfs
    opts: defaults,noatime
    state: mounted                   # mounted = configured in fstab AND mounted now
```
- `parted`: `label` defaults to `msdos` (set `gpt` explicitly) and changing the label of a disk that already has a different one loses the previous partitions. `part_start` defaults to `0%` and `part_end` to `100%`.
- `lvol size:` takes a size (megabytes by default, or with a unit suffix), a percentage of `VG`, `PVS` or `FREE`, and `+` or `-` prefixes to grow or shrink by an amount. `shrink` defaults to `true`; `shrink: false` stops it shrinking when the requested size is smaller than the current one.
- `filesystem` creates the filesystem only if none exists; `force: true` allows creating a new one on a device that already has one. `resizefs: true` grows the filesystem into the device space (XFS only grows when mounted).
- `lvol resizefs: true` resizes the filesystem together with the logical volume, for ext2, ext3, ext4, reiserfs and XFS, and only when the module itself resizes the LV.
- `mount` states: `present` (fstab only), `mounted` (fstab and mounted, creating the mount point if needed), `unmounted` (unmounts, leaves fstab), `absent` (removes the fstab entry, unmounts and removes the mount point), `absent_keep_mountpoint`, `absent_from_fstab`, `remounted` (always reports changed) and `ephemeral` (mount without touching fstab, added in ansible.posix 1.5.0; always changed). `boot: false` adds `noauto`.
- NFS: `mount: {src: "nfs.example:/export/data", path: /data, fstype: nfs, opts: "rw,sync,hard", state: mounted}`.

Mount by UUID for anything not LVM:
```yaml
- ansible.builtin.command: blkid -s UUID -o value /dev/vg_data/lv_pg
  register: uuid
  changed_when: false
- ansible.posix.mount: {src: "UUID={{ uuid.stdout }}", ...}
```

## 3. Growing after a cloud disk is resized
Grow the partition (for example with `growpart`, from cloud-utils; not covered by the docs checked here), then:
```yaml
- community.general.lvg: {vg: vg_data, pvs: "{{ data_disk }}1", pvresize: true}
- community.general.lvol: {vg: vg_data, lv: lv_pg, size: +100%FREE, resizefs: true}
```
`pvresize` defaults to `false`. Use `+100%FREE` to take all remaining space in the VG.

## 4. Swap
```yaml
- community.general.lvol: {vg: vg_sys, lv: lv_swap, size: 4g}
- community.general.filesystem: {fstype: swap, dev: /dev/vg_sys/lv_swap}
```
`filesystem` supports `fstype: swap` (it runs `mkswap`). Add the fstab entry and activate swap as your platform requires.

## 5. The declarative alternative: the storage system role
`linux-system-roles.storage` (shipped as `rhel-system-roles.storage` on RHEL) manages storage from one data structure: `storage_pools` with `name`, `disks` and nested `volumes`; each volume has `name`, `size`, `fs_type` and `mount_point`. It also supports encryption and RAID.
```yaml
- hosts: db
  roles: [redhat.rhel_system_roles.storage]
  vars:
    storage_pools:
      - name: vg_data
        disks: [sdb]
        volumes:
          - {name: lv_pg, size: 100%, fs_type: xfs, mount_point: /var/lib/pgsql}
```
`storage_safe_mode` defaults to `true`: an error occurs instead of automatically removing existing devices or formatting. If a volume `size` is omitted it behaves as `size: 100%`.

## Gotchas
- `lvol` is not idempotent with `+`, `-` or a percentage of `FREE`. A bare `size: 100%FREE` is computed from the free space when the task runs, so a second run requests a smaller size and, unless `shrink: false`, tries to shrink the LV. Use `+100%FREE` to take all remaining space.
- `filesystem` leaves an existing filesystem alone unless `force: true`, so asking for a different `fstype` on a device that has one will not change it; check with `blkid` first.
- `filesystem` needs the tools for the type (`e2fsprogs`, `xfsprogs`, and so on); install them in the same play.

## Verify
- [ ] `lsblk -f` on the host shows the partition, VG/LV, fstype and mountpoint as declared.
- [ ] Reboot the host; the mount comes back (fstab entry correct, by UUID or LV path).
- [ ] Second play run reports `changed=0` for parted/lvg/lvol/filesystem/mount.

## Checked

2026-11-09. Checked against the module documentation in the community.general (parted, lvg, lvol, filesystem) and ansible.posix (mount) source on GitHub, and the linux-system-roles storage README: option names, defaults, mount states, the lvol non-idempotence note, resizefs behaviour, storage_safe_mode and the pool/volume variable names.

Corrected: `lvol size: 100%FREE` was described as growing on every run; the docs say it can instead shrink on a rerun unless `shrink: false`, and recommend `+100%FREE`. `ephemeral` was attributed to Ansible 2.5; the module says ansible.posix 1.5.0.

Removed as not in the documentation: the facts-based disk selection example (the `200.00 GB` string and NVMe link lookup), the `parted` always-changed claim, `ansible_facts.mounts` and `ansible_facts.lvm` notes, the claim that ext4 resizes online, the `_netdev,vers=4.2` NFS options and `nfs-utils` note, the swap fstab and `swapon` lines, the `growpart` return-code handling, and the exam-objective source.

Method: documentation only; no commands were run.
