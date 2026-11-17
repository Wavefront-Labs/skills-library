---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.fat-and-exfat-forensics
name: fat-and-exfat-forensics
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [fat-forensics, exfat-forensics, fat32, exfat, usb-media, deleted-file-recovery, sleuthkit, dfir]
level: practitioner
status: draft
description: "Examine FAT12/16/32 and exFAT volumes from USB sticks and SD cards: structures, timestamp quirks, deleted entry recovery and TSK commands."
sources: ["https://www.sleuthkit.org/sleuthkit/docs.php", "https://learn.microsoft.com/en-us/windows/win32/fileio/exfat-specification", "https://www.amazon.com/System-Forensic-Analysis-Brian-Carrier/dp/0321268172"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FAT and exFAT forensics

**Goal:** analyse removable media (USB sticks, SD cards, cameras, older drives) correctly,
because FAT-family timestamps and deletion behaviour differ from NTFS.

## Structures
- **FAT12/16/32:** boot sector, FAT tables (cluster chains, usually 2 copies), root directory,
  data area. Directory entries are 32 bytes; long file names (LFN) are stored in extra entries
  preceding the 8.3 entry.
- **exFAT:** boot region, FAT (often unused for contiguous files: `NoFatChain` flag), allocation
  bitmap, up-case table, directory entry sets (File `0x85`, Stream Extension `0xC0`, File Name
  `0xC1`).

## Timestamps
| | Created | Modified | Accessed | Zone |
|---|---|---|---|---|
| FAT | 10 ms resolution | **2-second** resolution | date only | local time, no zone |
| exFAT | 10 ms | 10 ms | 2 s | local time + UTC offset field (if set by the OS) |
FAT times are local time of the writing machine: record the suspect host's time zone before
converting. Modified times survive copying (a copied file keeps the source mtime, gets a new
created time), which can make created later than modified: normal copy behaviour.

## Deletion
- FAT: first byte of the 8.3 name set to `0xE5`, cluster chain zeroed in the FAT, data stays.
  Recovery works well for contiguous files (start cluster + size in the entry); fragmented
  files lose their chain.
- exFAT: the `InUse` bit of each entry type is cleared (`0x85 -> 0x05`), bitmap freed; start
  cluster, length and `NoFatChain` survive, so contiguous files recover cleanly.

## Commands
```bash
fsstat image.dd                      # FS type, cluster size, FAT location, volume label/serial
fls -r -p image.dd                   # deleted entries marked with '*'
istat image.dd <inode> ; icat -r image.dd <inode> > recovered.bin   # -r attempts deleted recovery
tsk_recover -e image.dd outdir/      # export all, including unallocated files
```
The volume serial number (from `fsstat`) ties a USB stick to Windows artefacts
(`EMDMgmt`, LNK `VolumeSerialNumber`, jump lists).

## Gotchas
- Cameras and phones write FAT with their own clock and zone; check device settings.
- Quick format rewrites the FAT and root directory but not data: carve the data area.
- Some tools reset the 2-second rounding; always compare raw entry values.

## Self-check
You converted timestamps with the right zone, linked the volume serial to host artefacts, and
validated recovered files by header and size.
