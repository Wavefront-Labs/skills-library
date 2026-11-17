---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.macos-fsevents-analysis
name: macos-fsevents-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [fsevents, macos, fseventsd, file-system-history, mac-apt, fseventsparser, dfir]
level: practitioner
status: draft
description: "Parse macOS FSEvents (.fseventsd) logs to reconstruct file creation, rename, deletion and volume mounts, including files long since removed."
sources: ["https://github.com/dlcowen/FSEventsParser", "https://github.com/ydkhatri/mac_apt", "https://developer.apple.com/documentation/coreservices/file_system_events"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FSEvents analysis

**Goal:** recover a history of file system changes on a Mac (and on USB volumes it wrote to)
that persists after files are deleted.

## Where
- `/System/Volumes/Data/.fseventsd/` (macOS 10.15+, Data volume) or `/.fseventsd/` on older
  systems and on every writable external volume the Mac mounted.
- Files are gzip-compressed pages named by hex event ID (`0000000001a2b3c4`), plus
  `fseventsd-uuid`. Headers `1SLD` (older), `2SLD` (adds node IDs, 10.13+) and `3SLD` (macOS 13+).

## Parse
```bash
python FSEParser_V4.1.py -s /mnt/data/.fseventsd -o out -t folder    # TSV + SQLite, reports and filters
python mac_apt.py -i image.E01 -o out E01 FSEVENTS
```
Collect the folder with root privileges (live: `sudo cp -Rp /System/Volumes/Data/.fseventsd`)
or from an image. Full Disk Access is needed for live collection tools.

## Record contents
Each record: full **path**, **event ID** (monotonic), **flags** (Created, Removed, Renamed,
Modified, InodeMetaMod, FinderInfoMod, ChangeOwner, XattrMod, IsFile/IsDir/IsSymlink, Mount,
Unmount, EndOfTransaction), and node ID (2SLD+).

## Timing (the main caveat)
Records carry **no timestamp**. Approximate time by:
- The gzip file's modification time (when the page was flushed): all records in that file
  occurred before it, after the previous file's mtime.
- Correlating event IDs with paths whose times you know (e.g. a file with a known birth time,
  unified log entries, system log rollovers).
Report times as ranges.

## Uses
- Deleted attacker tools and staging directories (`/tmp/.x/`, `~/Library/...`).
- Downloads and `com.apple.quarantine` xattr changes (XattrMod) on downloaded files.
- Mount/Unmount of `/Volumes/<name>`: external media and disk images (DMG) usage.
- Trash activity (`/.Trashes`, `~/.Trash`) and renames used to masquerade files.
- Document access patterns for insider cases.

## Gotchas
- macOS purges old pages; coverage varies from weeks to months depending on activity.
- High-churn paths (caches, Spotlight) dominate; filter out noise early.
- Event ID wraparound/reset after OS reinstall; check `fseventsd-uuid`.

## Self-check
Each finding has path, flags, event ID and a bounded time range with the source file's mtime
stated.
