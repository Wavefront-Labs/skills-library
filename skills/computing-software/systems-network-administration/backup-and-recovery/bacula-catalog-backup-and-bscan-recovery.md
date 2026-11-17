---
id: computing-software.systems-network-administration.backup-and-recovery.bacula-catalog-backup-and-bscan-recovery
name: bacula-catalog-backup-and-bscan-recovery
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [bacula, bacula-catalog, bscan, bootstrap-file, catalog-recovery, bareos, dbcheck]
level: advanced
status: docs-checked
description: "Protect and recover the Bacula catalog: nightly catalog backup job with bootstrap files kept off-host, restoring the catalog, and rebuilding it from volumes with bscan."
sources:
  - https://www.bacula.org/15.0.x-manuals/en/main/Catalog_Maintenance.html
  - https://www.bacula.org/15.0.x-manuals/en/utility/Volume_Utility_Tools.html
  - https://www.bacula.org/15.0.x-manuals/en/main/Bootstrap_File.html
  - https://www.bacula.org/15.0.x-manuals/en/main/Configuring_Director.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bacula catalog backup and bscan recovery

**Goal:** if the Director's database is lost, restores still work.

## The catalog
A MySQL or PostgreSQL database holding job, file and volume records. Without it Bacula does not know what is on which volume.

## Nightly catalog backup job
The manual's example backs up the catalog after the nightly save: a `BackupCatalog` job using the `Catalog` FileSet and a schedule that starts after the normal cycle (`WeeklyCycleAfterBackup`, `Run = Level=Full sun-sat at 1:10`):
```text
Job {
  Name = "BackupCatalog"
  Type = Backup
  Client = rufus-fd
  FileSet = "Catalog"
  Schedule = "WeeklyCycleAfterBackup"
  Storage = DLTDrive
  Messages = Standard
  Pool = Default
  RunBeforeJob = "/opt/bacula/scripts/make_catalog_backup.pl MyCatalog"
  RunAfterJob  = "/opt/bacula/scripts/delete_catalog_backup"
  Write Bootstrap = "/opt/bacula/working/BackupCatalog.bsr"
}
FileSet {
  Name = "Catalog"
  Include {
    Options { signature = MD5 }
    File = /opt/bacula/working/bacula.sql
  }
}
```
`make_catalog_backup.pl` takes the database password on the command line, which the manual says is acceptable only on machines with only trusted users; PostgreSQL has a `.pgpass` password file and MySQL has `.my.cnf` as alternatives.

## Bootstrap files
Always write a bootstrap file for the catalog job, and preferably write or copy it to another computer. It lets you quickly recover the database backup; without one recovery is possible but takes more work and longer. A bootstrap file specifies exactly which volumes and files to restore (see the Bootstrap File chapter).

`bextract` extracts files from a volume using a bootstrap file; its usage is `bextract [options] <device-name> <directory-to-store-files>` (`-b <file>` bootstrap, `-V` volume names separated by `|`). The manual calls it a last resort ("if you find yourself using bextract, you probably have done something wrong"):
```bash
bextract -b BackupCatalog.bsr /dev/nst0 /tmp/catalog-restore
```
The restored file is the catalog dump (`bacula.sql`); reload it into the database with your database's own tools. `bextract` cannot restore ACLs or encrypted files.

## No catalog backup: rebuild with bscan
`bscan` re-creates catalog records from the volumes. The manual calls it a last resort too: the best recovery is reloading the catalog backup via its bootstrap file, and scanning volumes is slow. Take an ASCII backup of the database first, because bscan modifies the catalog.

Preconditions for an empty database: SQL server running, the `bacula` database and tables created from the scripts in the `cats` directory, and the Director started and stopped once with the proper `bacula-dir.conf` so Client and Storage records exist (they are not stored on volumes).

Without `-s` it only reports what it would do:
```bash
bscan -c bacula-sd.conf -v -V Vol001\|Vol002 /dev/nst0
```
Add `-s` (store records in the database) and `-m` (update media info) to write:
```bash
bscan -s -m -c bacula-sd.conf -v -V Vol001\|Vol002 /dev/nst0
```
- For disk volumes, replace the device name with the directory that holds the volumes (it must match the Archive Device in the storage config).
- List all needed volumes in one command, in the order written; the command line is limited to 511 bytes, so for many volumes use a `.bsr` file of `Volume=` lines (not both).
- A rebuilt catalog is not identical: autochanger slots are not restored (use `update slots`), and Client records come from `bacula-dir.conf`.
- Scanned jobs that were pruned earlier are pruned again unless you change the Job and File retention times.

## Maintenance
- `dbcheck` finds (and with `-f` fixes) orphaned records and inconsistencies; the manual says you normally should not need to run it often.
- `File Retention` and `Job Retention` (Client and Pool resources; the Pool value takes precedence) set how long records stay in the catalog and affect only the catalog, not archived data. File records dominate catalog size: the manual's estimate is about 154 bytes per saved file.

## Checked
2026-11-07. Read: Catalog_Maintenance in full as fetched (the text starts mid-page at the BackupCatalog example and covers the example job, security notes, third-party databases and database size); Volume_Utility_Tools sections for bextract, bscan (usage, preconditions, examples, limits) and dbcheck; Bootstrap_File was only searched, not read in full; Configuring_Director read only the Pool File Retention and Job Retention text. Trimmed or removed: "PostgreSQL (recommended)", `Priority = 11`, `Write Bootstrap` with `%n`, `JobDefs`, the `psql bacula <` restore line, the `-c` flag on bextract (not in the page's usage), "email" as a bootstrap destination, "PostgreSQL vacuum/analyze", and the invented quarterly Verify step. Corrected: the example job is the manual's, not a shipped default.
Method: documentation only; no commands were run.
