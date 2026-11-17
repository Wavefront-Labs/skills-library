---
id: computing-software.collaboration-platform-administration.nextcloud.client-resync-after-restore
name: client-resync-after-restore
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [data-fingerprint, files-scan, restore, sync-clients, occ]
level: advanced
status: draft
description: "After restoring an outdated Nextcloud backup, run maintenance:data-fingerprint so clients can return newer files, and files:scan when the database is newer than data."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/maintenance/restore.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: stop sync clients from overwriting good data with an old restore, and recover what they hold.

Default behaviour: the server is the authoritative source. When server and client differ, clients fetch from the server. If the restored backup is older than the client state, clients may be more current than the server.

Fix: run the fingerprint command after the restore.

```
sudo -E -u www-data php occ maintenance:data-fingerprint
```

It changes the synchronisation algorithm to recover as much data as possible:
- files missing on the server are recovered from the clients
- where content differs, users are asked which version to keep

The docs also name a rarer case where the database is newer than the data directory. The fingerprint helps there too: the server restores data from clients and preserves the shares. Until then the files would be visible but not accessible.

When files exist on disk but the database does not know them, run a scan to update the database:

```
sudo -E -u www-data php occ files:scan --all
```

(`--all` scans every user; scan a single user by passing their id instead.)

Order of operations: restore folders, restore database, run the fingerprint command, then scan if needed, and only then bring users back online.

Check: a client that held a newer file than the backup prompts the user or uploads it, instead of deleting it.
