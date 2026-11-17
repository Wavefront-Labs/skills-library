---
id: computing-software.database-administration.sql.updatable-views-check-option
name: updatable-views-check-option
category: computing-software
field: database-administration
product: sql
tags: [sql, updatable-views-check-option]
level: advanced
status: docs-checked
description: "Make simple views updatable and stop writes that escape the view filter."
sources: ["https://www.postgresql.org/docs/current/sql-createview.html", "https://www.sqlite.org/lang_createview.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Updatable views and WITH CHECK OPTION

- PostgreSQL views are automatically updatable (INSERT, UPDATE, DELETE, MERGE) when: exactly one FROM entry that is a table or another updatable view; no top-level WITH, DISTINCT, GROUP BY, HAVING, LIMIT or OFFSET; no top-level UNION, INTERSECT or EXCEPT; no aggregates, window functions or set-returning functions in the select list.
- Such a view may mix updatable and read-only columns. A column is updatable only if it is a simple reference to an updatable base column; assigning to a computed column raises an error.
- The view's WHERE condition limits which rows UPDATE and DELETE can reach, but without a check option an UPDATE can move a row out of the view and an INSERT can add a row that the view cannot show.
- `CREATE VIEW v AS SELECT * FROM t WHERE tenant = 7 WITH CHECK OPTION;` rejects INSERT, UPDATE and MERGE that create rows not visible through the view.
- `WITH LOCAL CHECK OPTION` checks only the view's own condition; `CASCADED` also checks the underlying base views, and is assumed if neither word is given. The check option is not allowed on RECURSIVE views and is ignored for views or bases that use INSTEAD OF triggers or INSTEAD rules.
- `WITH (security_barrier = true)` makes all the view's WHERE conditions evaluate before any condition the user adds (for row-level security). `WITH (security_invoker = true)` checks the base relations against the privileges of the querying user instead of the view owner.
- A view that does not meet the conditions is read-only in PostgreSQL unless you add INSTEAD OF triggers. In SQLite views are always read-only; an INSTEAD OF trigger on the view is the way to write through it.
- Self-check: try inserting a row outside the filter, with and without the check option.

## Checked

2026-11-08. Confirmed against the PostgreSQL CREATE VIEW page (updatable view conditions, check option semantics, view options, INSTEAD OF) and the SQLite CREATE VIEW page (read-only views, INSTEAD OF). Removed the "PostgreSQL 15+" gate for security_invoker, which the current page does not state, and corrected the description of security_barrier. The SQLite lang.html root source was replaced by the specific page.

Method: documentation only; no commands were run.
