---
id: computing-software.systems-network-administration.backup-and-recovery.lto-generations-and-barcode-labels
name: lto-generations-and-barcode-labels
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [lto-generations, barcode-labels, lto, tape, tape-compatibility, media-id]
level: practitioner
status: docs-checked
description: "Plan LTO media by generation: read/write compatibility between drives and cartridges, LTO-10 limits, and barcode label practice for tape libraries."
sources:
  - https://www.lto.org/lto-generation-compatibility/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LTO generations and barcode labels

**Goal:** buy the right tapes for your drives, keep old tapes readable, and label them so the library and software agree.

## Compatibility rules (LTO Program)
- LTO drive generations 1-7 read tapes from two generations prior and write tapes from the prior generation.
- LTO-8 drives read and write LTO-7 and LTO-8 media, including LTO-7 Type M.
- LTO-9 drives read and write LTO-8 and LTO-9 media only.
- LTO-10 drives read and write LTO-10 media only (30 TB and 40 TB LTO-10 media are interchangeable).
- Check the LTO Program compatibility page before buying; do not assume a newer drive reads old tapes.
Consequence: keep at least one older drive (or migrate data) for tapes still under retention when you upgrade.

LTFS (Linear Tape File System) is an open standard, so LTFS-formatted tapes can be read by drives from any LTO vendor.

## Capacity, speed and initialisation
Native capacity, native speed and any first-load calibration or initialisation time differ per generation and drive vendor. Take them from the drive vendor's specification for the exact drive, not from a generic table; plan on native, not compressed, capacity.

## Barcode labels
- Use the label format your library and backup software document (volume serial plus media-type suffix is the usual shape); set barcode reporting consistently in the library.
- Cleaning cartridges carry their own label prefix; check your library's documentation.
- Buy pre-printed vendor labels; home-printed labels can fail to scan.
- Reserve prefixes per pool or site (for example one letter for onsite, another for vault) to aid handling.

## Gotchas
- Mixed generations in one partition: software may load a tape into a drive that cannot write it; restrict by media type.

## Verify
Library inventory shows every barcode with the expected media type, and the backup software volume list matches.

## Checked
2026-10-28. Confirmed against the LTO Program Generation Compatibility page (generation 1-7 rule, LTO-8 including Type M, LTO-9, LTO-10 media, LTFS). Removed: the capacity and speed table, media ID codes, example barcodes, LTO-9 calibration time, and the IBM label source (page returned no content); the lto.org technology page redirects to the compatibility page.
Method: documentation only; no commands were run.
