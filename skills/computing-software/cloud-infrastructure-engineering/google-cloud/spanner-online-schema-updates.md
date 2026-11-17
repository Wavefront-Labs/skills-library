---
id: computing-software.cloud-infrastructure-engineering.google-cloud.spanner-online-schema-updates
name: spanner-online-schema-updates
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, spanner, spanner-ddl-updates, schema-updates, liquibase, migrations]
level: practitioner
status: docs-checked
description: "Run Spanner DDL changes online: batching statements, long-running operations, backfill and validation phases, migration tools, and which changes are slow or blocked."
sources: ["https://docs.cloud.google.com/spanner/docs/schema-updates", "https://docs.cloud.google.com/sdk/gcloud/reference/spanner/databases/ddl/update", "https://docs.cloud.google.com/sdk/gcloud/reference/spanner/operations/list"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spanner online schema updates

Spanner applies DDL without downtime, but each change is a long-running operation (LRO) that may
backfill (new index) or validate existing data (NOT NULL, foreign key, type change).

## 1. Apply DDL in batches
```bash
gcloud spanner databases ddl update <DB> --instance=<I> --ddl-file=changes.sql --async
gcloud spanner operations list --instance=<I> --database=<DB> --type=DATABASE_UPDATE_DDL
gcloud spanner operations describe <OP> --instance=<I> --database=<DB>
```
- Batch related statements in one `--ddl-file`: the statements run as a batch, and if one fails, all subsequent statements in the batch are cancelled. Schema versions do not map one-to-one to statements or batches.
- Reads and writes continue during a schema update.
- `gcloud spanner databases ddl describe <DB>` dumps the current schema for review/diff.

## 2. Cost classes of change
| Fast (metadata only) | Validates / backfills (slow, proportional to data) |
|---|---|
| add or drop a non-key column (an added column cannot be NOT NULL), add or drop a table or index (table operations take minutes) | add NOT NULL to a non-key column, add a foreign key, reduce a column length, change BYTES to STRING, add a CHECK constraint, add a stored generated column; CREATE INDEX on an existing table takes minutes to hours |

- Add NOT NULL columns in steps: add nullable, backfill with partitioned DML
  (`gcloud spanner databases execute-sql --enable-partitioned-dml --sql="UPDATE T SET c='x' WHERE c IS NULL"`), then alter to NOT NULL.
- Validation and index builds can take minutes to many hours; an index created in the same batch as its base table takes minutes.

## 3. Migration tools
Schema migration tools such as Liquibase (Google documents a Spanner integration) keep an ordered changelog; run them from CI with a service account that can update the schema (for example `roles/spanner.databaseAdmin`). Keep each changeset to one logical change so a failed validation does not leave half a release applied.

## Gotchas
- A failed statement cancels the rest of its batch; use `operations describe` to see which statements were applied before reapplying.
- You can cancel a long-running data-validation operation with `gcloud spanner operations` (the documentation does not say whether this covers index backfills).
- GoogleSQL and PostgreSQL dialects use different DDL syntax; keep one dialect per changelog.

## Verify
- [ ] The operation shows `done: true` with no error.

## Checked
Checked 2026-10-24 against the Spanner schema-updates page and the gcloud `spanner databases ddl update` and `spanner operations list` references (docs.cloud.google.com). Confirmed the fast versus validating change classes, batching and failure behaviour, `--ddl-file`, `--async`, `--enable-partitioned-dml` and the `DATABASE_UPDATE_DDL` operation type. Removed the unconfirmed per-batch and per-week schema-update limits, primary-key change advice and the `INDEX_STATE` check. The Liquibase integration page was not read; only its existence is cited.
Method: documentation only; no commands were run.
