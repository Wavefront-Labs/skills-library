---
id: computing-software.systems-network-administration.linux.mkfs-xfs-options-and-xfs-admin
name: mkfs-xfs-options-and-xfs-admin
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, filesystems, xfs, mkfs-xfs, xfs-admin, xfs-info, xfs-growfs, su-sw, reflink, xfs-label, rhcsa, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Create XFS filesystems with sensible options (su/sw for RAID, reflink, log size, labels), inspect them with xfs_info, change label/UUID with xfs_admin, and grow online."
sources:
  - https://git.kernel.org/pub/scm/fs/xfs/xfsprogs-dev.git/plain/man/man8/mkfs.xfs.8.in
  - https://git.kernel.org/pub/scm/fs/xfs/xfsprogs-dev.git/plain/man/man8/xfs_admin.8
  - https://git.kernel.org/pub/scm/fs/xfs/xfsprogs-dev.git/plain/man/man8/xfs_growfs.8
  - https://git.kernel.org/pub/scm/fs/xfs/xfsprogs-dev.git/plain/man/man8/xfs_repair.8
  - https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/xfs.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mkfs.xfs and xfs_admin

**Goal:** XFS created with geometry that suits the storage underneath, plus the
label/UUID/growth operations you'll need later (XFS can grow but never shrink).

## 1. Create
```bash
mkfs.xfs -L data /dev/vg0/data                     # defaults are good on LVM/single disks
mkfs.xfs -d su=64k,sw=4 -L data /dev/md0           # RAID: stripe unit = chunk, stripe width = data disks
mkfs.xfs -f /dev/sdb1                              # overwrite existing signature (be sure!)
mkfs.xfs -m reflink=1,crc=1 /dev/sdb1              # reflink (cp --reflink, deduplication); on by default in current mkfs.xfs, needs crc=1
mkfs.xfs -l size=256m /dev/sdb1                    # bigger log for metadata-heavy loads
mkfs.xfs -n size=64k /dev/sdb1                     # larger directory blocks for huge directories
mkfs.xfs -N /dev/sdb1                              # dry run: print geometry only
```
On a block device mkfs.xfs queries the device for appropriate sunit/swidth; `-d noalign` disables
that detection. Set `su`/`sw` by hand if the device does not report its geometry. `-i maxpct=`
sets the maximum percentage of space used for inodes.

## 2. Inspect
```bash
xfs_info /data                 # geometry (mounted: pass mount point; unmounted: device)
xfs_db -r -c 'sb 0' -c 'p uuid label' /dev/sdb1
```

## 3. Change with xfs_admin
```bash
umount /data
xfs_admin -L newlabel /dev/sdb1
xfs_admin -U generate /dev/sdb1        # new UUID (cloned LUN/snapshot); on a CRC filesystem this sets an incompatible flag (see xfs_admin(8), `-U restore`)
xfs_admin -l -u /dev/sdb1              # print label and UUID
xfs_admin -c 1 /dev/sdb1               # enable lazy-counters (old fs)
```
Quick alternative for a cloned fs on the same host: mount with `-o nouuid` once.

## 4. Grow (online)
```bash
lvextend -L +50G /dev/vg0/data
xfs_growfs /data               # mounted, by mount point
# or in one step: lvextend -r -L +50G /dev/vg0/data
```
Shrinking isn't supported: back up, recreate smaller, restore.

## Gotchas
- Duplicate UUID (snapshot mounted beside origin) → "Filesystem has duplicate UUID … can't mount": `nouuid` or `xfs_admin -U generate`.
- `xfs_repair` needs an unmounted filesystem; `-L` zeroes a dirty log even though it contains metadata changes (see the DIRTY LOGS section of xfs_repair(8)).
- The data section must be at least 300 MiB (mkfs.xfs(8)); use another filesystem for tiny volumes.

## Verify
- [ ] `xfs_info` shows expected sunit/swidth (in blocks) and `reflink=1` if wanted.
- [ ] `blkid /dev/sdb1` shows the new LABEL/UUID; fstab references match.
- [ ] `df -h` reflects growth after `xfs_growfs`.

## Checked
Checked 2026-10-26 against the xfsprogs-dev master man pages (mkfs.xfs, xfs_admin, xfs_growfs, xfs_repair) and the kernel XFS admin guide.
Confirmed: `-L`, `-f`, `-N`, `-d su=,sw=`, `-m reflink=,crc=`, `-l size=`, `-n size=`, `-i maxpct=`; automatic sunit/swidth query and `-d noalign`; reflink created by default and needing CRCs; 300 MiB minimum data section; `xfs_admin -L`, `-U generate` (incompatible flag on CRC filesystems), `-l`, `-u`, `-c 1` lazy-counters; xfs_growfs needs a mounted filesystem; the nouuid mount option; xfs_repair -L.
Removed as unconfirmed: the RHEL 9 / xfsprogs 5.1 default-version statement, the dynamic-inode remark and xfsdump attribute handling.
Method: documentation only; no commands were run.
