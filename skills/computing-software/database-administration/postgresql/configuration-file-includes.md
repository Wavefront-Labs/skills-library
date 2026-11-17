---
id: computing-software.database-administration.postgresql.configuration-file-includes
name: configuration-file-includes
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, include-dir, include-if-exists, postgresql-conf, conf-d, configuration-management]
level: practitioner
status: verified
description: "Split postgresql.conf with include, include_if_exists and include_dir (conf.d) so config management owns drop-in files, and know which setting wins."
sources:
  - https://www.postgresql.org/docs/current/config-setting.html#CONFIG-INCLUDES
  - https://www.postgresql.org/docs/current/view-pg-file-settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration file includes (include_dir / conf.d)

## Directives
```ini
# end of postgresql.conf
include_if_exists = 'local.conf'      # optional file, no error if missing
include 'tuning.conf'                  # required: startup fails if absent
include_dir = 'conf.d'                 # every *.conf in the dir, sorted by C-locale filename
```
- Relative paths resolve from the directory of the file containing the directive.
- A missing `include` target is fatal (`could not open configuration file`, startup fails and reload keeps the old settings); a missing `include_if_exists` target is only logged (`skipping missing configuration file`).
- Files in `include_dir` load in **filename order** (`00-base.conf`, `50-memory.conf`, `90-local.conf`); non-`.conf` files and dotfiles are ignored.
- **Last setting wins**, across all files in read order. Put `include_dir` at the end of postgresql.conf so drop-ins override the shipped defaults.
- `postgresql.auto.conf` (ALTER SYSTEM) is always read last and beats everything.
- pg_hba.conf and pg_ident.conf support `include`, `include_if_exists`, `include_dir` too (PG16+).

## Who set this value?
```sql
SELECT name, setting, sourcefile, sourceline FROM pg_settings WHERE name = 'shared_buffers';
SELECT sourcefile, sourceline, name, setting, applied, error
FROM pg_file_settings WHERE name = 'shared_buffers' ORDER BY seqno;
```
`pg_file_settings` shows every occurrence; only the last has `applied = t` (earlier, overridden lines show `f` with no error, and so does an `ALTER SYSTEM` value that has not been reloaded yet). Rows with `error` not null would break a reload.

## Workflow
1. Write the drop-in (`conf.d/60-wal.conf`).
2. `SELECT * FROM pg_file_settings WHERE error IS NOT NULL;` — must be empty.
3. `SELECT pg_reload_conf();` then check `pending_restart` in pg_settings for restart-only parameters.

## Gotchas
- A setting later in postgresql.conf (after `include_dir`) silently overrides the drop-in. Keep the main file free of the parameters config management owns.
- A stale `postgresql.auto.conf` entry from an old `ALTER SYSTEM` beats your drop-in; `ALTER SYSTEM RESET name;` removes it.
- A syntax error in any included file makes reload ignore the whole change set (logged), and makes the next restart fail.

## Checked
- PostgreSQL 18.6 scratch clusters: `conf.d` with `10-mem.conf` (32MB) and `60-mem.conf` (64MB) plus the main file's 128MB gave `pg_settings.shared_buffers` 64MB from `60-mem.conf`; `pg_file_settings` listed three rows, only the last `applied = t`. With `10-b.conf`=7MB and `50-a.conf`=9MB the effective `work_mem` was 9MB; `.hidden.conf` and `zz.txt` in the directory were ignored; `ALTER SYSTEM SET work_mem='5MB'` then beat the drop-in (`sourcefile` = `postgresql.auto.conf`). A missing `include` made startup fail with `could not open configuration file`; `include_if_exists` logged `skipping missing configuration file`. A syntax error or unknown parameter in an included file on reload logged `contains errors; no changes were applied`.
- Docs (auth-pg-hba-conf and config-setting pages, 16 release notes): C-locale filename order, dotfiles and non-.conf skipped, relative to the including file; `include_dir` in pg_hba.conf appears in the 16 release notes and not in the 15 docs.
- Debian packaging note removed because it could not be run here.
