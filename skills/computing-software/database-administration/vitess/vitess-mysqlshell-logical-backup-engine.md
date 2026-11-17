---
id: computing-software.database-administration.vitess.vitess-mysqlshell-logical-backup-engine
name: vitess-mysqlshell-logical-backup-engine
category: computing-software
field: database-administration
product: vitess
tags: [backup, mysqlshell, logical-backup, backup-engine, restore, experimental]
level: advanced
status: docs-checked
description: "Use the experimental MySQL Shell backup engine in Vitess: flags, how the MANIFEST differs from the data location, and database and user restore caveats."
sources:
  - https://vitess.io/docs/25.0/user-guides/operating-vitess/backup-and-restore/creating-a-backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `mysqlshell` engine is marked EXPERIMENTAL. It takes logical backups: MySQL Shell dumps all data to tab-separated plain text. The docs give the motivation that physical backups can suffer silent corruption in rarely read pages, whereas a logical backup reads every row on the tablet. It needs the `mysqlsh` binary (included in MySQL distributions and Vitess containers); MySQL 8.0 is supported and 8.0.21 or later is recommended.

Unlike other engines, Vitess does not upload the data. MySQL Shell writes many (often thousands of) files into a target directory and needs its own direct access to object storage such as S3, GCS or Ceph. The Vitess backup location holds only the MANIFEST, which points at the real location and is used at restore to tell MySQL Shell where to load from.

Required flags: `--backup-engine-implementation=mysqlshell`, `--mysql-shell-backup-location string` (differs from the Vitess backup location), and `--mysql-shell-flags="-js"` (`-js` is mandatory; connection settings go here, or use MySQL Shell's `--credential-store-helper`).

Optional flags: `--mysql-shell-dump-flags` (for example `{"threads": 4}` as JSON), `--mysql-shell-load-flags`, `--mysql-shell-should-drain=false` (true moves the tablet to BACKUP type during the backup), and `--mysql-shell-speedup-restore=false` (on MySQL 8.0.21+ disables redo logs and the doublewrite buffer for the restore). If you set the load flags you must keep `updateGtidSet` as `replace`, `progressFile` empty and `skipBinlog` true; `loadUsers` defaults to false.

Caveats: MySQL stays running, so all databases except information_schema, mysql, ndbinfo, performance_schema and sys are backed up, and Vitess drops all databases on the host before the load. Users are saved separately; with `loadUsers: true` Vitess drops existing users (except internal ones and the current login) first because MySQL Shell fails if a user exists.

## Checked

2026-11-04. All claims confirmed in the Using mysqlshell (EXPERIMENTAL) section of the Creating a Backup page: how it works, flags, and limitations on databases and users.

Method: documentation only; no commands were run.
