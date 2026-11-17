---
id: computing-software.database-administration.postgresql.locale-providers-libc-icu-builtin
name: locale-providers-libc-icu-builtin
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, locale-provider, lc-collate, lc-ctype, icu, builtin-provider, collation, localization]
level: practitioner
status: docs-checked
description: "Pick the PostgreSQL locale provider (libc, icu or builtin C.UTF-8) for a cluster or database, set LC_COLLATE/LC_CTYPE, and avoid glibc-upgrade index corruption."
sources:
  - https://www.postgresql.org/docs/current/locale.html
  - https://www.postgresql.org/docs/current/app-initdb.html
  - https://www.postgresql.org/docs/current/collation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locale providers (libc / icu / builtin)

The provider decides who implements sorting (`LC_COLLATE`) and character classification (`LC_CTYPE`): the OS C library, the ICU library, or PostgreSQL itself.

| Provider | Pros | Risk |
|---|---|---|
| `libc` | default for `initdb`; uses the OS locale | the same locale name can behave differently across platforms and OS upgrades; indexes can corrupt if the definitions change |
| `icu` | ICU language-tag locales, rich options | results depend on the ICU library version, which is updated over time; PG records the version and warns |
| `builtin` | `C`, `C.UTF-8` and `PG_UNICODE_FAST` implemented inside PostgreSQL; the docs call `C.UTF-8` behaviour efficient and stable across versions | `C.UTF-8` collates by code point, not linguistically; only those three locales exist |

## Choosing at creation
```bash
initdb -D <DATA_DIR> --locale-provider=builtin --builtin-locale=C.UTF-8 --encoding=UTF8   # PG17+
initdb -D <DATA_DIR> --locale-provider=icu --icu-locale=en-US --locale=en_US.UTF-8
```
```sql
CREATE DATABASE app TEMPLATE template0 LOCALE_PROVIDER icu ICU_LOCALE 'en-US' LOCALE 'en_US.UTF-8';
CREATE DATABASE logs TEMPLATE template0 LOCALE_PROVIDER builtin BUILTIN_LOCALE 'C.UTF-8';
```
With ICU, `initdb` still selects and initializes libc locale settings (for legacy code), and the server must be built with ICU support. `C.UTF-8` is available only when the database encoding is UTF-8.

## Practical policy
- Use `builtin C.UTF-8` (or `C`) as the database default when you mainly need correctness and speed; add ICU collations on the specific columns/queries that need human ordering: `ORDER BY name COLLATE "en-x-icu"`.
- Use ICU database-wide when user-visible sorting matters everywhere and you can control ICU versions.

## Inspect
```sql
SELECT datname, datlocprovider, datcollate, datctype, datlocale, datcollversion FROM pg_database;
-- datlocprovider: c = libc, i = icu, b = builtin; datlocale is NULL for libc (datcollate/datctype are used instead)
SELECT pg_database_collation_actual_version(oid), datcollversion FROM pg_database WHERE datname = current_database();
```
Mismatch = the library changed since the database was created: reindex text indexes, then `ALTER DATABASE app REFRESH COLLATION VERSION;`.

## Gotchas
- `LC_COLLATE`/`LC_CTYPE` cannot be changed after creation; switching means dump/restore or logical replication into a new database.
- `LIKE 'abc%'` can use a plain B-tree index only under the `C` locale; otherwise create the index with `text_pattern_ops` (or `varchar_pattern_ops`), which compares character by character, and keep a default-class index for `<` and `>` comparisons.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): Locale Support and Collation Support chapters (providers `libc`, `icu`, `builtin`; builtin locales `C`, `C.UTF-8`, `PG_UNICODE_FAST` and the UTF-8 requirement for `C.UTF-8`; ICU results depend on the library version; libc behaviour varies by platform), initdb options (`--locale-provider`, `--builtin-locale`, `--icu-locale`; ICU still initializes libc settings), CREATE DATABASE `LOCALE_PROVIDER`, `BUILTIN_LOCALE`, `ICU_LOCALE`, `pg_database` columns `datlocprovider`, `datlocale`, `datcollversion`, ALTER COLLATION version notes, LC_COLLATE/LC_CTYPE fixed after creation, and the `*_pattern_ops` operator classes. Removed the per-provider version numbers, the physical-replica remark and the `daticulocale` remark, which the documentation checked does not give.
Method: documentation only; no commands were run.
