---
id: computing-software.data-engineering.snowflake.projection-and-aggregation-policies
name: projection-and-aggregation-policies
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, projection-policy, aggregation-policy, privacy, data-governance]
level: sme
status: docs-checked
description: "Restrict how sensitive Snowflake columns and tables can be queried: projection policies (filter but not select) and aggregation policies (minimum group size)."
sources:
  - https://docs.snowflake.com/en/user-guide/projection-policies
  - https://docs.snowflake.com/en/user-guide/aggregation-policies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Projection and aggregation policies

**Goal:** allow analysis on sensitive data without allowing extraction of individual values.

## Projection policy: usable but not selectable
```sql
CREATE PROJECTION POLICY governance.policies.no_project_email
  AS () RETURNS PROJECTION_CONSTRAINT ->
  CASE WHEN IS_ROLE_IN_SESSION('PII_READER') THEN PROJECTION_CONSTRAINT(ALLOW => true)
       ELSE PROJECTION_CONSTRAINT(ALLOW => false) END;

ALTER TABLE crm.customers MODIFY COLUMN email
  SET PROJECTION POLICY governance.policies.no_project_email;
```
Other roles can still use `email` in WHERE and inner queries, but projecting it fails with a projection policy error. Add `ENFORCEMENT => 'NULLIFY'` to `PROJECTION_CONSTRAINT(ALLOW => false, ...)` to return NULL instead of failing. Do not return NULL from the policy body to deny projection. A joined unprotected table can still project matching values, so do not rely on the policy alone for join keys.

## Aggregation policy: only aggregates over big enough groups
```sql
CREATE AGGREGATION POLICY governance.policies.min_group_10
  AS () RETURNS AGGREGATION_CONSTRAINT ->
  CASE WHEN IS_ROLE_IN_SESSION('ANALYST_FULL') THEN NO_AGGREGATION_CONSTRAINT()
       ELSE AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 10) END;

ALTER TABLE health.visits SET AGGREGATION POLICY governance.policies.min_group_10;
```
Queries must aggregate; rows in groups smaller than 10 are placed in a remainder group (NULL group key) instead of being shown, and a query that cannot even fill a remainder group returns NULL in every field. Window functions and recursive CTEs are not allowed against an aggregation-constrained table, and the policy body cannot reference a UDF, table or view.

## Combine with
- Masking policies (transform value) and row access policies (filter rows) in the same account; projection and aggregation policies restrict the query result instead.
- A projection policy attaches to a column (`ALTER TABLE ... MODIFY COLUMN ... SET PROJECTION POLICY`, or `ALTER VIEW`); an aggregation policy attaches to a table or view (`ALTER { TABLE | VIEW } ... SET AGGREGATION POLICY`). Each column or table supports only one; use `FORCE` to replace atomically.

## Gotchas
- Enterprise Edition or higher.
- A projection constraint does not stop a determined actor from deducing values with deliberate queries (analysts can still group or join on hashes); the docs suit it to partners you already trust and advise omitting the column or using differential privacy where leakage must be prevented. A larger minimum group size makes it less likely that a record can be deduced from results.
- A projection policy on a table column carries over to views that reference that column. Test BI tools that issue `SELECT *` probes.

## Verify
As a restricted role: `SELECT email` fails, `WHERE email = ...` works; small-group aggregates appear only in the remainder row.

## Checked
2026-11-09. Confirmed against the Snowflake docs "Projection policies" and "Aggregation policies": Enterprise Edition requirement, policy signatures and the PROJECTION_CONSTRAINT, AGGREGATION_CONSTRAINT and NO_AGGREGATION_CONSTRAINT functions, MIN_GROUP_SIZE, ENFORCEMENT NULLIFY, remainder groups, the ALTER TABLE/VIEW assignment syntax, one policy per object, view carry-over, and the leakage caveats. Removed: the clean-room claim, tag-based assignment, and the claim that aggregation policies are inherited by views. IS_ROLE_IN_SESSION in the examples was confirmed on its own function page (checks the active primary or secondary role hierarchy).
Method: documentation only; no commands were run.
