---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.recovering-ext4-data-via-the-journal
name: recovering-ext4-data-via-the-journal
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [ext4-journal, ext4-forensics, jls, linux-forensics, dfir]
level: advanced
status: docs-checked
description: "Inspect the ext3/ext4 JBD2 journal with jls and debugfs logdump to find earlier copies of metadata blocks, and know what debugfs undelete cannot do."
sources: ["https://www.kernel.org/doc/html/latest/filesystems/ext4/journal.html", "https://manpages.debian.org/testing/e2fsprogs/debugfs.8.en.html", "https://www.sleuthkit.org/sleuthkit/man/jls.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting the ext4 journal for earlier metadata

**Goal:** the ext3/ext4 journal can still hold older copies of metadata blocks. Find which journal records refer to a block of interest and dump them. The debugfs manual states that `lsdel` (`list_deleted_inodes`) is not useful for recovering files deleted on ext3 or ext4, because the inode's data blocks are no longer available after the inode is released.

## Journal layout (kernel documentation)
- The journal inode is typically inode 8 and is a normal but hidden file; the first 68 bytes of the journal inode are replicated in the ext4 superblock.
- A transaction begins with a descriptor block followed by data blocks, or with a revocation list, and a finished transaction ends with a commit block. A transaction with no commit record (or mismatched checksums) is discarded during replay.
- A descriptor block holds tags describing the final on-disk locations of the data blocks that follow it. Revocation blocks stop replay of a block journalled in an earlier transaction, typically a metadata block that was freed and reallocated as file data.

## Inspect the journal
```bash
jls -o <sector_offset> image.dd                    # journal block numbers and descriptions
jls -f linux-ext3 img.dd                           # example form from the manual
debugfs -R "logdump -a" image.dd > logdump.txt     # print descriptor blocks of the journal
debugfs -R "logdump -b <block>" image.dd           # journal records that refer to a given block
debugfs -R "logdump -O" image.dd                   # also show old (checkpointed) entries
debugfs -R "logdump -S" image.dd                   # journal superblock
```
- `jls` takes `-f fstype`, `-i imgtype`, `-o imgoffset` (sector offset of the file system), `-b dev_sector_size`, `-v`, and an optional journal inode argument.
- `logdump -c` prints the contents of the data blocks selected by `-a` and `-b`; `-n num_trans` continues past a journal block missing a magic number; `-i filespec` selects a different journal inode; `-f` reads a regular file containing journal data; `-s` locates the journal via backup information in the superblock.
- debugfs opens the file system read-only unless `-w` is given; `-c` (catastrophic mode) also forces read-only.

## Directory history
`debugfs -R "ls -d /path" image.dd` lists deleted entries in a directory (`-l` gives a verbose listing).

## Gotchas
- Checkpointed entries may no longer reflect current state; `logdump -O` shows old entries.

## Verify
Each recovered artefact is tied to a journal transaction or block reference in the logdump output.

## Checked
Checked 2026-11-09 against the kernel ext4 journal page, the debugfs manual (logdump, ls, lsdel, open options) and the jls manual. Removed: ext4magic commands and flags, the "journal is small, often 128 MB" and circular-overwrite statements, `data=ordered` explanation, extundelete claims, the claim that the inode extent tree is recovered from older inode-table copies, and the earlier `logdump -i <inode>` usage (the manual defines `-i filespec` as the journal inode source).
Method: documentation only; no commands were run.
