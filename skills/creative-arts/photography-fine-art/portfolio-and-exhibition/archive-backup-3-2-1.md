---
id: creative-arts.photography-fine-art.portfolio-and-exhibition.archive-backup-3-2-1
name: archive-backup-3-2-1
category: creative-arts
field: photography-fine-art
product: portfolio-and-exhibition
tags: [portfolio-and-exhibition, archive-backup, image-rights, 3-2-1-backup, checksums, digital-preservation]
level: practitioner
status: draft
description: "Protect a photography archive with 3-2-1 backups: storage layout, local copies, offsite and cloud, verification with checksums, migration and catalog inclusion."
sources: ["https://www.cisa.gov/sites/default/files/publications/data_backup_options.pdf", "https://www.dpconline.org/handbook", "https://dpbestflow.org/ (ASMP dpBestflow)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 3-2-1 archive backup

**3 copies** of every file, on **2 different media/devices**, **1 offsite**. Add: one copy offline or immutable (protects against ransomware), and verification.

## Layout
- **Working copy**: archive drive or NAS holding raws (`YYYY/YYYY-MM-DD_shoot`), master TIFF/PSDs, Lightroom catalog and presets.
- **Local backup**: a second drive or NAS updated nightly (versioned backup: Time Machine, Windows File History, or rsync/robocopy plus snapshots on a NAS).
- **Offsite**: cloud backup (Backblaze B2, AWS S3/Glacier, a backup service) or rotated drives stored elsewhere (swap monthly).

## What to include
- Raw files and masters, Lightroom/Capture One catalogs and their backups, presets and print templates, inventory database, contracts, licences and registration records.
- Previews and caches can be excluded.

## Verification
- Generate checksums (e.g. `md5`/`sha256` manifests, or tools like ChronoSync, FreeFileSync verify, rsync `--checksum`, IntegrityChecker) and compare periodically to detect silent corruption (bit rot).
- Quarterly test restore: pick 10 random files and a catalog from the offsite copy and open them.
- Alert on drive SMART errors; replace drives at about 4-5 years.

## Migration
- Every 5-7 years move to new media; verify checksums after copy.
- Keep raw formats with DNG copies for long-term readability if proprietary raw support is a concern.

## Card handling
- Do not format cards until files exist in two places (import second copy + backup run).

## Verify
- [ ] Three copies exist for the latest shoot (check paths), offsite copy is less than one week old, and the last test restore succeeded.
