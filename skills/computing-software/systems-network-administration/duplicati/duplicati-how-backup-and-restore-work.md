---
id: computing-software.systems-network-administration.duplicati.duplicati-how-backup-and-restore-work
name: duplicati-how-backup-and-restore-work
category: computing-software
field: systems-network-administration
product: duplicati
tags: [backup-process, deduplication-blocks, dblock-dindex, block-size, remote-volume-size, restore-process, file-list]
level: advanced
status: docs-checked
description: "Understand Duplicati's block-based backup and restore algorithm and how block size and remote volume size affect speed, deduplication and restore cost."
sources: ["https://docs.duplicati.com/technical-details/understanding-backup/how-backup-works", "https://docs.duplicati.com/technical-details/understanding-backup/backup-size-parameters", "https://docs.duplicati.com/technical-details/understanding-restore/how-restore-works"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# How Duplicati backup and restore work

Backup: activate an operating system snapshot if possible, scan the source recursively, and for each file read a block at a time; skip a block that already exists, otherwise add it to a volume. When a volume reaches the maximum size a new one starts and the previous one is processed: compressed (if not done while adding), encrypted and uploaded. At the end a file list that explains how to recreate every file is uploaded. Duplicati then checks that the remote storage looks as expected and downloads a few random volumes to verify the data. Retention rules then remove old lists and may consolidate remote volumes to reclaim space.

Block size: files are split into fixed-size blocks. Smaller blocks deduplicate more and upload less after a small change (a change smaller than a block still rewrites a whole block), but increase the number of blocks to track and may slow things. Typical values run from 100 KiB for backups under 3 GiB up to 1 MiB. Because comparison needs equal sizes, the block size cannot be changed after the first backup; changing it would amount to a new backup.

Remote volume size: the size of files stored at the destination; the count is roughly the data size divided by it. Larger volumes cut per-file overhead (headers, handshakes, smaller lists), but a restore must download a whole remote volume to extract any block. For cloud providers limited by your connection, about 50 to 500 MiB is reasonable; on a local network 500 to 2000 MiB can be acceptable.

Restore: work out the files (take the file list of the version, apply filters, skip files that exist with correct content), then for each block locate its volume, download it, decrypt and decompress it, append the block to the file and finally verify the file against the original content. With a local database most of this is database queries; without one, Duplicati builds a temporary database during the restore.

## Checked

2026-11-04. Confirmed against the How backup works, Backup size parameters and How restore works pages. Nothing removed.

Method: documentation only; no commands were run.
