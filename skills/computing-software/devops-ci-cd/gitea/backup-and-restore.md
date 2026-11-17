---
id: computing-software.devops-ci-cd.gitea.backup-and-restore
name: backup-and-restore
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-dump-restore, gitea, gitea-dump, regenerate-hooks, pg-dump, convert-database, backup-consistency]
level: practitioner
status: docs-checked
description: "Back up Gitea with gitea dump (stopped instance), what the zip contains, native DB dumps, manual restore incl. Docker paths, hook regeneration, DB type conversion."
sources: ["https://docs.gitea.com/administration/backup-and-restore/", "https://docs.gitea.com/administration/command-line/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Backup and restore

`gitea dump` writes everything to one ZIP; there is **no restore command**, restore is manual.

## Consistency
Stop Gitea first. The database, files and git repositories change together (a migration holds a DB transaction while the repo is copied), so a live backup can leave a DB that claims a complete repo that is not.

## Dump
As the Gitea user in the install directory: `./gitea dump -c /path/to/app.ini`. Output `gitea-dump-<timestamp>.zip` contains `app.ini` (if outside `custom/`), `custom/`, `data/` (APP_DATA_PATH: attachments, avatars, lfs, indexers, the SQLite file; sessions excluded for file sessions), `repos/`, `gitea-db.sql`, `log/` (not needed for recovery). Temp files go to `--tempdir` or `TMPDIR`.
Useful flags: `--file/-f`, `--tempdir/-t`, `--skip-repository/-R`, `--skip-custom-dir`, `--skip-lfs-data`, `--skip-attachment-data`, `--skip-package-data`, `--skip-log`, `--skip-index`, `--database/-d` (sqlite3, mysql, mssql, postgres), `--type` (zip, tar, tar.gz, tar.xz, tar.zst, ...).

The SQL inside uses XORM and open issues exist around restoring it, so admins may prefer native tools: `mysqldump -u$USER -p$PASS --database $DATABASE > gitea-db.sql` or `pg_dump -U $USER $DATABASE > gitea-db.sql`.

Docker: run it as the `RUN_USER` from `app.ini` and `docker exec -w <tempdir>` so zipping does not hit permission errors: `docker exec -u <user> -it -w <tempdir> <container> bash -c '/usr/local/bin/gitea dump -c </path/to/app.ini>'`.

## Restore (binary layout example)
```sh
unzip gitea-dump-<ts>.zip && cd gitea-dump-<ts>
mv app.ini /etc/gitea/conf/app.ini
mv data/* /var/lib/gitea/data/
mv log/* /var/lib/gitea/log/
mv repos/* /var/lib/gitea/data/gitea-repositories/
chown -R gitea:gitea /etc/gitea/conf/app.ini /var/lib/gitea
mysql --default-character-set=utf8mb4 -u$USER -p$PASS $DATABASE <gitea-db.sql   # or sqlite3 / psql -U $USER -d $DATABASE
service gitea restart
```
Docker (rootful): `mv data/* /data/gitea`, `mv repos/* /data/git/repositories/`, `chown -R git:git /data`. Rootless: `mv data/conf/app.ini /etc/gitea/app.ini`, `mv data/* /var/lib/gitea`, `mv repos/* /var/lib/gitea/git/repositories`.
After moving between install methods or directories, run `gitea admin regenerate hooks` (with `-c <app.ini>`) or pushes fail because hook paths are stale; `gitea doctor check` (optionally `--fix`) diagnoses leftovers.

## Converting database type
Not well tested. Stop Gitea, take a full backup, run `gitea doctor check --all --fix` and `gitea doctor recreate-table` on the source, then `gitea dump --database postgres` and extract `gitea-db.sql`. Create the target user/DB and import with `SET synchronous_commit TO off`, `SET on_error_stop TO on`, `\i gitea-db.sql` (faster, less crash-safe, acceptable because you hold a backup). Finally point `app.ini` at the new DB.

## Checked

2026-11-03: read https://docs.gitea.com/administration/backup-and-restore/, https://docs.gitea.com/administration/command-line/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
