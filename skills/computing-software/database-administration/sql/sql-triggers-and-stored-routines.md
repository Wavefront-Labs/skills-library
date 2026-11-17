---
id: computing-software.database-administration.sql.sql-triggers-and-stored-routines
name: sql-triggers-and-stored-routines
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-triggers, stored-procedures, user-defined-functions, plpgsql]
level: advanced
status: docs-checked
description: "Decide when to use PostgreSQL triggers, functions and procedures and write them safely: timing, volatility, SECURITY DEFINER, dynamic SQL."
sources: ["https://www.postgresql.org/docs/current/sql-createtrigger.html", "https://www.postgresql.org/docs/current/sql-createfunction.html", "https://www.postgresql.org/docs/current/sql-createprocedure.html", "https://www.postgresql.org/docs/current/xfunc-volatility.html", "https://www.postgresql.org/docs/current/plpgsql-statements.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Triggers and stored routines

PostgreSQL behaviour, from the PostgreSQL documentation; other engines differ.

- Timing: a trigger fires `BEFORE`, `AFTER` or `INSTEAD OF` the event. Fired before or instead of the event, it can
  skip the operation for the current row or change the row being inserted or updated; fired after, all changes,
  including other triggers' effects, are visible to it. `INSTEAD OF` triggers exist only on views and must be
  `FOR EACH ROW`; `BEFORE` and `AFTER` triggers on a view must be `FOR EACH STATEMENT`.
- Row-level (`FOR EACH ROW`) fires once per modified row; statement-level fires once per statement, even when zero
  rows are modified. Several triggers of the same kind on one event fire in alphabetical order by name.
- Transition tables: `REFERENCING OLD TABLE / NEW TABLE AS name` gives an `AFTER` trigger on a plain table the
  statement's whole before and after row sets. It cannot be combined with a column list on an `UPDATE` trigger.
- `SELECT` triggers do not exist; the docs point to rules and views for such needs.
- `WHEN (condition)` limits when a trigger fires; `INSTEAD OF` triggers do not support it.
- Practice: use triggers for `updated_at`, audit rows and invariants a constraint cannot express. Avoid hidden
  business logic and long trigger chains, and keep slow external calls out of the transaction (judgement, not from the docs).
- Functions versus procedures: invoke a procedure with `CALL`; the `CREATE PROCEDURE` page says procedures can use
  transaction control statements such as `COMMIT` and `ROLLBACK`, depending on the language.
- Volatility is a promise to the optimizer: `VOLATILE` (the default), `STABLE` or `IMMUTABLE`. Only `STABLE` and
  `IMMUTABLE` functions can be used in an index scan condition. Labelling a function `IMMUTABLE` when it is not can
  get it folded to a constant at planning time and a stale value re-used.
- `SECURITY DEFINER` runs a function with its owner's privileges. Set `search_path` on it to exclude schemas writable
  by untrusted users (the docs example sets `admin, pg_temp`). PostgreSQL grants `EXECUTE` to `PUBLIC` on new
  functions by default; revoke that and grant it to only the roles that need it.
- Dynamic SQL in PL/pgSQL uses `EXECUTE command-string [USING ...]`. Pass values with `USING` (preferred to
  inserting values as text, and less prone to SQL injection); build identifiers with `format('%I')` or `quote_ident`.
- Keep routine source in version-controlled migrations. Logic in the database sits close to the data but is harder
  to version and debug; decide per team.

## Checked
2026-11-08. Confirmed in the PostgreSQL CREATE TRIGGER page (timing semantics, row versus statement level, INSTEAD OF
rules, REFERENCING and its limits, alphabetical order, WHEN, no SELECT triggers), CREATE FUNCTION page
(SECURITY DEFINER, search_path advice, PUBLIC execute default), CREATE PROCEDURE page (CALL, transaction control),
the function volatility page and PL/pgSQL statements page (EXECUTE, USING, `%I`, `quote_ident`). Removed: the
"PostgreSQL 11+" tag for procedures, SQL Server `inserted`/`deleted` tables, `%L` as a documented alternative
for values, and the test-framework names (pgTAP, tSQLt), which these pages do not cover. The cited ISO and SQLite
index pages were dropped as sources.
Method: documentation only; no commands were run.
