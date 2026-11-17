---
id: computing-software.systems-network-administration.duplicati.duplicati-disaster-recovery-tools
name: duplicati-disaster-recovery-tools
category: computing-software
field: systems-network-administration
product: duplicati
tags: [disaster-recovery, recovery-tool, list-broken-files, purge-broken-files, encrypted-volumes, corrupt-backup-restore]
level: advanced
status: draft
description: "Restore as much as possible from a damaged Duplicati backup, first by purging broken files, then with the Recovery Tool download, index and restore steps."
sources: ["https://docs.duplicati.com/using-tools/disaster-recovery", "https://docs.duplicati.com/technical-details/understanding-restore/disaster-recovery"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Disaster recovery for a damaged Duplicati backup

Two kinds of disaster: loss of the source files or whole system, and missing or corrupted backup files. Duplicati is strict when backing up but robust when restoring, even from partially bad data, and the restore algorithm is simple enough that a Python recovery script and a C# Recovery Tool exist for when the normal client cannot run or the backup is badly damaged.

Prerequisites: protocol, location and credentials of the remote store; the passphrase; a computer with room for the restored files; the command line tools that ship with Duplicati; and, for the Recovery Tool, temporary local space for all the backup files.

Option 1, purge: if you still have the machine with a valid local database, run `list-broken-files` against the backup URL with `--dbpath` and `--passphrase` (add `--full-result`). It reports remote files whose size or hash does not match, and which files in which versions they affect. Purge the broken files to make the backup consistent again.

Option 2, the Recovery Tool, which performs the normal restore steps manually:
1. `download` fetches all remote files, decrypts them and stores them locally. This is required because the tool must read every file's contents.
2. An index is built that records what information lives in which downloaded file.
3. `restore <localfolder> [version]` recreates files from the blocks in the dblock files, optionally with `--targetpath` (otherwise files return to their original locations) and filters.
Optional commands list files in the downloaded set and recompress or re-upload files. A normal restore uses the dindex files to learn how to assemble blocks inside dblock files in order, then moves recreated files to the restore location.
