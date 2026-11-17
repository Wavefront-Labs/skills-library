---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.xfs-and-btrfs-forensics
name: xfs-and-btrfs-forensics
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [xfs-forensics, btrfs-forensics, linux-filesystems, xfs_db, btrfs-subvolumes, snapshots, dfir]
level: advanced
status: draft
description: "Examine XFS (RHEL default) and Btrfs (SUSE, Fedora, NAS) volumes read-only: inspection tools, timestamps, deleted data, subvolumes and snapshots."
sources: ["https://man7.org/linux/man-pages/man8/xfs_db.8.html", "https://btrfs.readthedocs.io/en/latest/", "https://www.sans.org/white-papers/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# XFS and Btrfs forensics

**Goal:** analyse Linux servers and NAS devices that do not use ext4. TSK support for these is
limited, so lean on native tools with read-only safeguards.

## Mounting safely
```bash
losetup -r -P -f --show image.dd          # read-only loop with partitions
mount -o ro,norecovery /dev/loop0p2 /mnt/xfs        # XFS: norecovery prevents log replay
mount -o ro,nologreplay /dev/loop0p3 /mnt/btrfs     # Btrfs: nologreplay (with ro)
```
Without `norecovery`/`nologreplay`, a dirty journal is replayed, which writes to the
device (blocked by a read-only loop, causing mount failure, or altering a writable copy).

## XFS
- Default on RHEL/CentOS/Rocky 7+. Allocation groups, B+tree inodes, metadata journal.
- Timestamps: atime, mtime, ctime; **crtime** (birth) on v5 filesystems; nanosecond; v5 with
  `bigtime` extends range past 2038. `stat` on a mounted fs or
  `xfs_db -r -c "inode <n>" -c print /dev/loop0p2` for raw inode fields (`v3.crtime`).
- `xfs_db -r` (read-only) to walk inodes and directories; `xfs_logprint` to read the log for
  recent metadata changes.
- Deleted files: XFS clears extent information in freed inodes quickly; recovery relies on
  carving and log remnants. Plan on carving (`photorec`, `bulk_extractor`).
- Recent TSK releases add partial XFS support; verify with a test image before relying on it.

## Btrfs
- Copy-on-write B-trees, subvolumes and snapshots (openSUSE snapper, Synology, Fedora).
```bash
btrfs subvolume list -s /mnt/btrfs        # snapshots (snapper keeps .snapshots/<n>/snapshot)
btrfs inspect-internal dump-super /dev/loop0p3
btrfs inspect-internal dump-tree -t <tree> /dev/loop0p3   # raw trees, includes old generations
btrfs restore -D -v /dev/loop0p3 /out     # -D dry run; restore can read older tree roots (-t)
btrfs-find-root /dev/loop0p3              # list older tree roots for historic views
```
- Snapshots are your VSS equivalent: diff files between them to find changes. Snapper also logs
  each snapshot's trigger (`/.snapshots/<n>/info.xml`, often package installs via zypper).
- CoW means old data blocks often survive; older tree roots let `btrfs restore` recover
  deleted files.
- Timestamps include `otime` (birth) on Btrfs.

## Gotchas
- Never run `xfs_repair` or `btrfs check --repair` on evidence.
- NAS RAID (Synology SHR = md + LVM + Btrfs) must be assembled first; see RAID/LVM reconstruction.

## Self-check
The volume was mounted with replay disabled, birth times were captured, and snapshots or older
tree roots were checked before concluding data is gone.
