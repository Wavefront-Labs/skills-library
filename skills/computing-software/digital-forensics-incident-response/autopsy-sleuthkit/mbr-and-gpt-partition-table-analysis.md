---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.mbr-and-gpt-partition-table-analysis
name: mbr-and-gpt-partition-table-analysis
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [gpt-analysis, partition-analysis, mmls, disk-imaging, dfir]
level: practitioner
status: draft
description: "Analyse MBR and GPT partition tables: protective MBR, GPT header and backup, partition type GUIDs, gaps and hidden areas, and detecting deleted or altered partitions."
sources: ["https://uefi.org/specifications", "https://www.sleuthkit.org/sleuthkit/man/mmls.html", "https://en.wikipedia.org/wiki/GUID_Partition_Table"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MBR and GPT partition table analysis

**Goal:** account for every sector of the disk: which partitions exist, what type they are, and
whether anything sits in gaps, deleted partitions or beyond the declared end.

## MBR
- Sector 0: boot code (446 bytes), four 16-byte partition entries (status, type, LBA start, size), signature `55AA`.
- Extended partitions chain via EBRs. Types: 0x07 NTFS/exFAT, 0x0B/0x0C FAT32, 0x83 Linux, 0x8E LVM, 0xEE GPT protective.
- Boot code is a malware target (bootkits): hash and compare sector 0 boot code against known Windows MBR code.

## GPT (UEFI spec)
- LBA 0 protective MBR (type 0xEE); LBA 1 GPT header (`EFI PART` signature, disk GUID, CRC32s,
  first/last usable LBA, partition entry array location); entries at LBA 2-33 (128 x 128 bytes).
- **Backup header** at the last LBA, backup array just before it. Differences between primary and backup = tampering or corruption.
- Entry: type GUID, unique GUID, start/end LBA, attributes, UTF-16 name.
  Common type GUIDs: `C12A7328-F81F-11D2-BA4B-00A0C93EC93B` EFI System; `E3C9E316-0B5C-4DB8-817D-F92DF00215AE` Microsoft Reserved;
  `EBD0A0A2-B9E5-4433-87C0-68B6B72699C7` Basic data; `DE94BBA4-06D1-4D40-A16A-BFD50179D6AC` Windows Recovery;
  `0FC63DAF-8483-4772-8E79-3D69D8477DE4` Linux filesystem; `7C3457EF-0000-11AA-AA11-00306543ECAC` APFS.

## Tools
```bash
mmls image.dd                   # shows partitions and unallocated gaps (sizes in sectors)
gdisk -l image.dd               # verifies primary vs backup GPT, CRCs
sfdisk -d image.dd
testdisk image.dd               # finds deleted/lost partitions by scanning for boot sectors
```
`mmls` "Unallocated" ranges: examine them (`blkls`/`dd` + strings/carving).

## Red flags
- Gaps larger than alignment (more than 1 MiB) between partitions or after the last partition.
- Partition entries zeroed in primary but present in backup GPT (deleted partition).
- HPA/DCO: disk reports fewer sectors than physical (`hdparm -N`, `hdparm --dco-identify`).

## Verify
Every sector range is accounted for: partitions, alignment gaps, and examined unallocated areas.
