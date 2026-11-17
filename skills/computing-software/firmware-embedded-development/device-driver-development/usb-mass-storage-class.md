---
id: computing-software.firmware-embedded-development.device-driver-development.usb-mass-storage-class
name: usb-mass-storage-class
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [usb-device, usb-msc, bulk-only-transport, scsi-commands, block-device, fat-filesystem, uf2-bootloader, concurrent-access, firmware-embedded-development]
level: advanced
status: draft
description: "Expose flash or an SD card as a USB mass-storage drive: BOT/SCSI basics, the shared-filesystem corruption trap, and the 'fake FAT' drag-and-drop update trick."
sources:
  - https://www.usb.org/document-library/mass-storage-bulk-only-10
  - https://github.com/microsoft/uf2
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USB mass storage class (MSC)

**Goal:** the device appears as a USB drive (for logs, configuration files or drag-and-drop
firmware updates) without corrupting data.

## Protocol in brief
Bulk-Only Transport: host sends a 31-byte **CBW** (command block wrapper) on bulk OUT carrying
a SCSI command, data moves on bulk IN/OUT, device answers with a 13-byte **CSW** status.
Commands you must implement: `INQUIRY`, `TEST UNIT READY`, `READ CAPACITY(10)`, `READ(10)`,
`WRITE(10)`, `REQUEST SENSE`, `MODE SENSE(6)`, `PREVENT ALLOW MEDIUM REMOVAL`,
`START STOP UNIT`. Stacks like TinyUSB give you callbacks (`tud_msc_read10_cb`,
`tud_msc_write10_cb`, `tud_msc_capacity_cb`): you implement block read/write.

## The big trap: two masters on one filesystem
When the host mounts the drive it caches the FAT and directory. If firmware also writes files
(FatFs) to the same volume, the two views diverge and the filesystem corrupts. Rules:
- Firmware **unmounts / stops writing** while the host has the medium (between
  `START STOP UNIT` load and eject, or while USB is configured), or
- Expose the medium **read-only** to the host (`tud_msc_is_writable_cb` returns false), or
- Signal media change (sense key UNIT ATTENTION, ASC 0x28) after firmware modifies data so the
  host re-reads. Works on Linux/Windows but caching is still racy: prefer exclusivity.

## Flash backing
- Block size 512 bytes; NOR flash erase sectors are 4 KB+: buffer and read-modify-write, or
  use a flash translation layer with wear levelling. Writes from the host are tiny and random
  (FAT updates), so raw sector-erase per 512-byte write wears flash fast.
- SD cards: pass through blocks directly; mind SPI-mode speed (1-2 MB/s typical).

## "Fake FAT" drag-and-drop updates (UF2 style)
Bootloaders like UF2 synthesise a FAT12 volume on the fly (no real storage): reads return
generated boot sector/FAT/directory; writes are inspected for UF2 blocks (512 bytes with magic
numbers and a target address) and programmed directly to flash. Works on every OS without
tools, and avoids the shared-filesystem problem because nothing is stored.

## Verify
- [ ] Copy a large file, eject, re-plug: file intact (`md5sum`/`certutil -hashfile`).
- [ ] Firmware logging while host mounted: either blocked, or read-only to host with no
      corruption over a long soak.
- [ ] `fsck`/`chkdsk` clean after repeated plug/unplug without eject.
