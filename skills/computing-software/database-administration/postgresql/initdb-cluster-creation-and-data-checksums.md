---
id: computing-software.database-administration.postgresql.initdb-cluster-creation-and-data-checksums
name: initdb-cluster-creation-and-data-checksums
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, initdb, initdb-options, data-checksums, postgres-server-setup, pg-checksums, locale, encoding, wal-segsize]
level: practitioner
status: verified
description: "Create a new PostgreSQL cluster with initdb choosing locale, encoding, auth defaults and data checksums correctly, since several of these cannot be changed later."
sources:
  - https://www.postgresql.org/docs/current/app-initdb.html
  - https://www.postgresql.org/docs/current/creating-cluster.html
  - https://www.postgresql.org/docs/current/app-pgchecksums.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating a cluster with initdb

**Goal:** a data directory whose irreversible choices (encoding, default locale
provider, checksums, WAL segment size) are made on purpose, not by whatever the
OS locale happened to be.

## The command
Run as the `postgres` OS user, into an empty directory it owns (mode 0700):
```bash
initdb -D /var/lib/postgresql/17/main \
  --encoding=UTF8 \
  --locale-provider=icu --icu-locale=und \   # or --locale-provider=builtin --builtin-locale=C.UTF-8 (PG17+, needs --encoding=UTF8)
  --lc-messages=C \
  --data-checksums \
  --auth-local=peer --auth-host=scram-sha-256 \
  --username=postgres --pwfile=<file-with-password>
```
Distro packages wrap initdb; check your wrapper's documentation for how to pass these options.

## What cannot be changed later
| Choice | Changeable? |
|---|---|
| Server encoding of `template1`/new DBs | Per database at CREATE DATABASE, but `template0` copy needed for a different one |
| `--wal-segsize` (default 16MB) | Only with `pg_resetwal --wal-segsize` offline; treat as fixed |
| Data checksums | Offline only: `pg_checksums --enable -D <datadir>` with the server cleanly shut down (rewrites every block; slow on big clusters) |
| Default collation provider | Per database at CREATE DATABASE; existing indexes depend on it |

PostgreSQL 18 enables checksums by default; on 17 and earlier you must ask.
The docs say checksums "might incur a small performance penalty"; they turn silent
storage corruption into a loud error, so enable them on new clusters. `--no-data-checksums` opts out on 18.

## Gotchas
- Collation settings affect the sort order of indexes, so the docs say they must stay fixed or text indexes become
  corrupt. With libc locales the order comes from the OS library, so an OS update that changes it has the same
  effect; the PG17 `builtin` C.UTF-8 provider does not depend on the OS; see the collation-version skill.
- `--locale=C` gives byte-order sorting (fast, stable) but `ORDER BY name` is not
  human-alphabetical; decide per database.
- Do not put the data directory on the mount point root: a failed mount then
  leaves an empty directory where initdb or the server may run against the
  wrong disk. Use a subdirectory.
- `--auth trust` (old default for local) on a multi-user host lets any OS user in
  as superuser. Set `--auth-local` and `--auth-host` explicitly.

## Verify
```sql
SHOW data_checksums;            -- on
SHOW server_encoding;           -- UTF8
SELECT datname, datlocprovider, datcollate, datlocale FROM pg_database;   -- datlocale since 17 (was daticulocale)
```
`pg_controldata -D <datadir> | grep -i checksum` shows `Data page checksum version: 1`.

## Checked
- PostgreSQL 18.6: `initdb --encoding=UTF8 --locale-provider=icu --icu-locale=und --lc-messages=C --auth-local=... --auth-host=scram-sha-256 --username=postgres --pwfile=...` succeeded and printed `Data page checksums are enabled`; `pg_controldata` showed `Data page checksum version: 1` and 16777216-byte WAL segments; `SHOW data_checksums` = on, `server_encoding` = UTF8; `--no-data-checksums` printed `Data page checksums are disabled`; `--locale-provider=builtin --builtin-locale=C.UTF-8` without UTF8 encoding failed (`requires encoding "UTF-8"`); `pg_database` has `datlocale` (the skill's `daticulocale` column no longer exists since 17: fixed). `pg_checksums --enable`/`--disable` exist.
- Docs: PG18 release notes (initdb now enables checksums by default, `--no-data-checksums`), initdb page (`--data-checksums` default, small performance penalty, builtin locale values `C`, `C.UTF-8`, `PG_UNICODE_FAST`), pg_checksums page (cleanly shut down), pg_resetwal page (`--wal-segsize` modifies a cluster without initdb), creating-cluster page (do not use a mount point itself), template0 section of the CREATE DATABASE docs, locale page (locale settings affect index sort order and must stay fixed), `trust` warning in the initdb page.
- Removed the Debian and RHEL wrapper commands (not run here); `--auth-local=peer` is documented but Unix-only.
