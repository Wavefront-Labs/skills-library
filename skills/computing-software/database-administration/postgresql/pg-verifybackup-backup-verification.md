---
id: computing-software.database-administration.postgresql.pg-verifybackup-backup-verification
name: pg-verifybackup-backup-verification
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, pg-basebackup, pg-verifybackup, backup-manifest, backup-verification, restore-testing]
level: practitioner
status: verified
description: "Check a pg_basebackup against its backup_manifest with pg_verifybackup (files, checksums, required WAL), and know what it cannot prove compared with a test restore."
sources:
  - https://www.postgresql.org/docs/current/app-pgverifybackup.html
  - https://www.postgresql.org/docs/current/app-pgbasebackup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verifying base backups with pg_verifybackup

Since PG13, `pg_basebackup` writes a `backup_manifest` (JSON) listing every file with size
and checksum, plus the WAL range needed for consistency. `pg_verifybackup` checks a backup
against it.

## Taking a verifiable backup
```bash
pg_basebackup -h primary -U replicator -D /backups/base/2026-10-18 \
  -Fp -X stream -c fast -P --manifest-checksums=SHA256
```
- `--manifest-checksums`: `CRC32C` (default, fast), `SHA224/256/384/512` (stronger), `NONE`.
- `-Ft` (tar) is supported for verification from PG18; on older versions verify plain
  format, or extract tar first.

## Verifying
```bash
pg_verifybackup /backups/base/2026-10-18
# backup successfully verified
pg_verifybackup -n /backups/base/2026-10-18        # skip WAL parsing (WAL not in backup)
pg_verifybackup -w /archive/wal /backups/base/x    # check required WAL from another location
pg_verifybackup -i 'pg_log' /backups/base/x        # ignore a path
```
It reports: files missing or extra, size mismatches, checksum mismatches, manifest tampering
(manifest has its own checksum), and whether the WAL needed (from `pg_waldump` parsing) is
present and readable.

## What it does not prove
- That the data **inside** files is logically sound: a backup of an already-corrupt page
  verifies fine. Use data checksums (`initdb -k`) plus `pg_amcheck` on a restored copy.
- That WAL archived **after** the backup (needed for PITR) is complete.
- That your restore procedure, permissions and config work. Only a test restore that starts
  the server and runs queries proves that.

## In a backup pipeline
1. `pg_basebackup ... --manifest-checksums=SHA256`
2. `pg_verifybackup` immediately (catches truncated copies, full disks)
3. Copy to off-site storage; re-run `pg_verifybackup` after copy, or compare object checksums.
4. Weekly: restore to scratch, start with `recovery_target = 'immediate'`, run `pg_amcheck --all`.

Incremental backups (PG17 `--incremental`) have manifests too; verify each, and verify the
output of `pg_combinebackup` before relying on it.

## Gotchas
- Do not edit files (e.g. `postgresql.auto.conf` for a standby) inside the backup before
  verifying, or it fails with checksum mismatch. `-R` written files are already in the manifest.
- Third-party tools (pgBackRest `verify`, WAL-G `backup-verify`) have their own equivalents.

## Verify
Exit status 0 and `backup successfully verified`; deliberately corrupt a copy of one file
in a test to confirm your pipeline catches it.

## Checked
- PostgreSQL 17.6: a plain backup verifies (`backup successfully verified`, also with `-n`); a changed file reports the size mismatch, an extra file reports `present on disk but not in the manifest` (and `-i` ignores it), a removed file and an edited manifest report `present in the manifest but not on disk` and `manifest checksum mismatch`; a tar-format backup is rejected on 17 (18 notes add tar support); default manifest checksum is CRC32C; `-w`, `-n`, `-i`, `-q`, `-s`, `-e` exist; `pg_combinebackup` output verifies. PG13 notes introduce pg_verifybackup.
