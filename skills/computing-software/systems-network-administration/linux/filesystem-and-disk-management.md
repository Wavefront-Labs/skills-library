---
id: computing-software.systems-network-administration.linux.filesystem-and-disk-management
name: filesystem-and-disk-management
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, filesystem, disk, storage, lsblk, blkid, parted, gpt, lvm, pvcreate, vgextend, lvextend, lvresize, xfs, ext4, xfs-growfs, resize2fs, fstab, uuid, nofail, findmnt, mount, df, du, inodes, deleted-open-files, lsof, growpart, cloud-disk, smartctl, sysadmin]
level: practitioner
status: draft
description: "Add, partition, mount and grow Linux storage safely: lsblk/blkid, GPT, LVM, ext4 vs XFS resizing, fstab by UUID with nofail, and 'disk full' triage (inodes, deleted open files)."
sources:
  - https://man7.org/linux/man-pages/man8/lsblk.8.html
  - https://man7.org/linux/man-pages/man5/fstab.5.html
  - https://man7.org/linux/man-pages/man8/lvextend.8.html
  - https://man7.org/linux/man-pages/man8/xfs_growfs.8.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Filesystem and disk management — add, grow, mount, and find the missing space

**Goal:** attach new storage, put it under LVM, grow it online, mount it so a missing
disk can't brick the boot, and diagnose "disk full" correctly the first time.

## 1. Identify before you touch
```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,UUID   # tree of disks/partitions/LVs
blkid                                          # UUIDs and fs types
findmnt --real                                 # what is mounted where, with options
```
Device names (`/dev/sdb`, `/dev/nvme1n1`) are **not stable** across reboots or after
hot-adding disks in a VM. Always confirm size and serial (`lsblk -o +SERIAL`) before
`mkfs` — formatting the wrong disk is the classic irreversible mistake.

## 2. Partition + LVM a new disk
```bash
parted -s /dev/sdb mklabel gpt mkpart data 1MiB 100% set 1 lvm on
pvcreate /dev/sdb1
vgcreate vg_data /dev/sdb1
lvcreate -n lv_app -l 80%VG vg_data      # leave headroom for snapshots/growth
mkfs.xfs /dev/vg_data/lv_app              # or mkfs.ext4
```
Leaving 10-20% of the VG free is cheap insurance: you can grow a hot LV in seconds or
take an LVM snapshot before a risky upgrade.

## 3. Mount persistently — by UUID, with `nofail` for non-root data
```
# /etc/fstab
UUID=<UUID>  /srv/app  xfs  defaults,nofail,x-systemd.device-timeout=10s  0 0
```
```bash
mkdir -p /srv/app && systemctl daemon-reload && mount -a && findmnt /srv/app
```
**Always run `mount -a` (or `findmnt --verify`) after editing fstab.** A typo in fstab
without `nofail` can drop the box into emergency mode on the next reboot — painful on a
cloud VM with no console. Use `nofail` for anything not needed to boot.

## 4. Grow a filesystem online
Order matters: disk/partition → PV → LV → filesystem.
```bash
# cloud disk enlarged in the console:
growpart /dev/sdb 1          # from cloud-guest-utils / cloud-utils-growpart
pvresize /dev/sdb1
lvextend -r -l +100%FREE vg_data/lv_app   # -r resizes the filesystem too
```
Without `-r`: XFS uses `xfs_growfs /srv/app` (takes the **mount point**, online only);
ext4 uses `resize2fs /dev/vg_data/lv_app` (online grow works).
**XFS cannot shrink.** If you may ever need to shrink, use ext4 (offline shrink:
unmount, `e2fsck -f`, `resize2fs` to a smaller size, *then* `lvreduce`). Getting that
order wrong truncates the filesystem.

## 5. "Disk full" triage
```bash
df -hT                       # bytes
df -i                        # inodes — full inodes look like "No space left" with free GB
du -xh --max-depth=1 / | sort -h | tail     # -x stays on one filesystem
lsof -nP +L1                 # deleted-but-open files still holding space
```
- **`df` and `du` disagree** → a process holds a deleted file open (classic: a log
  rotated with `rm` instead of the app reopening it). Restart/reload that process, or
  truncate via `: > /proc/<PID>/fd/<FD>`.
- **Inodes exhausted** → millions of tiny files (session dirs, mail queues, cache).
  Find them with `find /path -xdev -type f | cut -d/ -f2-4 | sort | uniq -c | sort -n | tail`.
- ext4 reserves 5% of blocks for root by default; on large data volumes
  `tune2fs -m 1 /dev/...` reclaims space (keep the reserve on `/`).
- Something mounted *over* a non-empty directory hides the files underneath; `du` won't
  see them. Bind-mount `/` elsewhere (`mount --bind / /mnt/root`) to inspect.

## 6. Disk health
`smartctl -a /dev/sda` (smartmontools) for reallocated/pending sectors on physical
disks; `dmesg -T | grep -iE 'i/o error|blk_update'` for kernel-level errors. Not
meaningful on most cloud virtual disks.

**Uncertain/varies:** package names for `growpart` and default filesystems differ by
distro (RHEL family defaults to XFS, Debian/Ubuntu to ext4). Btrfs and ZFS have their
own grow/snapshot tooling not covered here.

## Verify
- [ ] `lsblk` shows the new LV at the expected size and filesystem.
- [ ] fstab entry uses `UUID=` and `nofail`; `findmnt --verify` reports no errors.
- [ ] `mount -a` succeeds and a test reboot (or `systemctl daemon-reload` + remount) brings it back.
- [ ] After growth, `df -h` shows the new size without unmounting.
- [ ] For a full disk you checked `df -i` and `lsof +L1`, not only `du`.
