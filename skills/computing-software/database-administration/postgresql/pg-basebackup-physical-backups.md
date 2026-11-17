---
id: computing-software.database-administration.postgresql.pg-basebackup-physical-backups
name: pg-basebackup-physical-backups
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-basebackup, pg-basebackup-options, continuous-archiving, physical-backup, incremental-backup, pg-combinebackup, wal-method, replica-seeding]
level: practitioner
status: verified
description: "Take physical base backups with pg_basebackup (WAL included, checksummed manifests, PG17 incremental backups) to seed replicas or as the base for PITR."
sources:
  - https://www.postgresql.org/docs/current/app-pgbasebackup.html
  - https://www.postgresql.org/docs/current/app-pgcombinebackup.html
  - https://www.postgresql.org/docs/current/app-pgverifybackup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pg_basebackup

**Goal:** a self-contained, verifiable copy of the whole cluster, taken online.

## Typical invocations
```bash
# Self-contained backup (includes the WAL needed to make it consistent)
pg_basebackup -h primary -U replicator -D /backups/base_$(date +%F) \
  -Ft -z -X stream -c fast -P --manifest-checksums=SHA256

# Seed a new streaming replica directly into its data dir
pg_basebackup -h primary -U replicator -D <standby-datadir> -Fp -X stream -c fast -R -S standby1 -C
```
- `-X stream` streams WAL over a second connection during the backup so the
  copy is consistent on its own. `-X none` relies on your WAL archive.
- `-c fast` forces an immediate checkpoint instead of waiting for the next
  spread one (backup otherwise "hangs" at start for up to checkpoint_timeout).
- `-R` writes `standby.signal` and `primary_conninfo`; `-S/-C` create and use a
  replication slot so the primary keeps WAL until the standby connects.
- `--max-rate=100M` throttles to protect production I/O.
- `-T OLD=NEW` remaps tablespace paths.

## Incremental backups (PG17)
Requires `summarize_wal = on` on the server.
```bash
pg_basebackup -D full0 ...
pg_basebackup -D incr1 --incremental=full0/backup_manifest ...
pg_combinebackup full0 incr1 -o restored_datadir     # synthesise a full one to restore
```

## Permissions
The user needs `REPLICATION` attribute and a `replication` line in pg_hba.conf:
`hostssl replication replicator 10.0.0.0/8 scram-sha-256`. Uses one of
`max_wal_senders` (two with `-X stream`).

## Gotchas
- A backup without its WAL is useless: tar format with `-X fetch/stream`
  puts WAL in `pg_wal.tar`; keep it with base.tar.
- Not a retention system: no catalogue, no expiry, no parallelism. For
  production backups use pgBackRest or barman; pg_basebackup is ideal for
  seeding replicas.
- Throughput is single-stream; multi-TB clusters take many hours.

## Verify
```bash
pg_verifybackup /backups/base_2026-10-16       # checks manifest checksums and WAL presence (plain format)
```
Periodically restore and start it with `recovery_target = 'immediate'`.

## Checked
- PostgreSQL 17.6 (local primary): `-Fp -X stream -c fast --manifest-checksums=SHA256` and `-Ft -z` both work and write `backup_manifest`; `-R -S name -C` writes `standby.signal`, `primary_conninfo`, `primary_slot_name` and creates a physical slot; `--incremental` fails with `incremental backups cannot be taken unless WAL summarization is enabled` until `summarize_wal = on`, then `full0` + incremental + `pg_combinebackup` builds a datadir that `pg_verifybackup` accepts; `--max-rate`, `-T` and `--incremental` exist.
