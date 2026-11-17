---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.idempotent-and-two-phase-mutations
name: idempotent-and-two-phase-mutations
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [two-phase-mutation, idempotent-mutations, data-pipelines, idempotency-keys, staging-tables, atomic-swap]
level: advanced
status: docs-checked
description: "Make pipeline writes safe to retry: idempotent mutations and two-phase mutations that stage, validate, then publish, including Iceberg write-audit-publish."
sources: ["https://sre.google/workbook/data-processing/", "https://iceberg.apache.org/docs/latest/branching/", "https://iceberg.apache.org/docs/latest/spark-procedures/", "https://www.postgresql.org/docs/current/sql-insert.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Idempotent and two-phase mutations

SRE Workbook, Data Processing Pipelines, "Idempotent and Two-Phase Mutations":

- **Idempotent mutation**: can be applied multiple times with the same result, so separate executions of a
  pipeline with the same input always produce the same result. It prevents storing duplicate or incorrect data
  when a failed pipeline reprocesses data. The Workbook also notes you do not need "exactly once" semantics if
  work units are idempotent and can be performed more than once for the same result.
- **Two-phase mutation**: instead of applying a mutation straight away, the mutations are stored in a temporary
  location; a separate verification step (or pipeline) validates them for correctness; a follow-up step applies
  the verified mutations only after they pass. This helps when testing or canarying a pipeline, where the owner
  must decide whether the applied mutations are acceptable.

## Idempotent writes
- Deterministic output locations that a rerun overwrites rather than appends to.
- Upserts keyed by a business key. In PostgreSQL, `INSERT ... ON CONFLICT (...) DO UPDATE SET ...` turns a
  uniqueness violation into an update; the proposed row is available as `EXCLUDED`, and `UPDATE` privilege is
  also needed.
```sql
INSERT INTO daily_revenue (day, customer_id, revenue) VALUES ($1, $2, $3)
ON CONFLICT (day, customer_id) DO UPDATE SET revenue = EXCLUDED.revenue;
```
- Idempotency keys for external side effects: store the key with the effect and skip if seen (a design pattern
  you implement; the Workbook gives no specific mechanism).

## Two-phase pattern
1. Write to a staging location, not where consumers read.
2. Validate against the contract you care about (row counts, nulls, schema, drift against the previous run).
3. Publish only if validation passes; otherwise discard.
4. Keep the previous version for rollback. The Workbook also advises tying code changes to a release for fast
   rollbacks and having tested backup and restore procedures.

### Iceberg write-audit-publish
Iceberg branching supports this directly (Spark SQL):
```sql
ALTER TABLE db.table SET TBLPROPERTIES ('write.wap.enabled'='true');
ALTER TABLE db.table CREATE BRANCH `audit-branch`;
SET spark.wap.branch = audit-branch;   -- writes now go to the audit branch, independent of main history
-- validate the audit branch (for example data quality checks), then publish:
CALL catalog_name.system.fast_forward('prod.db.table', 'main', 'audit-branch');
```
`fast_forward` moves the `main` branch to the head of the audit branch. Iceberg also has `publish_changes` for
publishing a staged snapshot by its WAP ID. Check the Iceberg pages for retention options on branches.

## Gotchas
- Validation thresholds are yours to define; too tight blocks legitimate changes, so allow an approved override.
- Consumers reading staging locations defeat the pattern; restrict access.
- Avoid putting personally identifiable information in temporary storage; if you must, encrypt it (Workbook).

## Verify
- [ ] Rerun of any day produces identical output (checksum).
- [ ] A deliberately broken output is blocked at validation and never published.

## Checked

Checked 2026-11-09. Confirmed against the SRE Workbook Data Processing Pipelines page (idempotent and two-phase mutation descriptions), the Iceberg branching and Spark procedures pages (write.wap.enabled, spark.wap.branch, fast_forward, publish_changes) and the PostgreSQL INSERT page (ON CONFLICT, DO UPDATE, EXCLUDED). Removed: Snowflake SWAP, the Postgres rename-in-a-transaction recipe, Spark dynamic partition overwrite, the numeric validation thresholds and the file manifest pointer pattern, which no page read supported.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
