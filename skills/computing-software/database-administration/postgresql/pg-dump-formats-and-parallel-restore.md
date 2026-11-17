---
id: computing-software.database-administration.postgresql.pg-dump-formats-and-parallel-restore
name: pg-dump-formats-and-parallel-restore
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-dump, pg-dump-custom-format, pg-restore-parallel, pg-restore, logical-backup, directory-format, selective-restore, toc-list, pg-restore-list]
level: practitioner
status: verified
description: "Take pg_dump logical backups in custom or directory format, restore them in parallel with pg_restore -j, and do selective restores from the TOC list."
sources:
  - https://www.postgresql.org/docs/current/app-pgdump.html
  - https://www.postgresql.org/docs/current/app-pgrestore.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# pg_dump formats and parallel restore

**Goal:** logical dumps that restore fast and let you pull back one table.

## Pick the format
| `-F` | Output | Parallel dump | Parallel restore | Selective restore |
|---|---|---|---|---|
| `p` plain | SQL script | no | no (psql) | edit the text |
| `c` custom | one compressed file | no | yes | yes |
| `d` directory | one file per table | yes (`-j`) | yes | yes |
| `t` tar | tar | no | no | yes |
Default for anything over a few GB: directory format.
```bash
pg_dump -h db -U backup -d app -Fd -j 8 -Z zstd:3 -f /backups/app_$(date +%F)   # PG16+ zstd
pg_dump -d app -Fc -f app.dump                                                   # single file
```
`-j` needs `-j + 1` connections and takes ACCESS SHARE locks on every table up
front: concurrent DDL blocks until the dump ends.

## Restore
```bash
createdb -T template0 app_restored
pg_restore -d app_restored -j 8 --no-owner --role=app_owner /backups/app_2026-10-16
```
- `--no-owner --no-privileges` when restoring into a different environment.
- `--exit-on-error` (or `-e`); otherwise pg_restore continues and reports errors at the end.
- `-1/--single-transaction` cannot combine with `-j`.
- After restore: `vacuumdb --analyze-in-stages -d app_restored` (stats are not dumped before PG18).

## Selective restore
```bash
pg_restore -l app.dump > toc.list         # edit: comment out lines with ;
pg_restore -L toc.list -d app_restored app.dump
pg_restore -d app_restored -t invoices -n billing app.dump   # one table: data + definition only (17.6: no primary key or sequence), target schema must already exist
pg_restore --section=pre-data|data|post-data ...             # schema, data, then indexes/constraints
```

## Gotchas
- pg_dump does not include roles or tablespaces: also run `pg_dumpall --globals-only`.
- Large objects are included only for whole-database dumps or with `-b`.
- A dump is consistent as of its start (one snapshot), but long dumps hold that
  snapshot: vacuum cannot clean newer dead tuples meanwhile; on primaries this
  bloats busy tables. Dump from a replica, where recovery conflicts can cancel a long dump (see the
  hot-standby-query-conflicts skill).
- Restore with a newer pg_restore than the dump's server version is fine; the
  reverse is not.

## Verify
- `pg_restore -l <dump> | head` lists the TOC (the file is readable).
- Restore into a scratch database regularly and compare row counts on key tables.

## Checked
- PostgreSQL 17.6 on a two-schema scratch database: all four `-F` formats dump; `-j` with `-Fc` fails (`parallel backup only supported by the directory format`); `-Fd -j 4` and `-Z zstd:3` work (PG16 notes add LZ4/Zstandard); `pg_restore -j` into a directory dump works and fails for tar (`parallel restore is not supported with this archive file format`); `-1` with `-j` is refused; a plain-format file is refused by pg_restore; `-e` stops at the first error while the default continues and ends with `errors ignored on restore: N`; `-l` and `-L` skip chosen entries; `--section` splits CREATE TABLE, COPY and PRIMARY KEY; pg_dump omits roles and `pg_dumpall --globals-only` includes them; large objects are included in whole-database dumps and with `-b`, not with `-n`; no statistics in the 17 TOC (18 notes add `--statistics`); `vacuumdb --analyze-in-stages` ran. The pg_dump manual states `njobs + 1` connections and ACCESS SHARE locks.
