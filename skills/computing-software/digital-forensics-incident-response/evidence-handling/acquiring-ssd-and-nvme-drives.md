---
id: computing-software.digital-forensics-incident-response.evidence-handling.acquiring-ssd-and-nvme-drives
name: acquiring-ssd-and-nvme-drives
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [ssd-forensics, hpa-dco, nvme, trim, garbage-collection, forensic-acquisition, dfir]
level: advanced
status: draft
description: "Acquire SSD and NVMe drives forensically: TRIM and garbage collection effects, NVMe write blocking, HPA/DCO and namespaces, self-encrypting drives and repeatability."
sources: ["https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt", "https://nvmexpress.org/specifications/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Acquiring SSD and NVMe drives

**Goal:** a sound image of solid-state storage while understanding why it behaves unlike a
hard disk.

## Behaviour that matters
- **TRIM / UNMAP**: the OS tells the SSD which blocks are deleted; the controller may erase
  them. Deleted-file recovery and carving of unallocated space often yield zeros.
- **Garbage collection** runs autonomously when powered, even behind a write blocker, so
  the drive content can change between reads; two acquisitions may hash differently.
- **Wear levelling / over-provisioning**: physical NAND contains data not addressable via
  LBA; only chip-off or vendor tools reach it.
- **Self-encrypting drives (OPAL, eDrive/BitLocker hardware encryption)**: data is ciphertext
  unless unlocked; once removed and powered off it locks.

## Procedure
1. Prefer imaging quickly after seizure, minimising powered time.
2. NVMe: use a blocker that supports NVMe (Tableau TX1/T7u with NVMe adapter) or an
   NVMe-capable forensic imager.
3. Check for HPA/DCO on SATA SSDs (`hdparm -N`, `hdparm --dco-identify`) and for multiple
   **NVMe namespaces** (`nvme list`, `nvme list-ns /dev/nvme0`); image each namespace.
4. If encrypted and the system is running: do a live logical/physical acquisition of the
   unlocked volume instead of removing the drive.
5. Hash during acquisition; record that re-hashing the source may legitimately differ.

## Gotchas
- Soldered NVMe in modern laptops: no blocker possible; live acquisition or boot a forensic
  OS with software write blocking.
- Apple T2/M-series: storage is hardware-encrypted bound to the SoC; only logical
  acquisition from an unlocked running system or target/share-disk mode with credentials.

## Verify
Notes explain any source hash change by SSD behaviour, and the image's verification hash
matches the acquisition hash.
