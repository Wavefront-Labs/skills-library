---
id: computing-software.systems-network-administration.linux.ext4-forensics-and-undelete-with-debugfs
name: ext4-forensics-and-undelete-with-debugfs
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, debugfs, ext4, undelete, file-recovery, inode, e2fsprogs, extundelete]
level: advanced
status: docs-checked
description: "Inspect and rescue data on ext4 with debugfs: open read-only, stat inodes and extents, lsdel, dump files by inode, find which file owns a bad block, and when to use other tools."
sources:
  - https://github.com/tytso/e2fsprogs/blob/master/debugfs/debugfs.8.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# debugfs on ext4

## Work on a copy or read-only
Unmount first (or work on an image). `debugfs` opens the filesystem read-only by default; `-w` opens read-write — avoid.
```bash
debugfs /dev/vg/data           # or an image file
debugfs -c /dev/vg/data        # catastrophic mode: inode and group bitmaps are not read; forces read-only
```
## Useful commands
```
stats                       superblock summary
ls -l /var/lib/app          list a directory (-l long format)
stat <123456>               inode details: mode, times (incl. dtime), size, extents
blocks <123456>             data blocks of an inode
icheck 987654               which inode owns block 987654 (e.g. from a dmesg I/O error)
ncheck 123456               path(s) for an inode
lsdel                       list deleted inodes (alias of list_deleted_inodes)
dump <123456> /mnt/rescue/file.bin      copy inode contents out
rdump /var/lib/app /mnt/rescue          recursive copy of a directory
logdump                     journal contents
```
## Undelete
`debugfs` has `undel <inode> [pathname]`, but success depends on the state of the filesystem after the delete. Stop writing to the filesystem immediately and prefer restoring from backup.

## Bad block → file
dmesg `I/O error, dev sdb, sector 123456789` → convert to fs block: `(sector − partition start sector) × 512 / blocksize`,
then `icheck <block>` → `ncheck <inode>` → restore that file from backup.

## Verify
- [ ] Recovered files' checksums/contents validated; original device never mounted read-write during recovery.

## Checked

2026-10-26. e2fsprogs master (last commit 2026-09-07) debugfs(8): read-only default and -w, -c catastrophic mode (bitmaps not read, forced read-only), commands stat, blocks, icheck, ncheck, dump, rdump, logdump, ls -l, undel, list_deleted_inodes with alias lsdel, show_super_stats alias stats. Removed unconfirmed statements about ext4 zeroing extents and about extundelete, ext4magic, photorec and ddrescue. The sector-to-block conversion is arithmetic and was not checked against a source.

Method: documentation only; no commands were run.
