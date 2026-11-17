---
id: computing-software.data-engineering.snowflake.create-or-alter-declarative-ddl
name: create-or-alter-declarative-ddl
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, create-or-alter, declarative-ddl, schema-management, devops]
level: advanced
status: docs-checked
description: "Manage Snowflake objects declaratively with CREATE OR ALTER: what it changes, what it drops, supported object types, and safe use in CI/CD."
sources:
  - https://docs.snowflake.com/en/sql-reference/sql/create-or-alter
  - https://docs.snowflake.com/en/sql-reference/sql/create-table#create-or-alter-table
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Declarative DDL with CREATE OR ALTER

**Goal:** keep object definitions as the desired state in git and apply them idempotently, without hand-written ALTER scripts or data-destroying CREATE OR REPLACE.

## Behaviour
```sql
CREATE OR ALTER TABLE core.customers (
  customer_id NUMBER NOT NULL,
  email       VARCHAR,
  segment     VARCHAR DEFAULT 'unknown',      -- new column: added
  created_at  TIMESTAMP_NTZ
) DATA_RETENTION_TIME_IN_DAYS = 7 CHANGE_TRACKING = TRUE;
```
- Object missing: created.
- Object exists: Snowflake computes the difference and applies ALTERs; **data and grants are kept** (unlike CREATE OR REPLACE).
- Columns in the table but **not in the statement are dropped**. A renamed column becomes drop + add: data loss.
- Unsupported changes fail the statement. In rare cases (an extremely wide table) a subset of changes might already have been applied, so check the object state after a failure.

Supported for many object types (the reference lists them, including TABLE, DATABASE, DATABASE ROLE, FILE FORMAT, FUNCTION, NETWORK RULE, PIPE, PROCEDURE, TASK, VIEW and VERSIONED SCHEMA, some in Preview); check the reference for the current list and per-type limits. CREATE OR ALTER does not support data governance changes.

## Workflow
- Apply each file with whatever runs SQL in your pipeline. One file per object, desired state only.
- Renames: separate migration (`ALTER TABLE ... RENAME COLUMN`) applied before the declarative file is updated.
- CI: run against a test copy of prod first and diff `DESCRIBE TABLE` before/after.

## When to prefer migrations
Data backfills, renames, splitting columns, ordered multi-step changes. Many teams combine: declarative for objects, migrations for data changes.

## Gotchas
- Tables managed by dbt should stay with dbt; do not manage the same object two ways.
- Comments, tags, policies: check whether omission removes them for your object type before relying on it.

## Verify
Apply twice: second run is a no-op. Apply to a clone with a removed column only after confirming the drop is intended.

## Checked

2026-10-28: reviewed against the official documentation fetched this batch.

Confirmed on the CREATE OR ALTER and CREATE TABLE (CREATE OR ALTER TABLE) pages: the list of supported object types, data and privilege grants preserved, columns missing from the new definition are dropped, a renamed column cannot be detected (drop and add), and in a rare case of an extremely wide table a subset of changes might be applied before a failure. RENAME COLUMN is on the ALTER TABLE page.

Removed: the Snowflake CLI command and name, the zero-copy clone wording, and the schemachange/Flyway names (not on the pages read).

Method: documentation only; no commands were run.
