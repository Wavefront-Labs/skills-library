---
id: creative-arts.animation.encode-delivery.lto-ltfs-archiving
name: lto-ltfs-archiving
category: creative-arts
field: animation
product: encode-delivery
tags: [lto, archive, archiving, ltfs, tape, lto-9, cold-storage, mkltfs, offsite, restore-test]
level: advanced
status: draft
description: "Archive a finished production to LTO tape with LTFS: generations and capacities, formatting, writing with verification, labelling, dual copies and restore tests."
sources:
  - https://www.lto.org/technology/
  - https://www.snia.org/tech_activities/standards/curr_standards/ltfs
  - https://github.com/LinearTapeFileSystem/ltfs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LTO and LTFS archiving

**Goal:** a cheap, durable, offline copy of the production that survives ransomware, storage
failures and decades on a shelf. LTO tape with LTFS (Linear Tape File System) makes the tape
mount like a drive with a file index, readable by any LTFS implementation.

## Capacities (native, uncompressed)

LTO-7 6 TB, LTO-8 12 TB, LTO-9 18 TB. LTO-9 drives read and write LTO-8 media, but LTO-10 (2025, 30 TB native on standard cartridges, 400 MB/s) has no backward read or write compatibility with LTO-9 or earlier, so keep an LTO-9 drive to restore existing tapes (generation facts as of October 2026; confirm at lto.org/lto-10).
Media is lossless-compressed by the drive, but EXR/ProRes/FFV1 barely compress: plan on native.
A drive generation's readability window is the main longevity risk; migrate every two
generations.

## Workflow

1. Prepare the archive set (`creative-arts.animation.encode-delivery.archival-master-formats`)
   and its checksum manifest on fast disk. Tape writes need a sustained 300-400 MB/s feed;
   slow sources cause shoe-shining (stop/start wear).
2. Format: 
```bash
mkltfs -d /dev/sg1 -s SHOW01 -n "SHOW_S01_ARCHIVE_A"     # tape serial and volume name
ltfs -o devname=/dev/sg1 /mnt/ltfs
```
3. Copy large files sequentially (rsync or a tool like YoYotta, Hedge Canister, BRU, Archiware P5):
```bash
rsync -a --progress SHOW_S01/ /mnt/ltfs/SHOW_S01/
```
Many small files (scene/asset folders) are slow on tape: tar them first per asset or per shot.
4. Verify by reading back and checking the manifest from the tape, not from the source.
5. Unmount cleanly (`umount /mnt/ltfs`) so the index is written; an unclean eject loses the index.
6. Make the second copy on a separate tape set; store one off-site.

## Labelling and catalogue

Barcode labels (volume serial) on every cartridge; a catalogue (spreadsheet or the archive
tool's database) listing tape, contents, manifest, date, LTFS version, drive generation.
Keep the catalogue in at least two places; a tape you cannot find is not archived.

## Gotchas

- LTFS is append-only per tape in practice: deleting files does not free space.
- Cartridges need storage at stable temperature and humidity, upright, away from magnets.
- Windows uses vendor LTFS drivers (IBM, HPE); test cross-platform reads if a client will restore.

## Verify

Annual restore test from each tape set: mount, restore a random episode, verify checksums.
