---
id: computing-software.data-engineering.snowflake.stored-procedures
name: stored-procedures
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-stored-procedures, snowflake-scripting, python-stored-procedure, execute-as-owner, execute-as-caller, exception-handling, dynamic-sql, tasks]
level: advanced
status: docs-checked
description: "Write Snowflake stored procedures in Snowflake Scripting or Python: control flow, exception handling, owner's vs caller's rights, safe dynamic SQL, calling from tasks."
sources:
  - https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-overview
  - https://docs.snowflake.com/en/developer-guide/snowflake-scripting/index
  - https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-rights
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Stored procedures

**Goal:** package multi-statement operational logic (loads with checks, admin automation) inside Snowflake, callable from tasks or clients.

## Snowflake Scripting
```sql
create or replace procedure ops.load_orders(load_date date)
returns varchar
language sql
execute as owner
as
$$
declare
  rows_loaded integer default 0;
  bad_rows exception (-20001, 'too many rejected rows');
begin
  delete from analytics.orders where order_date = :load_date;
  insert into analytics.orders select * from staging.orders where order_date = :load_date;
  rows_loaded := sqlrowcount;
  if (rows_loaded = 0) then
    raise bad_rows;
  end if;
  return 'loaded ' || rows_loaded;
exception
  when other then
    raise;                         -- re-raise so the task/caller sees failure
end;
$$;
call ops.load_orders('2026-10-15');
```
Variables are referenced with `:` inside SQL statements. Snowflake Scripting global variables report the rows affected by DML (see the Scripting docs on determining the number of rows affected).

## Python procedure
```sql
create or replace procedure ops.count_rows(table_name string)
returns string language python runtime_version = '3.12'
packages = ('snowflake-snowpark-python') handler = 'run' execute as caller
as $$
def run(session, table_name):
    n = session.table(table_name).count()
    return f"{table_name}: {n} rows"
$$;
```

## Owner's vs caller's rights
- `execute as owner` (default): runs with the owner role's privileges. Good for controlled elevated actions, with limitations on what an owner's rights procedure can do.
- `execute as caller`: runs with caller privileges and session context.

## Dynamic SQL safety
Use `identifier(:name)` for object names and bind variables (`execute immediate :sql using (v1, v2)`), never string-concatenate untrusted input.

## Operate
Call it from a task's SQL statement (see CREATE TASK) and log progress to a table.

## Verify
- [ ] Failure path surfaces an error to the caller/task history.
- [ ] Procedure grants: only intended roles have USAGE.

## Checked

2026-10-28: reviewed against the official documentation fetched this batch.

Confirmed on the CREATE PROCEDURE, stored procedure overview/rights, Snowflake Scripting (exceptions, variables, DML status), IDENTIFIER and EXECUTE IMMEDIATE pages: owner's rights default and EXECUTE AS CALLER, SQLROWCOUNT, declared exceptions with RAISE, re-raising in a handler, `:` variable binding, IDENTIFIER(:name), EXECUTE IMMEDIATE :sql USING (...), RUNTIME_VERSION 3.12 example.

Removed: explicit transaction statements, ALTER TABLE ... RECLUSTER call, and the task CALL example (not on the pages read). Add transaction handling from the Snowflake transactions docs if atomicity is needed.

Method: documentation only; no commands were run.
