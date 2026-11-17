---
id: computing-software.collaboration-platform-administration.zulip.zulip-restore-backup
name: zulip-restore-backup
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [restore-backup, keep-settings, backup-restore, external-host]
level: practitioner
status: docs-checked
description: "Restore a Zulip backup with restore-backup on a matching OS and PostgreSQL version, handle hostname changes with EXTERNAL_HOST, keep-settings flags and inspect version files."
sources: ["https://zulip.readthedocs.io/en/latest/production/export-and-import.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Restoring a Zulip backup

1. Install the same base OS the backup came from; upgrade the OS only after restoring.
2. Install a new Zulip server following the install guide (the backup instructions say "through Step 3", while the install guide says to stop after Step 2 when importing a server backup), using `--postgresql-version` to match the backup's PostgreSQL. Upgrade PostgreSQL after restoring if you want a newer one.
3. As root, import:

```
~zulip/deployments/current/scripts/setup/restore-backup /path/to/backup
```

Afterwards the server should be fully operational.

Restoring under a different hostname, common when testing, needs `EXTERNAL_HOST` updated in `/etc/zulip/settings.py` and a restart once the restore completes. Until then Zulip believes the old hostname and returns HTTP 400 for the new one.

Restoring onto a differently configured host, such as a different `REMOTE_POSTGRES_HOST`: edit `/etc/zulip/settings.py` for the new host first, then run `restore-backup --keep-settings /path/to/backup`. Add `--keep-zulipconf` to preserve the local `/etc/zulip/zulip.conf` too.

To see what versions a backup used, read `postgres-version`, `os-version` and `zulip-version` inside it without extracting everything:

```
tar -Oaxf /path/to/archive/zulip-backup-rest.tar.gz zulip-backup/zulip-version
```

The Zulip version must match, so check this file before provisioning the new server.

## Checked

Confirmed against the Backups section of the export-and-import page and the install guide: restore steps, the EXTERNAL_HOST and HTTP 400 note, --keep-settings and --keep-zulipconf, and the version files inside the tarball. Reworded the install step to reflect the conflict between the two pages about Step 3.

Method: docs-checked 2026-11-09 against docs/production/export-and-import.md and docs/production/install.md in the zulip/zulip repository (main), the sources of the cited pages.
