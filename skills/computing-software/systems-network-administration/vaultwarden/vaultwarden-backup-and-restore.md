---
id: computing-software.systems-network-administration.vaultwarden.vaultwarden-backup-and-restore
name: vaultwarden-backup-and-restore
category: computing-software
field: systems-network-administration
product: vaultwarden
tags: [vaultwarden, backup, sqlite, restore, db-sqlite3, rsa-key, attachments, vaultwarden-backup]
level: practitioner
status: docs-checked
description: "Back up a Vaultwarden data directory safely: which files matter, the SQLite online backup, VACUUM INTO and built-in backup command, and restore pitfalls with WAL files."
sources: ["https://github.com/dani-garcia/vaultwarden/wiki/Backing-up-your-vault"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vaultwarden backup and restore

What to back up from the data directory:

- `db.sqlite3`: required; nearly all state (entries, users, orgs, devices).
- `attachments/`: required; attachment files live outside the database.
- `sends/`: optional; only if existing Sends must survive a restore.
- `config.json`: recommended; admin-page settings, may hold plaintext secrets (admin token, SMTP credentials), so encrypt it.
- `rsa_key*`: recommended; signs login tokens. Losing it logs everyone out and voids pending invitations. `rsa_key.pem` is sensitive; encrypt it.
- `icon_cache/`: optional; saves re-downloading icons.

Do not copy a live SQLite file naively. Use the Online Backup API:

```
sqlite3 data/db.sqlite3 ".backup '/path/to/backups/db-$(date '+%Y%m%d-%H%M').sqlite3'"
sqlite3 data/db.sqlite3 "VACUUM INTO '/path/to/backups/db-$(date '+%Y%m%d-%H%M').sqlite3'"
docker exec -it vaultwarden /vaultwarden backup     # built in since 1.32.1
```

`VACUUM INTO` also compacts but is slower. The Docker images ship neither `sqlite3` nor `cron`, so use the built-in command or schedule on the host. Back up at least daily, keep one copy off the machine (rclone, restic, rustic), encrypt backups, and do not rely on filesystem or VM snapshots alone.

Restore: stop Vaultwarden and delete any existing `db.sqlite3-wal` first; a stale WAL can corrupt the restored database. If you copied `db.sqlite3` directly, restore it with its matching `-wal` file. Test restores periodically. For MySQL/MariaDB or PostgreSQL, dump the database separately; the data directory still needs backing up.

## Checked

2026-11-03. Confirmed against the Vaultwarden wiki (https://github.com/dani-garcia/vaultwarden/wiki) by reading: Backing-up-your-vault (file list, .backup, VACUUM INTO, built-in backup since 1.32.1, WAL restore note, snapshots).
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
