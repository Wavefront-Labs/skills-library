---
id: computing-software.systems-network-administration.backup-and-recovery.pbs-tape-backup
name: pbs-tape-backup
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [pbs-tape, proxmox-backup-server, proxmox-tape, lto, tape-backup, media-pools]
level: advanced
status: docs-checked
description: "Back up Proxmox Backup Server datastores to LTO tape: changers and drives, media pools with allocation and retention, tape backup jobs, encryption keys, inventory and restore."
sources:
  - https://pbs.proxmox.com/docs/tape-backup.html
  - https://pbs.proxmox.com/docs/command-syntax.html#proxmox-tape
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PBS tape backup

**Goal:** offline, air-gapped copies of PBS datastores on LTO tape with a working restore path.

## Hardware setup
```sh
proxmox-tape changer scan                     # list changers
proxmox-tape drive scan                       # list drives
proxmox-tape changer create sl3 --path /dev/tape/by-id/scsi-XXXX
proxmox-tape drive create drive0 --path /dev/tape/by-id/scsi-YYYY-sg --changer sl3 --changer-drivenum 0
proxmox-tape status --drive drive0
```
Standalone drives work too (manual loading, `proxmox-tape load-media`).

## Media pools
```sh
proxmox-tape pool create weekly --allocation sat --retention 4weeks --encrypt <key-fingerprint>
```
- **Allocation**: `continue` (append to the current media set forever), `always` (new set each job), or a calendar event (`sat` starts a new set each Saturday).
- **Retention**: `keep` (never overwrite), `overwrite`, or a time span after which media are reusable.
- A **media set** is the group of tapes written together; restores need the whole set.

## Label and back up
```sh
proxmox-tape barcode-label --pool weekly --drive drive0     # label all new barcoded tapes
proxmox-tape backup store1 weekly --drive drive0 --eject-media
```
Schedule with tape backup jobs (GUI Tape Backup -> Backup Jobs) including `--latest-only` to write only the newest snapshot per group, and namespace selection.

## Encryption
`proxmox-tape key create --hint "2026 tape key"` ; store the exported paperkey offline. Lost key = unreadable tapes.

## Restore
```sh
proxmox-tape inventory --drive drive0                 # what is in the library
proxmox-tape media list
proxmox-tape restore <media-set-uuid> store-restore --drive drive0
```
Without the PBS catalogue (new server), `proxmox-tape catalog` rebuilds it from the inserted tape.

## Gotchas
- LTO drives need a fast feed; datastores on slow HDD may cause shoe-shining. Verify drive throughput.

## Verify
Restore one VM snapshot from tape into a scratch datastore quarterly and boot it.

## Checked

2026-10-28

Confirmed: PBS tape backup chapter and command syntax: changer scan, drive scan, changer-drivenum, load-media, pool allocation (continue, always, calendar event) and retention (keep, overwrite, time span), barcode-label, backup --eject-media, latest-only, inventory, media list, catalog.

Removed or corrected: the catalog --scan flag, the cleaning-slot gotcha.

Method: documentation only; no commands were run.
