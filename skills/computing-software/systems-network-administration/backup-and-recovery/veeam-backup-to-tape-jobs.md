---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-backup-to-tape-jobs
name: veeam-backup-to-tape-jobs
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam-tape, tape-backup, gfs-media-pool, lto, worm-tape, tape-encryption, veeam]
level: advanced
status: draft
description: "Run Veeam backup-to-tape: tape server and library setup, standard and GFS media pools, backup-to-tape and file-to-tape jobs, encryption, WORM media and vaulting."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/tape_device_support.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/backup_to_tape.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Veeam backup to tape

**Goal:** an offline, air-gapped copy of backups on tape with the right retention, managed by Veeam.

## Infrastructure
- **Tape server**: Windows machine attached to the library/drive (SAS or FC). Install the **vendor's** drivers for the drives and changer, not generic Microsoft ones; Veeam needs them to use the hardware correctly.
- Add the tape server; Veeam discovers libraries and drives; run **Inventory** (read labels) or **Catalog** (read contents) for existing tapes. Libraries with barcode readers inventory in seconds.

## Media pools
- **Standard media pool**: tapes for jobs with simple retention (overwrite after N days/weeks).
- **GFS media pool**: weekly/monthly/quarterly/yearly sets with separate retention per level; the job picks full restore points from repositories for each GFS period.
- Free, Unrecognized, Imported and Retired system pools hold tapes not yet assigned.
- Options: append vs new tape per session, multiple drives in parallel, encryption, WORM pools for WORM cartridges.

## Jobs
- **Backup to tape**: copies existing backup files (from jobs or repositories) to tape. Full and incremental, with **virtual synthetic full** built on tape from repository increments when no full exists.
- **File to tape**: arbitrary files/folders (NDMP supported for some NAS).

## Encryption
Hardware encryption on LTO drives managed by Veeam (keys stored in Veeam with password), or Veeam software encryption. Record passwords in the escrow process; a tape without its key is unrecoverable.

## Vaulting
Define **vaults** (off-site locations); media pools can move tapes to a vault after the job and track where each tape is. Use the export slot (I/E station) to eject.

## Gotchas
- Forever-incremental source chains cannot be copied as GFS fulls efficiently; ensure the source produces fulls or rely on virtual synthetic fulls.
- Tape drive speed requires a fast feed (LTO-9 native ~400 MB/s); slow sources cause shoe-shining.

## Verify
Restore a VM directly from a tape set periodically (Veeam can restore from tape to infrastructure), and reconcile the vault list with tapes physically off-site.
