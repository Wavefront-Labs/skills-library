---
id: computing-software.systems-network-administration.backup-and-recovery.change-journal-and-archive-bit-detection
name: change-journal-and-archive-bit-detection
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [change-journal, archive-bit, usn-journal, incremental-detection, file-level-backup]
level: advanced
status: docs-checked
description: "Understand how file backups detect changes: the archive bit, NTFS USN change journal and timestamp scans, and the trade-offs of each."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/fileio/change-journals
  - https://learn.microsoft.com/en-us/windows/win32/fileio/file-attribute-constants
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/fsutil-usn
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Change journal and archive bit detection

File-level incremental backups need to know which files changed. Methods, oldest to newest:

## Archive bit
- `FILE_ATTRIBUTE_ARCHIVE` (0x20) marks a file or directory as an archive file; Windows documents that applications typically use it to mark files for backup or removal.
- Only one backup product should rely on it: if two tools clear the bit, one of them will miss files. Any application or user can also clear it.

## Timestamp and size scan
Compare modification time and size with the catalog. Works on any filesystem but must walk the whole tree, so millions of files mean long scans. Microsoft describes scanning the whole volume as the brute-force method and notes the performance cost.

## Directory change notifications
Registering with `FindFirstChangeNotification` or `ReadDirectoryChangesW` is cheaper than a scan, but the application must run at all times, and watching many directories costs processing and memory.

## NTFS USN change journal
- NTFS keeps an update sequence number (USN) change journal per volume. On any file or directory change it records a description of the change and the name of the object. Backup tools read the journal instead of scanning.
- `fsutil usn queryjournal <volume>` shows the current journal, its records and its capacity; `fsutil usn readjournal` reads the records.
- The journal is truncated once it exceeds `maxsize` plus `allocationdelta`, so a journal too small for the change volume between backups loses history. `fsutil usn createjournal m=<maxsize> a=<allocationdelta> <volume>` on an existing journal updates those two values without disabling it.
- Do not delete the journal casually: `fsutil usn deletejournal` is slow and forces FRS and the Indexing Service to rescan the volume.
- Each journal has an unsigned 64-bit identifier; read the "Using the Change Journal Identifier" topic before building a tool that relies on stored USN positions.

## Choosing and verifying
Prefer the journal on large NTFS file servers. Periodically run a full scan or full backup to catch any missed changes.

## Checked

2026-11-09. Confirmed against the Windows "Change Journals" page, "File Attribute Constants" and the `fsutil usn` reference: archive attribute value and purpose, brute-force scan and notification trade-offs, USN journal contents, `queryjournal`/`readjournal`/`createjournal` parameters and truncation rule, deletejournal caution, 64-bit journal identifier. Removed: claims about restic ctime/inode checks, `touch -d`, ZFS/Btrfs/NetApp/PowerScale/VMware CBT snapshot diffs, clear-after-backup behaviour of the archive bit, journal wrap and ID-change fallback, and `attrib` usage (none of these appear on the cited pages).

Method: documentation only; no commands were run (2026-11-09).
