---
id: computing-software.database-administration.schema-design.schema-drift-detection
name: schema-drift-detection
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, schema-drift, schema-comparison, migra, database-devops, schema-migrations]
level: practitioner
status: draft
description: "Detect schema drift between environments and migration history (hotfixes applied by hand, missed migrations) with diff tools, checksums and scheduled checks, then reconcile."
sources:
  - https://github.com/djrobstep/migra
  - https://docs.liquibase.com/commands/inspection/diff.html
  - https://atlasgo.io/declarative/diff
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Schema drift detection

**Drift** = the live schema differs from what migrations say it should be: an index created by hand during an incident, a column altered directly in production, a migration applied in staging but not prod.

## Detection methods
1. **Migration tool checks**
   - Flyway: `flyway validate` (checksums of applied scripts vs files), `flyway check -drift` (Enterprise) compares the target with a build from scripts.
   - Liquibase: `liquibase diff --referenceUrl=<expected-db>` and `diff-changelog` to generate fixes; `status` lists unapplied changesets.
   - Atlas: `atlas schema diff --from <url> --to file://schema.hcl` or `atlas migrate validate`.
2. **Dump-and-diff**: build a clean database from migrations in CI, dump schema (`pg_dump -s --no-owner --no-privileges`, `mysqldump --no-data --skip-comments`, SQL Server SqlPackage `/Action:Extract` or Schema Compare), dump production the same way, normalise and diff.
3. **Dedicated diff tools**: `migra` (PostgreSQL, outputs SQL to reconcile), `pgquarrel`, `mysqldiff`/Skeema, Redgate SQL Compare, SqlPackage `DeployReport`.

## Schedule it
Nightly job per environment:
```bash
pg_dump -s --no-owner --no-privileges -h prod-db app | sed '/^--/d;/^SET /d' > prod.sql
pg_dump -s --no-owner --no-privileges -h ci-built-db app | sed '/^--/d;/^SET /d' > expected.sql
diff -u expected.sql prod.sql > drift.diff || notify "schema drift detected" drift.diff
```
Ignore intentional differences explicitly (environment-specific grants, partitions created by schedulers) with filters, not by tolerating noise.

## Prevent drift
- No DDL privileges for humans in production except a break-glass role with auditing (DDL event triggers in PostgreSQL, DDL triggers in SQL Server, `audit_log` in MySQL).
- Every hotfix gets back-ported as a migration the same day.
- Event trigger logging DDL:
```sql
CREATE TABLE ddl_log (at timestamptz DEFAULT now(), usr text DEFAULT current_user, tag text, cmd text);
CREATE FUNCTION log_ddl() RETURNS event_trigger LANGUAGE plpgsql AS $$
BEGIN INSERT INTO ddl_log(tag, cmd) VALUES (tg_tag, current_query()); END $$;
CREATE EVENT TRIGGER ddl_audit ON ddl_command_end EXECUTE FUNCTION log_ddl();
```

## Reconcile
Decide per difference: codify it (new migration that matches prod) or revert prod. Never silently edit already-applied migration files (checksum failures, broken history).

## Verify
The nightly diff is empty for every environment, and the DDL log shows only migration-tool users.
