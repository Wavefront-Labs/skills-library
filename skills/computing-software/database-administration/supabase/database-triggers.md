---
id: computing-software.database-administration.supabase.database-triggers
name: database-triggers
category: computing-software
field: database-administration
product: supabase
tags: [triggers, plpgsql, tg-op, trigger-function, cascade]
level: practitioner
status: docs-checked
description: "Create Postgres triggers in Supabase: trigger function plus trigger object, TG_OP, OLD and NEW, row vs statement level, and dropping in restricted schemas."
sources:
  - https://supabase.com/docs/guides/database/postgres/triggers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run a function automatically when rows change.

A trigger has two parts: a trigger function and the trigger object that says when it runs. The page's example function is `language plpgsql`, `returns trigger`, inserts into a log table using `old` and `new`, and ends with `return new;`.

```sql
create trigger "trigger_name"
after insert on "table_name"
for each row
execute function trigger_function();

drop trigger "trigger_name" on "table_name";
```

Timing is `BEFORE` or `AFTER` the event.

Variables available inside the function:
- `TG_OP`: `INSERT`, `UPDATE`, `DELETE` or `TRUNCATE`.
- `OLD`: previous row, in `UPDATE` and `DELETE` triggers.
- `NEW`: new row, in `UPDATE` and `INSERT` triggers.
- `TG_LEVEL`: `ROW` or `STATEMENT`.
- Also `TG_NAME`, `TG_WHEN` (`BEFORE` or `AFTER`), `TG_RELID`, `TG_TABLE_NAME` and `TG_TABLE_SCHEMA`.
- `TG_ARGV` and `TG_NARGS`: string arguments given at creation and their count.

`for each row` runs the function once per affected row; `for each statement` runs it once per operation, which can be more efficient when one statement touches many rows because you can process them as a group.

Restricted schemas: you cannot drop a trigger there because of permission restrictions. Drop the function with `CASCADE`, which removes the triggers that call it:

```sql
drop function if exists restricted_schema.function_name() cascade;
```

Back up the function definition first in case you want to recreate it.

## Checked

2026-11-04: Read the Postgres Triggers guide in full. Confirmed the two-part structure, SQL, variables, row vs statement wording, and restricted-schema drop. Reworded "ends with return new" to describe the page's example only, since the page does not make it a rule.
Method: documentation only; no commands were run.
