---
id: computing-software.data-engineering.databricks.governed-tags-and-abac-policies
name: governed-tags-and-abac-policies
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, unity-catalog, abac-policies, governed-tags, attribute-based-access-control, column-masks, row-filters, data-classification]
level: advanced
status: docs-checked
description: "Scale Unity Catalog access control with governed tags and ABAC policies: tag columns once, define catalog/schema-level row filter and column mask policies that follow the tags."
sources:
  - https://docs.databricks.com/en/data-governance/unity-catalog/abac/index.html
  - https://docs.databricks.com/en/database-objects/tags.html
  - https://docs.databricks.com/en/tables/row-and-column-filters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Governed tags and ABAC policies

**Goal:** instead of attaching a mask function to each PII column on each table, tag columns and let one policy at catalog level mask everything tagged, including future tables.

## Building blocks
- **Governed tags:** account-level tag definitions with allowed values and permissions on who may assign them (e.g. `pii` with values `email`, `phone`, `ssn`). Assign to catalogs, schemas, tables, columns.
- **UDFs:** the mask/filter logic, ordinary SQL UDFs in UC.
- **ABAC policies:** attached to a catalog/schema/table; say "for columns matching tag condition X, apply mask UDF Y, for principals Z, except W".

## Example
```sql
-- 1. mask function
CREATE OR REPLACE FUNCTION gov.policies.mask_email(email STRING)
RETURNS STRING
RETURN CASE WHEN email IS NULL THEN NULL
            ELSE concat(left(email, 1), '***@', split_part(email, '@', 2)) END;

-- 2. tag columns (or let data classification suggest tags)
ALTER TABLE sales.crm.customers ALTER COLUMN email SET TAGS ('pii' = 'email');

-- 3. create a policy (CREATE POLICY) on the catalog that applies the mask to columns
--    carrying the tag; take the exact clauses from the ABAC documentation
```
Row filter policies exist too; use them to filter rows by a column for regional groups.

(ABAC syntax and availability evolved through preview; check the current docs for exact clauses on your workspace.)

## Why ABAC over per-table masks
- New tables with tagged columns are protected automatically.
- One place to audit who sees what.
- Tag assignment can be delegated to data stewards (governed tag permissions) while policy authoring stays with the governance team.

## Requirements and limits
- Dedicated access compute on Databricks Runtime 15.3 or below cannot read tables with row filters or column masks.
- Policies evaluate at query time; UDF performance matters (keep them simple, deterministic).
- Table owners cannot override or remove ABAC policies; exempt principals through the policy definition.

## Verify
- [ ] As a non-exempt user, `SELECT email FROM sales.crm.customers` returns masked values; as `pii_readers`, clear values.
- [ ] A new table with a column tagged `pii=email` is masked without further action.
- [ ] The PII columns you expect carry the governed tag (check in Catalog Explorer).

## Checked

- 2026-10-28: confirmed on the row filters and column masks page (ABAC policies attach at catalog or schema level using governed tags, `CREATE POLICY`, owners cannot override, dedicated compute on Runtime 15.3 or below unsupported) and the tags page (`SET TAGS`).
- Removed: the full `CREATE POLICY` clause list (`has_tag_value`, `TO`, `EXCEPT`, `MATCH COLUMNS`), the row filter policy syntax, the dedicated-compute serverless claim and the `information_schema.column_tags` check (not in the fetched pages).

Method: documentation only; no commands were run.
