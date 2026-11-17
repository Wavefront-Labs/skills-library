---
id: computing-software.systems-network-administration.backup-and-recovery.worm-tape-media
name: worm-tape-media
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [worm-tape-media, tape, worm, immutability, compliance-retention, veeam-tape]
level: practitioner
status: draft
description: "Use LTO WORM tape for immutable retention: how WORM cartridges are enforced, backup software pool settings, append behaviour, retention planning, and disposal."
sources:
  - https://www.lto.org/technology/
  - https://helpcenter.veeam.com/docs/backup/vsphere/worm_tapes.html
  - https://www.ibm.com/docs/en/ts4500-tape-library?topic=cartridges-write-once-read-many-worm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WORM tape media

**Goal:** tape copies that cannot be overwritten or erased, for compliance retention or ransomware resistance.

## How WORM works
- WORM cartridges (media IDs LV/LW/LX/LY/LZ) carry a flag in cartridge memory and a factory-written servo/ID; the drive firmware refuses to overwrite data already written.
- You can **append** until the tape is full; you cannot erase, relabel or reuse it.
- Requires a WORM-capable drive (all LTO-3+ drives).

## Backup software
- **Veeam**: create a *WORM media pool* (or WORM GFS pool); retention is effectively permanent; only WORM cartridges can join; tapes cannot be erased from the console.
- **Bacula/Bareos**: label WORM volumes into a pool with `Recycle = no`; Bacula detects WORM media and will not recycle it.
- **NetBackup, Commvault**: WORM tape storage units/policies.
Make sure the software does not try to write a label over a partly used WORM tape; import WORM tapes as new or catalogue them.

## Plan
- WORM costs more per TB and every tape is used once: size budgets by total retained data, not by rotation.
- Use WORM for long-term/compliance copies (e.g. monthly GFS), rewritable media for short rotation.
- Pair with encryption (keys managed separately); WORM stops changes, not reading.

## Gotchas
- Mislabelled or wrong-pool WORM tapes are wasted.
- At end of retention WORM tapes must be physically destroyed (see media sanitisation); budget the destruction.
- Some regulations (SEC 17a-4) need more than WORM media: indexing, duplicate copy, third-party undertaking.

## Verify
Attempt to erase or overwrite a test WORM tape from the software: it is refused; library inventory shows WORM media IDs only in WORM pools.
