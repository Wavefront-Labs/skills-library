---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.apfs-forensics
name: apfs-forensics
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [apfs-forensics, apfs, macos, snapshots, apfs-fuse, sleuthkit, encryption, dfir]
level: advanced
status: draft
description: "Examine APFS containers and volumes: snapshots, encryption, copy-on-write effects, and tools (APFS-fuse, TSK pool support, mac_apt) for disk images."
sources: ["https://developer.apple.com/support/downloads/Apple-File-System-Reference.pdf", "https://github.com/sgan81/apfs-fuse", "https://github.com/ydkhatri/mac_apt"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# APFS forensics (snapshots, encryption, copy-on-write)

**Goal:** get from a Mac or iOS-family disk image to examinable files and metadata, using APFS
features (snapshots, checkpoints) rather than fighting them.

## Layout
- One **container** (GPT partition type `7C3457EF-...`) holds several **volumes** sharing
  space: on macOS 10.15+ a read-only *System* volume and a writable *Data* volume (firmlinked),
  plus Preboot, Recovery, VM.
- Copy-on-write: modified data goes to new blocks; old blocks become free but are often
  intact until reused. Container checkpoints (superblock history) and object maps let tools
  rebuild older states of the filesystem tree.

## Encryption
- FileVault on Intel with T2 and on Apple silicon: the Data volume is hardware-encrypted; an
  image of the raw disk without keys is useless. Acquire live (logical collection while
  unlocked) or obtain the password/recovery key.
- With a password/recovery key: `apfs-fuse -r <recovery-key> image.dd /mnt/apfs` or
  `apfs-fuse` prompting for the password; TSK `fls -P apfs -B <block> -k <password>` on recent
  versions.

## Tools
```bash
mmls image.dd                                   # find the container partition
pstat -o <offset> image.dd                      # TSK pool (container) and volume list
fls -o <offset> -P apfs -B <vol-block> image.dd # list a specific volume
apfs-fuse -o ro image.dd /mnt/apfs              # FUSE mount (Linux), -v <n> to choose volume
python mac_apt.py -i image.dd -o out E01 ALL    # macOS artefact extraction (handles APFS natively)
```
On a Mac examination box, attach the image read-only with `hdiutil attach -nomount -readonly`
and `mount_apfs -o rdonly`.

## Snapshots
- `tmutil listlocalsnapshots /` (live) or tool listings show local Time Machine snapshots
  (`com.apple.TimeMachine.<date>.local`) and OS update snapshots. Each is a point-in-time view:
  mount and diff like VSS (`mount_apfs -s <snapshot> / /mnt/snap`).
- Snapshots disappear after about 24 hours or under space pressure; collect early.

## Timestamps
APFS stores nanosecond-resolution create, modify, change, access and **date added**
(`date_added` in the inode extended fields; drives the Finder "Date Added" column and shows when
a file arrived in a folder).

## Gotchas
- Never boot or mount read-write: macOS will update the volume and snapshots.
- Clones (`cp -c`) share blocks; hashing still works, but carving finds duplicates.

## Self-check
You know which volume you examined (System vs Data), whether it was encrypted and how it was
unlocked, and which snapshots existed.
