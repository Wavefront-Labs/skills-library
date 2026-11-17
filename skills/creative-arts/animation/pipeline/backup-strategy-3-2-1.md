---
id: creative-arts.animation.pipeline.backup-strategy-3-2-1
name: backup-strategy-3-2-1
category: creative-arts
field: animation
product: pipeline
tags: [backup-strategy, 3-2-1, backup, disaster-recovery, restore-testing, immutable-backup, snapshots]
level: practitioner
status: draft
description: "Design backups for a production: the 3-2-1 rule and its variants, what to back up, snapshots versus backups, offsite and immutable copies, restore tests."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Backup strategy (3-2-1)

The **3-2-1 rule** (popularised by photographer Peter Krogh) says: keep **3 copies** of your data, on **2 different media**, with **1 copy offsite**. A common extension adds immutability and verification (often written 3-2-1-1-0): one copy offline or immutable, and zero errors on restore tests.

## What to back up
- **Source and project data**: scenes, rigs, textures, scripts, tracker database and config, editorial projects and audio sessions.
- **Deliverables and masters** (`archival-master-formats.md`).
- **Infrastructure**: asset database, production tracker, license server configs, pipeline code (in git).
- Do not back up **regenerable data** (render caches, temp files) unless regeneration is costly.

## Copies and media
- Primary storage counts as copy 1. A second system (a NAS, another site) and a different technology (tape, cold object storage) gives the second media type.
- Offsite can be cloud object storage, a second studio, or tapes stored elsewhere (`lto-ltfs-archiving.md`).
- **Snapshots are not backups**: a snapshot on the same storage system disappears with it. Use them for quick rollback only.

## Protect against ransomware and mistakes
- Keep at least one copy **offline or immutable** (object lock, WORM, tape in a vault, or an air-gapped drive).
- Use separate credentials for the backup system from the artists' accounts.
- Use versioned backups so a corrupted file does not overwrite the last good copy.

## Process
1. Set a **schedule** by data value: active work daily or continuous, archives after delivery.
2. **Verify** with checksums (`checksum-fixity.md`).
3. **Test restores** regularly (for example monthly), restoring a real project to a clean location and opening it.
4. Document the **restore procedure** and who does it, with target times (recovery time and recovery point objectives).
5. Monitor jobs and alert on failures.

## Verify
- [ ] Three copies on two media types with one offsite.
- [ ] One copy is offline or immutable.
- [ ] Last restore test date and result recorded.
