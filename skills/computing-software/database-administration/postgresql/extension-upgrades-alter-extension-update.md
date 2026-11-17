---
id: computing-software.database-administration.postgresql.extension-upgrades-alter-extension-update
name: extension-upgrades-alter-extension-update
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgres-extensions, create-extension, alter-extension-update, extension-versions, pg-available-extensions, postgis-upgrade, shared-preload-libraries, update-extensions-sql]
level: practitioner
status: docs-checked
description: "Upgrade PostgreSQL extensions safely: package vs catalog versions, ALTER EXTENSION UPDATE per database, preload libraries, and extension compatibility before major upgrades."
sources:
  - https://www.postgresql.org/docs/current/sql-alterextension.html
  - https://www.postgresql.org/docs/current/extend-extensions.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Upgrading extensions

**Goal:** after an OS package update, every database's extensions are on the new
version, and major-version upgrades are not blocked by a missing extension build.

## Two versions exist
- **Installed files** (shared library + SQL scripts from the OS package):
  `pg_available_extensions.default_version`.
- **Catalog version** in each database: `pg_extension.extversion`.
A package upgrade replaces the files on disk but each database's catalog version stays
old until you run `ALTER EXTENSION ... UPDATE`. Without a version argument it updates to the
`default_version` in the extension's control file.

## Find stale ones (per database)
```sql
SELECT e.extname, e.extversion, a.default_version
FROM pg_extension e JOIN pg_available_extensions a ON a.name = e.extname
WHERE e.extversion <> a.default_version;
```
## Update
```sql
ALTER EXTENSION pg_stat_statements UPDATE;          -- to default_version
ALTER EXTENSION some_extension UPDATE TO '<new_version>';   -- needs an update script path from the installed version
SELECT * FROM pg_extension_update_paths('some_extension');    -- check for unexpected or missing update paths
```
Run in **every** database that has it (loop over `pg_database`). Libraries listed in
`shared_preload_libraries` are loaded at server start, so restart after replacing their files.

## Before a major version upgrade
- Install the extension's shared object files for the new server version before running
  pg_upgrade; do not run `CREATE EXTENSION` in the new cluster (the schema definitions come from the old one).
- Check each extension's own documentation for upgrade prerequisites; third-party extensions may have their own procedures.
- After pg_upgrade, if extension updates are available it reports this and creates a script
  that you can run later to update them (otherwise run `ALTER EXTENSION ... UPDATE` yourself).

## Gotchas
- `ALTER EXTENSION UPDATE` works only if the extension supplies a suitable update script (or series of scripts) from the installed version to the requested one; it is not a downgrade mechanism. Take a backup before major extension jumps.
- Test update duration on a copy, since an update script can do real work.
- Managed services control which versions are available; check the provider's documentation.

## Verify
The stale query returns no rows in every database; `\dx` shows expected versions.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): ALTER EXTENSION reference (UPDATE needs a suitable update script or series of scripts; omitted version means the control file's default version), "Packaging Related Objects into an Extension" (`default_version`, `pg_extension_update_paths()`), the `pg_available_extensions` columns (`default_version`, `installed_version`) and `pg_extension.extversion`, and pg_upgrade (install shared object files first; do not load schema definitions such as `CREATE EXTENSION`; reports available updates and creates a script). Removed the PostGIS-specific function and pinned version, the packaging names, the quoted `could not load library` message, the script file name and the claims about specific extensions, which the PostgreSQL documentation does not give.
Method: documentation only; no commands were run.
