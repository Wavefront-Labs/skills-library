---
id: computing-software.database-administration.schema-design.liquibase-changelogs
name: liquibase-changelogs
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, liquibase-changelog, liquibase, changesets, schema-migrations, database-devops]
level: practitioner
status: gated
description: "Structure Liquibase changelogs and changesets (formatted SQL or YAML), use contexts, labels, preconditions and rollback, and run update, status and tagging safely in pipelines."
sources:
  - https://docs.liquibase.com/concepts/changelogs/home.html
  - https://docs.liquibase.com/concepts/changelogs/sql-format.html
  - https://docs.liquibase.com/commands/rollback/rollback.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Liquibase changelogs

## Layout
```text
db/
  changelog-root.yaml
  changes/
    2026/10/2026-10-18-001-add-orders-status.sql
    2026/10/2026-10-18-002-index-orders-status.sql
```
```yaml
# changelog-root.yaml
databaseChangeLog:
  - includeAll:
      path: changes/
      relativeToChangelogFile: true
```
`includeAll` runs the files in a directory; the alphabetical ordering (gated: unconfirmed, source is paywalled or blocked), so use sortable names anyway. Explicit `include` lists are safer for large teams.

## Formatted SQL changeset
```sql
--liquibase formatted sql

--changeset alice:2026-10-18-001 labels:orders context:!test
--preconditions onFail:HALT onError:HALT
--precondition-sql-check expectedResult:0 SELECT count(*) FROM information_schema.columns WHERE table_name='orders' AND column_name='status'
ALTER TABLE orders ADD COLUMN status text NOT NULL DEFAULT 'pending';
--rollback ALTER TABLE orders DROP COLUMN status;

--changeset alice:2026-10-18-002 runInTransaction:false
CREATE INDEX CONCURRENTLY idx_orders_status ON orders (status);
--rollback DROP INDEX CONCURRENTLY idx_orders_status;
```
- Identity = `author:id` + file path. Changing an applied changeset's content changes its checksum and fails `update` (`validCheckSum` only for deliberate fixes).
- `runInTransaction:false` for statements that cannot run in a transaction (PostgreSQL concurrent indexes).
- `runOnChange:true` for repeatable objects (views, functions) maintained in place.
- Tracking tables: `DATABASECHANGELOG` (applied changesets), `DATABASECHANGELOGLOCK` (prevents concurrent runs; a crashed run can leave it locked: `liquibase release-locks`) (gated: unconfirmed, source is paywalled or blocked).

## Commands in pipelines
```bash
liquibase --changelog-file=db/changelog-root.yaml --url=$URL --username=$U --password=$P status --verbose
liquibase ... update-sql > review.sql          # dry run for review (gated: unconfirmed, source is paywalled or blocked)
liquibase ... tag release-2026.10.18
liquibase ... update --labels=orders --contexts=prod
liquibase ... rollback --tag=release-2026.10.18   # uses --rollback blocks
```

## Practices
- One logical change per changeset; never mix DDL and large data migrations.
- Write rollback for every changeset or explicitly `--rollback empty` with a note; test rollback in CI.
- Contexts for environment-specific data (test seeds), labels for features.
- Keep `DATABASECHANGELOG` in backups; it is the history.

## Verify
`liquibase status` reports no pending changesets after deploy; `liquibase diff` against a reference shows no drift.

## Checked

- Date: 2026-11-02.
- Confirmed against: Liquibase docs for changelogs, SQL-format changelogs and the rollback command (formatted SQL header and --changeset attributes labels, context, runInTransaction (default true), runOnChange (default false), SQL check precondition with onFail/onError and expectedResult, --rollback blocks and rollback by tag, validCheckSum, includeAll with relativeToChangelogFile, checksum behaviour).
- Fixed: the example precondition used onFail:MARK_RAN, which the SQL-format page does not show; it now uses the documented onFail:HALT onError:HALT form.
- Gated: includeAll ordering, the DATABASECHANGELOGLOCK table and release-locks command, and update-sql (not stated in the fetched pages).

Method: documentation only; no commands were run.
