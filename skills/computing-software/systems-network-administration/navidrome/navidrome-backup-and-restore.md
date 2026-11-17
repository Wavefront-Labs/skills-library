---
id: computing-software.systems-network-administration.navidrome.navidrome-backup-and-restore
name: navidrome-backup-and-restore
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, backup, restore, sqlite, cron, backup-prune, database, bkp]
level: practitioner
status: docs-checked
description: "Back up and restore the Navidrome database: Backup.Path, Schedule and Count, manual create and prune, restore with the server stopped, and what backups do not contain."
sources: ["https://www.navidrome.org/docs/usage/admin/backup/", "https://www.navidrome.org/docs/usage/admin/cli/backup/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome backup and restore

Scope: backups cover only the database (users, play counts, playlists, ratings). They do not include the music or the config file, so keep those separately.

Configure scheduled backups (since 0.54):

```toml
[Backup]
Path = "/path/to/backup/folder"
Count = 7
Schedule = "0 0 * * *"
```
or `ND_BACKUP_PATH`, `ND_BACKUP_SCHEDULE`, `ND_BACKUP_COUNT`. Set `Backup.Path = ""` to disable. In Docker add a volume such as `./backup:/backup` and point `ND_BACKUP_PATH` at `/backup`. Files are named like `navidrome_backup_2026.04.01_04.00.00.db`.

CLI (alias `bkp`):
- `navidrome backup create [-d <folder>]`: backup now; does not prune. The next scheduled run prunes down to `Backup.Count`.
- `navidrome backup prune [-d <folder>] [-k <count>] [-f]`: keeps the newest `count` files matching the backup name pattern and ignores other files. `-k 0` deletes all after typing `YES` unless `--force`.
- `navidrome backup restore --backup-file <file> [-f]`: replaces the whole database. A bare file name or relative path is looked up in `Backup.Path`; absolute paths work anywhere. It asks for `YES` unless `--force`.

Restore only while Navidrome is stopped, and expect to lose everything after the backup (new users, play counts, playlists):

```bash
docker compose stop navidrome
docker compose run --rm navidrome backup restore --backup-file navidrome_backup_2026.04.01_04.00.00.db
docker compose start navidrome
```
Always take a `backup create` before risky operations such as changing PID settings or `missing fix`.

Verify: the backup file exists after `create`, and `navidrome user list` after a restore shows the expected users.

## Checked

2026-11-04. Confirmed against the Navidrome Automated Backup page and the `navidrome backup` CLI page: scope, 0.54 introduction, config keys and env vars, alias, create, prune and restore flags, YES prompt, restore path lookup, stop-before-restore. The PID-settings backup advice is on the Persistent IDs page. `Backup.Path = ""` disables backups per the Configuration Options page. Nothing removed.

Method: documentation only; no commands were run.
