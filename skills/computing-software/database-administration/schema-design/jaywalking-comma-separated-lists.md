---
id: computing-software.database-administration.schema-design.jaywalking-comma-separated-lists
name: jaywalking-comma-separated-lists
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, schema-patterns, jaywalking, sql-antipatterns, junction-table, first-normal-form]
level: practitioner
status: verified
description: "Recognise and fix the Jaywalking antipattern (comma-separated ids in one column): the query and integrity problems it causes and a safe migration to a junction table."
sources:
  - https://pragprog.com/titles/bksap1/sql-antipatterns-volume-1/
  - https://www.postgresql.org/docs/current/functions-string.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jaywalking (comma-separated lists)

From Karwin's *SQL Antipatterns*: storing a list of references in one string column, e.g.
`products.account_ids = '12,34,56'`, to avoid an intersection table. It violates first normal
form and causes:

| Problem | Example |
|---|---|
| no index use for lookups | `WHERE account_ids LIKE '%,34,%'` or regex scans every row |
| false matches | `LIKE '%3%'` matches 34 and 13 (checked) |
| no referential integrity | ids of deleted accounts remain; typos accepted |
| awkward joins | `JOIN accounts a ON ',' || p.account_ids || ',' LIKE '%,' || a.id || ',%'` |
| aggregation is hard | counting products per account needs string splitting |
| length limits | `varchar(255)` silently caps the list |
| updates race | two sessions appending to the string overwrite each other |

## Fix: an intersection (junction) table
```sql
CREATE TABLE product_accounts (
  product_id bigint NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  account_id bigint NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  PRIMARY KEY (product_id, account_id)
);
CREATE INDEX ON product_accounts (account_id);
```

## Migration (PostgreSQL example; other engines have split functions)
```sql
INSERT INTO product_accounts (product_id, account_id)
SELECT DISTINCT p.id, trim(x)::bigint
FROM products p
CROSS JOIN LATERAL unnest(string_to_array(p.account_ids, ',')) AS x
WHERE trim(x) ~ '^[0-9]+$'
  AND EXISTS (SELECT 1 FROM accounts a WHERE a.id = trim(x)::bigint)
ON CONFLICT DO NOTHING;
```
Other engines have their own split functions (for example MySQL `JSON_TABLE`, SQL Server `STRING_SPLIT`): check their docs; they were not run here.
Report rows that failed to parse or reference missing accounts before dropping the column.
Use an expand/contract rollout: write both representations, switch reads, then drop the column.

## When a list column is acceptable
Native array or JSON types (PostgreSQL `bigint[]` with a GIN index, JSON arrays) for small,
read-mostly lists where you accept no FK integrity: e.g. tags displayed as-is. Even then, a real
table is better if you filter or join on the elements often.

## Verify
After migration, counts per product match the old list lengths (for valid ids), lookups by
account use the index, and the old column is gone or no longer written.
