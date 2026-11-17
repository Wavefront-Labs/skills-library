---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.hfs-plus-forensics
name: hfs-plus-forensics
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [hfs-plus, filesystem-forensics, macos-forensics, the-sleuth-kit, dfir]
level: advanced
status: draft
description: "Examine HFS+ volumes from older Macs, Time Machine disks and iPods: catalog B-tree, journal, extended attributes, dates since 1904 and TSK support."
sources: ["https://developer.apple.com/library/archive/technotes/tn/tn1150.html", "https://www.sleuthkit.org/sleuthkit/docs/api-docs/4.2/fspage.html", "https://github.com/libyal/libfshfs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HFS+ forensics

**Goal:** HFS+ (Mac OS Extended) predates APFS (2017). It still appears on older Macs, external
drives formatted Mac OS Extended, Time Machine backups to HFS+ disks, and some media devices.

## Structures (Apple TN1150)
| Structure | Content |
|---|---|
| Volume header (offset 1024) | Signature `H+` (0x482B) or `HX` (HFSX case-sensitive), block size, file counts, dates |
| Catalog file (B-tree) | Every file/folder record: CNID, parent, name, create/content-mod/attribute-mod/access/backup dates |
| Extents overflow file | Extra extents for fragmented files |
| Attributes file | Extended attributes: `com.apple.quarantine`, `com.apple.metadata:kMDItemWhereFroms` (download URL), resource forks, compression (`com.apple.decmpfs`) |
| Journal (`.journal`) | Metadata changes; recent catalog states, deleted records |

Dates are seconds since **1904-01-01** (local time for the volume header create date, GMT for catalog records).

## Tools
```bash
fsstat -f hfs image.dd               # TSK reports HFS+ details
fls -r -f hfs -p image.dd            # list files incl. deleted catalog entries where recoverable
icat -f hfs image.dd <CNID>          # extract by catalog node ID
fsck_hfs -n /dev/diskN (macOS, read-only check)
```
- libfshfs (`fshfsinfo`, `fshfsmount`) for read-only FUSE mounting.
- Plaso parses HFS+ via dfVFS for timelines.

## Investigative notes
- `kMDItemWhereFroms` xattr gives download source URLs; `com.apple.quarantine` gives agent and time.
- HFS+ compressed files (decmpfs) store data in the resource fork/xattr; naive tools show zero-size files.
- Deleted files: catalog B-tree nodes are rebalanced, so deleted records disappear quickly; the journal and unallocated nodes may retain them - carve catalog leaf nodes.

## Gotchas
- Case-sensitive HFSX volumes can hold files differing only by case.
- Time Machine on HFS+ uses directory hard links; naive copies explode in size.

## Verify
Dates are converted from the 1904 epoch with correct time-zone handling and checked against a known file.
