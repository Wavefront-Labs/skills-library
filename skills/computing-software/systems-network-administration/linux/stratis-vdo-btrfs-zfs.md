---
id: computing-software.systems-network-administration.linux.stratis-vdo-btrfs-zfs
name: stratis-vdo-btrfs-zfs
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, stratis, vdo, btrfs, zfs, openzfs, zpool, zfs-snapshot, btrfs-subvolume, btrfs-snapshot, deduplication, compression, thin-provisioning, copy-on-write, advanced-storage, rhcsa, storage, sysadmin, stratis-pool, zfs-send, zfs-properties, btrfs-scrub, btrfs-balance]
level: advanced
status: docs-checked
description: "Choose and run the advanced Linux storage stacks: Stratis pools, VDO dedup/compression, Btrfs subvolumes and snapshots, and OpenZFS pools, with the gotchas of each."
sources:
  - https://stratis-storage.github.io/howto/
  - https://github.com/stratis-storage/stratis-cli/blob/master/docs/stratis.txt
  - https://github.com/lvmteam/lvm2/blob/main/man/lvmvdo.7_main
  - https://btrfs.readthedocs.io/en/latest/
  - https://openzfs.github.io/openzfs-docs/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Stratis, VDO, Btrfs and ZFS — the stacks beyond LVM+ext4/XFS

**Goal:** pick the right advanced storage layer for snapshots, dedup, compression or
checksummed data, and operate it without the classic mistakes (full CoW pools, unsynced
VDO, broken Btrfs RAID5).

| Need | Pick |
|---|---|
| RHEL, want snapshots/thin pools with a simple CLI, no new on-disk format | **Stratis** (XFS over dm-thin) |
| RHEL, dedup/compress VM images or backups on LVM | **VDO** (`lvcreate --type vdo`) |
| Fedora/openSUSE/Ubuntu, root snapshots, send/receive, mirrored data checksums | **Btrfs** |
| Large data pools, proven RAID-Z, ARC caching, replication, Ubuntu/TrueNAS/Proxmox | **ZFS** |

## 1. Stratis (RHEL/Fedora)
```bash
dnf install stratisd stratis-cli && systemctl enable --now stratisd
stratis pool create pool1 /dev/sdb /dev/sdc
stratis filesystem create pool1 fs1
mkdir /srv/fs1 && mount /dev/stratis/pool1/fs1 /srv/fs1
stratis filesystem snapshot pool1 fs1 fs1-snap
stratis pool add-data pool1 /dev/sdd                   # grow
```
- fstab line from the Stratis how-to, which starts the pool before mounting:
  `/dev/stratis/<pool>/<fs> /srv/fs1 xfs defaults,x-systemd.requires=stratis-fstab-setup@<pool uuid>.service 0 2`.
- Filesystems are thin: they grow as needed up to the pool's capacity (or a `--size-limit`), and overprovisioning is controlled by `stratis pool overprovision`; watch
  `stratis pool list` for physical use.
- Encryption: `stratis pool create --key-desc <key> …` after `stratis key set`.

## 2. VDO (dedup + compression under a filesystem)
```bash
lvcreate --type vdo -n vdo1 -L 100G -V 1T vg0           # 100G physical, 1T presented
mkfs.xfs -K /dev/vg0/vdo1                               # -K: skip discard at mkfs time (see mkfs.xfs(8); lvmvdo(7) uses mkfs.ext4 -E nodiscard)
mount /dev/vg0/vdo1 /srv/vdo
vdostats --human-readable                               # physical use and savings (needs /dev/mapper names)
```
- The presented size is a promise; monitor physical use (`lvs` Data% field, `vdostats`).
- lvmvdo(7) warns that TRIM/discard on large VDO volumes is slow, so avoid sending discards unless necessary (no `-o discard` mount option by default).
- VDO combines deduplication, LZ4 compression and thin provisioning; compression and deduplication can be switched with `lvchange --compression` and `--deduplication`.

## 3. Btrfs
```bash
mkfs.btrfs -L data /dev/sdb /dev/sdc            # multi-device defaults: data single (since 5.8), metadata raid1
mount -o compress=zstd:3,noatime /dev/sdb /mnt
btrfs subvolume create /mnt/@home
btrfs subvolume snapshot -r /mnt/@home /mnt/.snapshots/home-$(date +%F)
btrfs send /mnt/.snapshots/home-2026-10-15 | ssh backup btrfs receive /pool/home
btrfs filesystem usage /mnt                     # the only honest "df" for btrfs
btrfs scrub start -B /mnt                       # verify checksums monthly
btrfs balance start -dusage=50 /mnt             # reclaim half-empty chunks when "ENOSPC" with free space
```
- Use `btrfs filesystem usage` for space accounting; the balance documentation covers `usage=` filters for the case where balance returns ENOSPC.
- **RAID56 should not be used in production, only for evaluation or testing** (btrfs-man5, RAID56 status); prefer RAID1/RAID10 profiles.
- Disable CoW for chosen files or directories with `chattr +C` (NOCOW); this also implies no data checksums for those files.
- Mount subvolumes with `subvol=@home` in fstab; snapshots are subvolumes you can
  roll back by renaming/`set-default`.

## 4. OpenZFS
```bash
apt install zfsutils-linux                      # Ubuntu (OpenZFS Getting Started)
zpool create -o ashift=12 tank raidz2 /dev/disk/by-id/ata-* \
   -O compression=lz4 -O atime=off -O xattr=sa -O acltype=posix
zfs create tank/data
zfs set mountpoint=/srv/data tank/data
zfs snapshot tank/data@before-upgrade && zfs rollback tank/data@before-upgrade
zfs send -R tank/data@snap | ssh backup zfs receive -F pool/data
zpool scrub tank && zpool status -v
```
- Prefer persistent names such as `/dev/disk/by-id/` over `sdX` (OpenZFS FAQ recommends by-id for small pools).
- `ashift` defaults to auto-detect; set `ashift=12` when 4 KiB-sector disks report 512 B sectors (zpoolprops(7)). `recordsize` is designed for database workloads with fixed-size records; zfsprops(7) strongly discourages tuning it on general-purpose file systems.
- zfsprops(7): deduplication should not be enabled unless necessary; `compression=lz4` is a valid setting and `compression=on` selects the current default algorithm.

## Verify
- [ ] Pool/filesystem survives a reboot and mounts via fstab (or ZFS cache/`zfs-mount.service`).
- [ ] A snapshot taken, a file deleted, and the file restored from the snapshot.
- [ ] Capacity monitored at the **physical** layer (`vdostats`, `stratis pool list`,
      `btrfs fi usage`, `zpool list`) with an alert before 80 %.

## Checked
2026-10-27. Checked against the Stratis how-to (stratis-docs) and stratis-cli manual (docs/stratis.txt), lvmvdo(7) from lvm2, btrfs-progs documentation sources (mkfs.btrfs, Status, btrfs-man5 RAID56 section, mount options, balance filters, scrub), OpenZFS man pages (zpoolprops, zfsprops, zfs-send, zfs-receive), the OpenZFS FAQ and Ubuntu Getting Started. Confirmed: dnf install stratisd stratis-cli, stratis pool create, filesystem create and snapshot, pool add-data, key set and --key-desc; the fstab line with stratis-fstab-setup; lvcreate --type vdo -n -L -V, slow discard warning, vdostats and /dev/mapper names; Btrfs multi-device defaults (data single since 5.8, metadata raid1), subvolume snapshot -r, scrub -B, balance usage filter, RAID56 not for production, NOCOW implying no checksums; zpool create -o ashift, send -R and receive -F, acltype=posix, by-id naming advice. Changed: the Stratis fstab requirement (the documented form is x-systemd.requires=stratis-fstab-setup@<pool uuid>.service), mount -o discard on VDO, acltype=posixacl (documented value is posix). Removed: Stratis 1 TiB default and full-pool behaviour, VDO read-only and savings figures and LUKS advice, the Btrfs metadata-exhaustion explanation and fragmentation remark, ashift immutability wording, recordsize examples, the 5 GB per TB dedup figure, the 80 percent rule and DKMS remarks, none of which the documents confirm. Stratis snapshots are not described as writable because the manual does not say so.

Method: documentation only; no commands were run.
