---
id: computing-software.database-administration.postgresql.collation-versions-icu-and-glibc-upgrades
name: collation-versions-icu-and-glibc-upgrades
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, managing-databases, icu-collation, collation-version, glibc-collation, glibc-upgrade, index-corruption, localization, builtin-locale]
level: advanced
status: docs-checked
description: "Detect and repair PostgreSQL text-index corruption after an OS glibc or ICU upgrade changes collation order, and choose a locale provider that avoids it."
sources:
  - https://www.postgresql.org/docs/current/collation.html
  - https://wiki.postgresql.org/wiki/Locale_data_changes
  - https://www.postgresql.org/docs/current/sql-alterdatabase.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collation versions and OS upgrades

**Goal:** an OS upgrade (or pg_upgrade to binaries linked with a newer ICU) never leaves
corrupt B-tree indexes on text columns.

## Why it breaks
With the libc provider, string comparison is delegated to the OS. If the collation
definitions change, existing indexes are ordered by the old rules and the
database can see corrupt indexes and other problems. The docs name two legitimate
causes: upgrading the operating system to a new major version, and using pg_upgrade
to move to server binaries linked with a newer ICU. For glibc, the C library version is
used as a proxy for the collation version, which is imperfect because maintainers can
back-port newer collation definitions to older releases.

## Detect
PostgreSQL records the collation version when a collation or database is created and
checks it on use, warning on a mismatch, for example (format from the ALTER COLLATION docs):
```
WARNING: collation "xx-x-icu" has version mismatch
DETAIL: The collation in the database was created using version 1.2.3.4, but the operating system provides version 2.3.4.5.
HINT: Rebuild all objects affected by this collation and run ALTER COLLATION pg_catalog."xx-x-icu" REFRESH VERSION, or build PostgreSQL with the right library version.
```
Version information is recorded for libc collations on glibc systems, FreeBSD and Windows (only for BCP 47 names on Windows), and for ICU collations on all platforms.
```sql
SELECT datname, datcollversion, pg_database_collation_actual_version(oid) FROM pg_database;
SELECT collname, collversion, pg_collation_actual_version(oid) FROM pg_collation
WHERE collversion IS DISTINCT FROM pg_collation_actual_version(oid);
```
Check index consistency with amcheck:
```sql
CREATE EXTENSION amcheck;
SELECT bt_index_check(c.oid, true) FROM pg_index i JOIN pg_class c ON c.oid=i.indexrelid
WHERE c.relam = (SELECT oid FROM pg_am WHERE amname='btree');   -- errors = corrupt
```

## Repair
1. Reindex every index that depends on the collation, concurrently where possible, while connected to that database:
   `REINDEX DATABASE CONCURRENTLY app;` This form does not process indexes on system catalogs; those need `REINDEX SYSTEM` (cannot be run with `CONCURRENTLY`).
2. Fix duplicates that a unique index now rejects (`could not create unique index`),
   then retry.
3. Record the new version so the warning stops:
   ```sql
   ALTER DATABASE app REFRESH COLLATION VERSION;
   ALTER COLLATION "de-x-icu" REFRESH VERSION;
   ```
Refreshing only records the current version and makes the warning go away; it does not check that affected objects were rebuilt.

## Avoid it
- New clusters: `--locale-provider=builtin --builtin-locale=C.UTF-8` (the docs describe the builtin
  locales `C`, `C.UTF-8` and `PG_UNICODE_FAST` as stable across versions) or the `C` collation
  for identifiers/keys; use ICU only where linguistic order matters.
- Plan OS major upgrades with this check in mind: after the upgrade, rebuild dependent indexes
  before refreshing the recorded version.

## Verify
- Version queries above return no mismatches; amcheck runs clean.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): ALTER COLLATION notes (version recorded at creation and checked on use, warning format, causes, `REINDEX` then `REFRESH VERSION`, platform coverage, glibc version used as proxy, the documented dependency query), ALTER DATABASE `REFRESH COLLATION VERSION`, the `pg_collation_actual_version` and `pg_database_collation_actual_version` functions, `pg_database.datcollversion`, REINDEX (`DATABASE` excludes system catalogs; `SYSTEM` does not support `CONCURRENTLY`), amcheck `bt_index_check(index, heapallindexed)` and the builtin locale description. Corrected: `REINDEX DATABASE` does not touch system-catalog indexes. Removed the glibc 2.28 claim, the specific version numbers in the example warning, and the physical-replica and PG17 remarks, which the documentation checked does not give.
Method: documentation only; no commands were run.
