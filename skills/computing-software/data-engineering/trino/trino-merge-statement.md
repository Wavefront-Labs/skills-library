---
id: computing-software.data-engineering.trino.trino-merge-statement
name: trino-merge-statement
category: computing-software
field: data-engineering
product: trino
tags: [merge, merge-into, when-matched, when-not-matched, upsert]
level: practitioner
status: docs-checked
description: "Write Trino MERGE INTO statements: WHEN clause ordering, DELETE, UPDATE and INSERT branches, the single-match rule and connector support limits."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/sql/merge.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino merge statement

Syntax: `MERGE INTO target_table [ @ branch_name ] [ [ AS ] alias ] USING { source_table | query } [ [ AS ] source_alias ] ON search_condition when_clause [...]`. A `when_clause` is one of:

```text
WHEN MATCHED [ AND condition ] THEN DELETE
WHEN MATCHED [ AND condition ] THEN UPDATE SET ( column = expression [, ...] )
WHEN NOT MATCHED [ AND condition ] THEN INSERT [ column_list ] VALUES (expression, ...)
```

Rules from the docs:
- Any number of `WHEN` clauses is allowed. For each source row they are processed in order and only the first matching clause runs.
- The query fails if a single target row matches more than one source row, so make sure the `ON` condition is unique on the source side (aggregate or deduplicate the source first).
- `UPDATE` expressions can use any field of target or source; `INSERT` expressions can use only source fields.

Upsert example: increment purchases on a match, insert otherwise.

```sql
MERGE INTO accounts t USING monthly_accounts_update s
    ON (t.customer = s.customer)
    WHEN MATCHED
        THEN UPDATE SET purchases = s.purchases + t.purchases
    WHEN NOT MATCHED
        THEN INSERT (customer, purchases, address)
              VALUES(s.customer, s.purchases, s.address)
```

Put the narrower conditional clause first, for example `WHEN MATCHED AND s.address = 'Centreville' THEN DELETE` before the general `WHEN MATCHED THEN UPDATE`. The target may name a branch with `@ audit`.

Limitations: any connector can be the source, but only connectors that support `MERGE` can be the target; check the connector documentation.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. All claims match the page; unchanged.
