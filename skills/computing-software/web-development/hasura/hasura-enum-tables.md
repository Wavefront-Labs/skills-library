---
id: computing-software.web-development.hasura.hasura-enum-tables
name: hasura-enum-tables
category: computing-software
field: web-development
product: hasura
tags: [hasura, postgres, enums, schema, reference-table]
level: practitioner
status: docs-checked
description: "Model Postgres enums as single-column reference tables flagged is_enum so Hasura generates GraphQL enum types, instead of native Postgres enums."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/schema/postgres/enums.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restrict a field to a fixed set of values and get GraphQL enums.

Why not native enums: they are hard to change (values cannot be added inside a transaction with ALTER TYPE ADD VALUE, and cannot be removed without dropping the type). The docs say Hasura only generates GraphQL enum types for the referenced-table approach; native Postgres enum columns are treated like text fields.

Steps:
1. Create an enum table: a single-column `text` primary key whose values are valid GraphQL enum value names, optionally one second `text` column used as the value description, no other columns, and at least 1 row. Example: `CREATE TABLE user_role (value text PRIMARY KEY, comment text);` then insert the values.
2. Add foreign keys from columns in other tables to the enum table.
3. Mark the table as an enum. Console: `Data -> [table-name] -> Modify`, toggle `Set table as enum`. Metadata (`tables.yaml`):

```yaml
- table:
    schema: public
    name: user_role
  is_enum: true
```
Or pass `is_enum: true` to `pg_track_table`, or call `pg_set_table_is_enum` for an already tracked table.
4. Apply with `hasura metadata apply`.

Benefit: modifying the enum is just inserting, updating or deleting rows (cascades and transactions work).

Migrations: the insert of the values must come between the migration that creates the table and the migration that sets it as an enum; otherwise applying migrations errors, because an enum table needs at least 1 row.

Gotchas:
- Columns referencing the table use a generated GraphQL enum (for example `user_role_enum`), so filters use the bare value, such as `role: {_eq: administrator}`, not a quoted string.
- Hasura does not detect changes to the contents of an enum table; reload metadata manually after inserting, updating or deleting rows.

## Checked

2026-11-04. Confirmed against the cited pages: enums page: native vs reference-table enums, enum table restrictions, Console/CLI/API setting, foreign-key requirement, GraphQL enum usage, migration ordering, reload-metadata limitation. Removed or corrected: the seed-file suggestion (the page uses migrations) and the Verify step.

Method: documentation only; no commands were run.
