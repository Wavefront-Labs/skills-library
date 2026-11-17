---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.reparse-points-junctions-and-symlinks
name: reparse-points-junctions-and-symlinks
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [reparse-points, ntfs, symbolic-links, onedrive-forensics, dfir]
level: advanced
status: docs-checked
description: "Interpret NTFS reparse points (symlinks, junctions, mount points, cloud placeholders) in forensics: tags, what they imply for content, and collection cautions."
sources: ["https://learn.microsoft.com/en-us/windows/win32/fileio/reparse-points", "https://learn.microsoft.com/en-us/windows/win32/fileio/reparse-point-tags"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reparse points, junctions and symlinks

**Goal:** reparse points redirect or reinterpret file system access. They explain "phantom" paths, cloud placeholder files with no local content, and some attacker tricks.

## What a reparse point is
- A file or directory can carry a reparse point: user-defined data plus a reparse tag that identifies the data format. A file system filter that understands the tag processes the file; if no filter is found, the open fails.
- Reparse points implement NTFS file system links and mounted folders, and stub files for storage tiering (Microsoft's example is Remote Storage Server, where the stub's reparse data points to where the real file now lives).
- A directory must be empty to get a reparse point. Reparse points and extended attributes are mutually exclusive on a file. Reparse data (tag and optional GUID) cannot exceed 16 KB. There is a limit of 63 reparse points on any given path (31 if the reparse point targets a fully qualified path).
- Reading the tag: `FindFirstFile` returns `FILE_ATTRIBUTE_REPARSE_POINT` in `dwFileAttributes`; `dwReserved0` then holds the tag.
- The tag is a DWORD. Its low 16 bits say what kind of reparse point it is. Top bits include the Microsoft bit (tag owned by Microsoft) and the name surrogate bit (the file or directory represents another named entity in the system).

## Common Microsoft-defined tags (WinNT.h names)
| Tag | Forensic meaning |
|---|---|
| `IO_REPARSE_TAG_SYMLINK` | Symbolic link |
| `IO_REPARSE_TAG_MOUNT_POINT` | Junction or volume mount point |
| `IO_REPARSE_TAG_CLOUD` and `IO_REPARSE_TAG_CLOUD_1` to `_F` | Cloud files placeholders (content may not be local) |
| `IO_REPARSE_TAG_ONEDRIVE` | OneDrive |
| `IO_REPARSE_TAG_APPEXECLINK` | App execution link |
| `IO_REPARSE_TAG_WOF` | Windows Overlay Filter (compressed files) |
| `IO_REPARSE_TAG_DEDUP` | Data deduplication |
| `IO_REPARSE_TAG_AF_UNIX` | AF_UNIX socket |

Microsoft's tag page lists many more (DFS, HSM, SIS, PROJFS, WIM and others). Look the tag up there rather than guessing, and get numeric values from WinNT.h.

## Forensic implications
- **Cloud placeholders:** a file whose record carries a cloud tag may have no local content. Do not claim the user opened it locally without other evidence.
- **Dedup and other filter-backed files:** content is produced by a filter driver, so an acquisition tool that does not understand the tag may not return the real data. Test a sample file before relying on a copy.
- **Abuse:** symlinks and junctions can redirect file writes or hide data in unexpected locations. Treat an unexplained link as a lead and confirm it with other artefacts.
- Timelines can show duplicate paths when a tool follows junctions.

## Gotchas
- Following links during collection can duplicate data or loop. Collectors should record reparse points rather than follow them.

## Verify
For any file whose content matters, confirm it is not a placeholder, filter-backed stub or link to elsewhere, and record the tag you saw.

## Checked
Date: 2026-11-08.
Read in full: Microsoft Learn "Reparse points" and "Reparse Point Tags" (win32/fileio).
Confirmed: reparse point definition and filter behaviour, restrictions (empty directory, no extended attributes, 16 KB, 63/31 path limit), tag retrieval via FindFirstFile, tag bit layout (Microsoft bit, name surrogate bit), the listed tag names (SYMLINK, MOUNT_POINT, CLOUD and CLOUD_1 to _F, ONEDRIVE, APPEXECLINK, WOF, DEDUP, AF_UNIX).
Removed: hex tag values, the `$Extend\$Reparse` index and `$REPARSE_POINT` 0xC0 attribute details, `fsutil`, `dir /AL` and `istat` usage, the WindowsApps, CompactOS and chunk-store location claims, object-manager symlink claims, and the Sleuth Kit source (its home page says nothing about reparse points).
Method: documentation only; no commands were run.
