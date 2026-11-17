---
id: computing-software.data-engineering.databricks.row-filters-and-column-masks
name: row-filters-and-column-masks
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, unity-catalog, row-filters, column-masks, dynamic-views, fine-grained-access-control, abac, is-account-group-member, pii-masking]
level: practitioner
status: docs-checked
description: "Restrict rows and mask columns in Unity Catalog: row filter and column mask functions, mapping tables, dynamic views, tag-based ABAC policies, compute requirements and testing."
sources:
  - https://docs.databricks.com/aws/en/tables/row-and-column-filters
  - https://docs.databricks.com/aws/en/views/dynamic
  - https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unity Catalog row filters and column masks

**Goal:** one table, many audiences — each user sees only permitted rows and unmasked columns, enforced in every engine that reads through Unity Catalog.

## 1. Row filter
```sql
CREATE FUNCTION gov.sec.region_filter(region STRING)
RETURN is_account_group_member('global_sales') OR (region = 'EU' AND is_account_group_member('eu_sales'));

ALTER TABLE prod.sales.orders SET ROW FILTER gov.sec.region_filter ON (region);
ALTER TABLE prod.sales.orders DROP ROW FILTER;
```
The function returns BOOLEAN; rows where it is false or NULL are not shown.

## 2. Column mask
```sql
CREATE FUNCTION gov.sec.mask_email(email STRING)
RETURN CASE WHEN is_account_group_member('pii_readers') THEN email
            ELSE concat('***@', substring_index(email, '@', -1)) END;

ALTER TABLE prod.crm.customers ALTER COLUMN email SET MASK gov.sec.mask_email;
-- mask using other columns
ALTER TABLE prod.crm.customers ALTER COLUMN ssn SET MASK gov.sec.mask_ssn USING COLUMNS (country);
```

## 3. Mapping tables scale better than CASE lists
```sql
CREATE TABLE gov.sec.user_regions (principal STRING, region STRING);
CREATE FUNCTION gov.sec.region_filter_map(row_region STRING)
RETURN EXISTS (SELECT 1 FROM gov.sec.user_regions m
               WHERE m.region = row_region AND (m.principal = current_user() OR is_account_group_member(m.principal)));
```
Keep the mapping table small and governed; access changes become data changes, not DDL.

## 4. Tag-based policies (ABAC) and dynamic views
- ABAC (recommended by Databricks for consistent rules across many tables): tag columns and tables with governed tags and define row filter / column mask **policies** at catalog or schema level with `CREATE POLICY`; table owners cannot override or remove them.
- Dynamic views: a view whose query uses group-membership functions such as `is_account_group_member()`; useful to expose a curated or transformed subset, but users must be denied the base table.

## 5. Requirements and gotchas
- Use `is_account_group_member()` for account-level groups.
- Dedicated access compute on Databricks Runtime 15.3 or below cannot read a table with row filters or column masks.
- Time travel is not supported with table-level row filters or column masks.
- Filters/masks are evaluated per row — keep functions simple; avoid heavy subqueries on large tables.
- Some features don't work on filtered tables (check the docs' limitations list, e.g. certain clone/sharing operations).

## Verify
- [ ] Query as a member of each audience group (or a test principal) returns only expected rows/masked values.
- [ ] The filter applies through every path: SQL warehouse, notebook, BI connector.
- [ ] Functions live in a governed schema users cannot modify.

## Checked

- 2026-10-28: confirmed on the row filters and column masks page (`ALTER TABLE ... SET ROW FILTER` / `SET MASK`, ABAC recommended and policies cannot be overridden by table owners, `CREATE POLICY`, `is_account_group_member()`, dedicated compute on Runtime 15.3 or below unsupported, no time travel with table-level filters).
- Removed: `is_member()` comparison, owner/admin exemption claim, mask return type rule, DML visibility claim, `EXECUTE AS` and the serverless filtering claim (not in the fetched pages).

Method: documentation only; no commands were run.
