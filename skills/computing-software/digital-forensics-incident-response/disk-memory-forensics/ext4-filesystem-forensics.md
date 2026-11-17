---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.ext4-filesystem-forensics
name: ext4-filesystem-forensics
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [ext4-forensics, filesystem-forensics, linux-forensics, inodes, jbd2, debugfs, dfir]
level: advanced
status: docs-checked
description: "Examine ext4 images: partition layout, superblock, inode times including crtime and dtime, and the jbd2 journal, using Sleuth Kit tools and debugfs."
sources: ["https://www.kernel.org/doc/html/latest/filesystems/ext4/index.html", "https://www.kernel.org/doc/html/latest/filesystems/ext4/inodes.html", "https://www.kernel.org/doc/html/latest/filesystems/ext4/journal.html", "https://www.sleuthkit.org/sleuthkit/man/mmls.html", "https://www.sleuthkit.org/sleuthkit/man/fsstat.html", "https://www.sleuthkit.org/sleuthkit/man/istat.html", "https://www.sleuthkit.org/sleuthkit/man/icat.html", "https://man7.org/linux/man-pages/man8/debugfs.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ext4 filesystem forensics

**Goal:** extract timeline and metadata evidence from Linux ext4 volumes.

## Orientation
```bash
mmls disk.raw                       # partition layout, incl. unallocated sectors
fsstat -o 2048 disk.raw             # superblock details: mount times, features, group layout
fls -o 2048 -r -p -m / disk.raw > body.txt   # bodyfile, recursive, full paths
istat -o 2048 disk.raw 1311234      # inode: uid, gid, mode, size, link count, times, blocks
icat -r -o 2048 disk.raw 1311234 > out.bin   # -r tries recovery if the file is deleted
```
- `mmls` shows sectors not in any partition, which can be searched for hidden data. `-o` is the
  sector offset where the file system starts.
- `istat -B num` shows num block addresses; useful for an unallocated inode of size 0 that still
  has block pointers.
- `istat -z` and `-s` set the original system's time zone and clock skew.
- Read-only alternative: `debugfs -c -R 'stat <1311234>' partition.img` (`-c` opens in
  catastrophic mode, read-only).

## Timestamps
The inode holds access, change, modification and deletion times (`i_atime`, `i_ctime`, `i_mtime`,
`i_dtime`) plus a creation time (`i_crtime`). The extra fields give nanosecond resolution.
`debugfs stat` reports crtime and dtime; the `stat()` system call does not. Inode records are
256 bytes by default (`s_inode_size`; the part past the original 128 bytes is `i_extra_isize`).

## Journal (jbd2)
- The journal inode is typically inode 8; the journal is a hidden file. Journal fields are
  big-endian, ext4 fields little-endian.
- Default `data=ordered` journals metadata only, so file data blocks are not guaranteed consistent
  after a crash; `data=journal` journals data as well.
- Structure: journal superblock (magic `0xC03B3998` in each block header), descriptor blocks,
  data blocks, revocation blocks and a commit block. A transaction without a commit record, or
  with mismatched checksums, is discarded on replay. The commit block holds `h_commit_sec`,
  the commit time in seconds since the epoch.
- `debugfs -c -R 'logdump -a' partition.img` dumps the journal contents. Check
  `man debugfs` on your version for `logdump` options such as `-O`.

## Gotchas
- Open images read-only (`debugfs -c`, Sleuth Kit tools) rather than mounting them.
- `debugfs lsdel` is not useful on ext3/ext4.
- Layers such as LVM or LUKS sit below the file system and must be handled first.
- Other file systems need their own tools; do not assume ext4 behaviour applies.

## Checked
Date: 2026-11-07.
Read in full: kernel.org ext4 inodes and journal pages (and the high-level design overview), the Sleuth Kit man pages for mmls, fsstat, istat and icat (plus fls earlier), and the debugfs man page.
Confirmed: the commands and flags above, the inode time fields and nanosecond extras, the 256-byte default, the journal layout, magic number, big-endian and ordered-mode statements, and that debugfs reports crtime and dtime.
Trimmed: extent zeroing on delete, ext4magic and extundelete recovery, PhotoRec and bulk_extractor carving, mount `noload`, the noatime/relatime note, the XFS/Btrfs remark, `fsstat` last-mount path and the Verify step, as none are stated on these pages.
Method: documentation only; no commands were run.
