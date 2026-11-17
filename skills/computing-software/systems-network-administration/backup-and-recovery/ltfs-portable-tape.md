---
id: computing-software.systems-network-administration.backup-and-recovery.ltfs-portable-tape
name: ltfs-portable-tape
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [ltfs, linear-tape-file-system, tape, archive, data-interchange, mkltfs, lto]
level: practitioner
status: docs-checked
description: "Use LTFS to treat LTO tapes as portable file systems: mkltfs, mount and copy, ordered copy for speed, index handling, ltfsck recovery and fitting use cases."
sources:
  - https://www.snia.org/tech_activities/standards/curr_standards/ltfs
  - https://www.ibm.com/docs/en/spectrum-archive-sde
  - https://github.com/LinearTapeFileSystem/ltfs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LTFS for portable tape

**Goal:** move or archive large datasets on tape in a vendor-neutral format any LTFS system can read.

## What LTFS is
A format specification defined by SNIA and, from version 2.2, published as ISO/IEC 20919 (version 2.5.1 is published as 20919:2021). It describes data placement, the shape of the index and extended attribute names, so tapes are self-describing. The open-source LTFS project is the reference implementation, and its drive support table starts at LTO-5.

## Format and mount (open-source LTFS or vendor builds)
```bash
ltfs -o device_list                      # find drives
mkltfs -d /dev/sg1 -s VOL001 -n project-x   # format (erases tape): -d device (required), -s 6-character tape serial, -n volume name; -f forces formatting a used medium
mkdir -p /mnt/ltfs
ltfs -o devname=/dev/sg1 /mnt/ltfs
rsync -av --progress /data/project-x/ /mnt/ltfs/project-x/
umount /mnt/ltfs                         # writes the final index; wait for it to finish
```

## Performance
- Prefer large sequential files over millions of small files (pack small files into archives first).
- `ltfs_ordered_copy` copies files with LTFS order optimization; it accepts a file list on stdin (for example from `find`) with `-t <target-dir>`.
- `mkltfs --rules` (for example `size=1M`) chooses which small files are written to the index partition.

## Recovery
`ltfsck <device>` is the recover and rollback utility for LTFS tapes (use it when a mount fails or the index was not written); `-l` lists rollback points, and `-r` with `-g <generation>` rolls back to an earlier index generation. `ltfs -o rollback_mount=<gen>` mounts a previous index generation read-only.

## Use cases
- Media and research data interchange (send tapes to partners).
- Long-term archive with a readable, documented format.
- Not a replacement for backup software: no catalog across tapes, retention, encryption management or deduplication by itself.

## Gotchas
- Check drive and media generation compatibility with the drive vendor before planning migrations.
- Unmounting without waiting for the index write can leave a tape needing `ltfsck`.

## Verify
Mount the tape on a different machine (ideally different vendor drive) and compare checksums of a sample of files.

## Checked

Checked 2026-10-27 against the open-source LTFS project (LinearTapeFileSystem/ltfs: README and the mkltfs, ltfsck, ltfs and ltfs_ordered_copy man pages). Confirmed: SNIA and ISO/IEC 20919 status of the format specification, `ltfs -o device_list` and `-o devname=`, `mkltfs -d/-s/-n/-f/-r`, `ltfsck` rollback options, `-o rollback_mount`, and `ltfs_ordered_copy` usage. Removed the unconfirmed LTO-9 read/write compatibility statement and the vendor Windows and macOS mount remark.

Method: documentation only; no commands were run.
