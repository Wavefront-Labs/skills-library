---
id: computing-software.database-administration.sql.sql-views-and-materialized-views
name: sql-views-and-materialized-views
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-views, materialized-views, updatable-views, security-barrier]
level: practitioner
status: docs-checked
description: "Create PostgreSQL views and materialised views, and know refresh, updatability and permission behaviour."
sources: ["https://www.postgresql.org/docs/current/sql-createview.html", "https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html", "https://www.postgresql.org/docs/current/rules-materializedviews.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Views

PostgreSQL behaviour, from the PostgreSQL documentation. Other engines differ; check their own docs.

- A view is not physically materialised: the query is run every time the view is referenced. Good for stable
  interfaces, hiding joins and exposing a subset of columns.
- Automatically updatable views: exactly one entry in `FROM` (a table or another updatable view); no `WITH`,
  `DISTINCT`, `GROUP BY`, `HAVING`, `LIMIT`, `OFFSET`, set operations, aggregates, window functions or set-returning
  functions in the select list. Computed columns are read-only; plain columns stay updatable.
- Without `CHECK OPTION`, an `INSERT`, `UPDATE` or `MERGE` through a view can create rows not visible through the
  view. `WITH [CASCADED | LOCAL] CHECK OPTION` rejects them; with neither keyword, `CASCADED` is assumed. It only
  works on automatically updatable views and cannot be used with `RECURSIVE` views.
- A more complex view is read-only by default. Add `INSTEAD OF` triggers to make it writable (rules are another
  option, but the docs say triggers are easier to understand and use correctly).
- Materialised views persist results in a table-like form and cannot be updated directly. Refresh with
  `REFRESH MATERIALIZED VIEW [CONCURRENTLY] name [WITH [NO] DATA]`. The data is not always current, so schedule the
  refresh (the docs' example runs it nightly).
- `CONCURRENTLY` avoids locking out concurrent selects but requires at least one `UNIQUE` index that uses only column
  names and covers all rows (no expression index, no `WHERE`), a populated view, and it cannot be combined with
  `WITH NO DATA`. Only one `REFRESH` at a time can run on a given materialised view. Without it, a refresh touching
  many rows is typically cheaper but can block readers. You need the `MAINTAIN` privilege to refresh.
- `REFRESH` does not guarantee to preserve the `ORDER BY` of the defining query.
- Permissions: by default the view owner's permissions decide access to the underlying tables, which gives restricted
  but secure access. With `security_invoker = true` the invoking user's permissions are checked instead (and row-level
  security policies of the invoker apply). `security_barrier = true` is for views meant to provide row-level security:
  the view's own `WHERE` conditions are evaluated before conditions added by the view's user.
- A `SELECT *` view keeps the columns the table had at creation; columns added later are not part of the view.
- Give every view column an explicit name and type (`SELECT text 'Hello' AS hello`), otherwise the name is
  `?column?` and the type defaults to `text`.

## Checked
2026-11-08. Confirmed in the PostgreSQL CREATE VIEW page (not materialised, updatable-view conditions, CHECK OPTION
rules, INSTEAD OF triggers, security_invoker, security_barrier, SELECT * example, column naming note), REFRESH
MATERIALIZED VIEW page (CONCURRENTLY conditions, MAINTAIN, ORDER BY note) and Rule System section 39.3 (materialised
views cannot be updated directly, data not always current). Removed: the claims that the planner flattens views
together with the outer query or stacked views, Oracle fast refresh, SQL Server indexed views, MySQL having no
materialised views, INSTEAD OF support in other engines, and the PostgreSQL 15 version tag for `security_invoker`,
none of which these pages state.
Method: documentation only; no commands were run.
