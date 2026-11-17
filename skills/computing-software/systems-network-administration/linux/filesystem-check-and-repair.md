---
id: computing-software.systems-network-administration.linux.filesystem-check-and-repair
name: filesystem-check-and-repair
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, fsck, e2fsck, xfs-repair, xfs-metadump, filesystem-repair, filesystem-corruption, superblock, lost-found, journal-replay, read-only-remount, ddrescue, data-recovery, ext4, xfs, btrfs-check, storage, sysadmin, fsck-mode]
level: practitioner
status: docs-checked
description: "Check and repair ext4/XFS filesystems safely: when fsck runs at boot, e2fsck and xfs_repair flags, backup superblocks, lost+found, and imaging the disk before destructive repair."
sources:
  - https://man7.org/linux/man-pages/man8/e2fsck.8.html
  - https://man7.org/linux/man-pages/man8/xfs_repair.8.html
  - https://man7.org/linux/man-pages/man8/fsck.8.html
  - https://www.gnu.org/software/ddrescue/manual/ddrescue_manual.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Filesystem check and repair: fix metadata without making it worse

**Goal:** get a filesystem that went read-only, refuses to mount, or complains in `dmesg`
back to a clean, mountable state, and know when to stop and image the disk instead.

## 0. Triage before touching anything
- Check kernel messages and the mount options (`dmesg -T`, `findmnt`) to separate filesystem errors from disk I/O errors.
- **Disk I/O errors or failing SMART attributes mean the disk is dying.** Image it first with GNU ddrescue
  (`ddrescue <infile> <outfile> <mapfile>`) and repair the image, not the disk.
- Pure metadata inconsistencies (unexpected power loss) are repaired in place after unmounting.
- Never repair a **mounted** filesystem. For `/`, use rescue media or the initramfs, since root stays mounted in
  normal operation.

## 1. ext4: e2fsck
```bash
umount /dev/vg/data
e2fsck -n /dev/vg/data          # report only; opens read-only and makes no changes
e2fsck -f -y /dev/vg/data       # force a check even if clean; answer yes to all fixes
e2fsck -p /dev/vg/data          # preen: fix only problems that are safe to fix automatically
```
- `-b superblock` uses an alternate superblock when the primary is damaged (get backup locations from `mke2fs -n`,
  which is not covered by the sources here).
- Unreferenced inodes are reconnected into `lost+found`.
- `-y` answers yes to every question and can destroy data on a failing disk; image first.
- Boot-time checking order comes from the sixth `/etc/fstab` field (`fs_passno`); see fsck(8).

## 2. XFS: xfs_repair
```bash
umount /data
xfs_repair -n /dev/sdb1          # no-modify mode: report only
xfs_repair /dev/sdb1             # repair
```
- A dirty log can only be replayed by mounting the filesystem. If `xfs_repair` reports a dirty log, mount and unmount
  once so it replays. `-L` forces log zeroing and loses the un-replayed metadata changes: last resort.
- `-m maxmem` limits memory use (megabytes); `-P` disables prefetching of inode and directory blocks, which reduces
  memory use if it runs out.
- Disconnected inodes are placed in `lost+found`.

## 3. After repair
```bash
mount /dev/vg/data /data && ls /data/lost+found
```
Restore known-good files from backup where application data was corrupted; a repair makes metadata consistent, it
does not make file contents correct. Btrfs has its own tooling (`btrfs check`, `btrfs scrub`); read the btrfs
documentation before using any repair mode.

## Failure modes
- Running `e2fsck -y` on a dying disk: image first.
- `xfs_repair -L` as a reflex: it discards the log that would have made the filesystem consistent.
- Repairing the wrong device under LVM/RAID: always check the top-level LV or md device, never a PV or RAID member.

## Verify
- [ ] `e2fsck -n` / `xfs_repair -n` after the repair reports no errors.
- [ ] Filesystem mounts read-write; `dmesg` stays quiet under load.
- [ ] `lost+found` reviewed; critical data compared with backups.

## Checked
2026-10-28. Confirmed in the e2fsck(8), xfs_repair(8), fsck(8) man pages and the GNU ddrescue manual: `-n`, `-p`, `-y`,
`-b superblock`, `lost+found`, XFS `-n`, `-L`, `-m`, `-P`, dirty-log replay by mounting, the `fs_passno` sixth field.
Removed as unconfirmed: the Red Hat chapter in `sources` (404, dropped), `tune2fs` options, `fsck.mode` and `fsck.repair`
kernel parameters, `xfs_metadump`, the RAM-per-TiB rule, the Btrfs repair advice, `nofail`.
Method: documentation only; no commands were run.
