---
id: computing-software.data-engineering.snowflake.access-history-auditing
name: access-history-auditing
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, access-history, auditing, column-level-lineage, base-objects-accessed, objects-modified, sensitive-data-access, unused-tables, account-usage, access-auditing]
level: advanced
status: docs-checked
description: "Audit Snowflake access with ACCESS_HISTORY: who read which columns, flattening base objects, write lineage via objects_modified, PII access reports, unused tables."
sources:
  - https://docs.snowflake.com/en/user-guide/access-history
  - https://docs.snowflake.com/en/sql-reference/account-usage/access_history
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ACCESS_HISTORY auditing

**Goal:** answer audit and governance questions (who accessed PII columns, which tables are unused, where did this table's data come from) from Snowflake's own logs. Enterprise edition+.

## Structure
`snowflake.account_usage.access_history`: one row per query with JSON arrays:
- `direct_objects_accessed`: objects named in the query (e.g. a view).
- `base_objects_accessed`: underlying tables/columns actually read (resolves views).
- `objects_modified`: targets written, with column-level source mapping (lineage).
- `policies_referenced`: masking/row access policies applied.
Latency up to ~3 hours; 365 days retention.

## Who read a PII column (last 30 days)
```sql
select ah.query_start_time, ah.user_name, obj.value:"objectName"::string as table_name,
       col.value:"columnName"::string as column_name, ah.query_id
from snowflake.account_usage.access_history ah,
     lateral flatten(ah.base_objects_accessed) obj,
     lateral flatten(obj.value:"columns") col
where ah.query_start_time >= dateadd(day, -30, current_timestamp())
  and obj.value:"objectName"::string = 'ANALYTICS.CRM.DIM_CUSTOMERS'
  and col.value:"columnName"::string in ('EMAIL', 'PHONE')
order by 1 desc;
```

## Unused tables
Candidates are tables whose names never appear in `base_objects_accessed` over a chosen window (for example 90 days). Flatten `base_objects_accessed` as above and compare the object names with your table inventory; confirm with owners before archiving or dropping.

## Write lineage
`objects_modified[*].columns[*].directSources` / `baseSources` show which source columns fed each written column: column-level lineage for INSERT/MERGE/CTAS.

## Practice
- Materialise daily flattened extracts into an audit schema for fast reporting.
- Combine with `login_history` and `query_history` for full investigations.

## Verify
- [ ] PII access report runs and lists only expected roles/users.
- [ ] Unused-table report reviewed quarterly.

## Checked
2026-10-28. Confirmed against the ACCESS_HISTORY view page and the Access History guide (Enterprise Edition or higher, 365 days, latency up to 180 minutes, direct_objects_accessed, base_objects_accessed, objects_modified, policies_referenced, objectName and columnName fields, directSources and baseSources). Removed: the tag_references join and the unused-table query, which used ACCOUNT_USAGE.TABLES columns not checked in this batch.
Method: documentation only; no commands were run.
