---
id: computing-software.database-administration.postgresql.pg-dumpall-globals-roles-and-tablespaces
name: pg-dumpall-globals-roles-and-tablespaces
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-dump, pg-dumpall, globals-only, roles-only, logical-backup, role-passwords, cluster-migration]
level: practitioner
status: verified
description: "Back up PostgreSQL cluster-wide objects (roles, passwords, tablespaces, role settings) with pg_dumpall --globals-only and restore them before per-database dumps."
sources:
  - https://www.postgresql.org/docs/current/app-pg-dumpall.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pg_dumpall for globals

**Goal:** a restore onto a fresh server recreates the roles and their memberships
before the database dumps need them as owners and grantees.

## What pg_dump misses
Roles, role memberships, role passwords, per-role/per-database settings
(`ALTER ROLE ... SET`), and tablespaces are cluster-global. Without them,
`pg_restore` fails with `role "app_owner" does not exist` on every object.

## Commands
```bash
pg_dumpall -h db -U postgres --globals-only > globals.sql      # roles + tablespaces
pg_dumpall --roles-only > roles.sql
pg_dumpall --globals-only --no-role-passwords > globals_nopw.sql   # for non-superuser runs / sharing
```
Full cluster in one plain SQL file (`pg_dumpall > all.sql`) works for small
clusters but restores serially; prefer globals + per-database `pg_dump -Fd`.
Recent releases (seen in 18.6; see the `--restrict-key` option in the pg_dumpall docs) wrap the plain
script in psql `\restrict <key>` / `\unrestrict <key>` lines, so restore it with a psql new enough to
understand them.

## Restore order
```bash
psql -U postgres -d postgres -f globals.sql        # errors for existing roles (postgres) are expected
for db in app reporting; do createdb -T template0 $db; pg_restore -d $db -j 8 /backups/$db; done
```

## Gotchas
- Password verifiers are dumped exactly as stored (a role with an md5 hash is restored with
  that md5 hash; SCRAM roles keep their `SCRAM-SHA-256$...` verifier). Re-set md5 passwords if you are moving to SCRAM.
- `--no-role-passwords` reads role data from `pg_roles` instead of the superuser-only `pg_authid`, so
  it works without superuser rights, but restored roles have a null password and password logins fail
  until one is set.
- Tablespace paths in the dump must exist on the target or be edited.
- The globals file contains password hashes: protect it like a credential.

## Verify
- `grep -c '^CREATE ROLE' globals.sql` matches `SELECT count(*) FROM pg_roles WHERE rolname !~ '^pg_';`.
- On the target, `\du` matches the source and a dump restore produces no
  missing-role errors.

## Checked
- PostgreSQL 18.6: `pg_dumpall --globals-only` wrote 5 `CREATE ROLE` lines and 1 `CREATE TABLESPACE` (count matched `SELECT count(*) FROM pg_roles WHERE rolname !~ '^pg_'` = 5); `--roles-only` wrote no tablespace; `--globals-only --no-role-passwords` wrote no `PASSWORD` clauses; role memberships and `ALTER ROLE ... SET work_mem` were included; the output contained `\restrict` / `\unrestrict` lines. Restoring `globals.sql` into a second cluster printed `role "postgres" already exists` (expected) and a tablespace error because the directory was already in use (the tablespace path must exist and be unused on the target). Roles with md5 and SCRAM verifiers were dumped as stored. `pg_dump -Fd -j 2`, `createdb -T template0` and `pg_restore -j 4` round-tripped a 1000-row table.
- Docs (pg_dumpall page): `--globals-only` = roles and tablespaces, `--no-role-passwords` text, `--restrict-key`.
