---
id: computing-software.database-administration.sql.update-from-and-delete-using
name: update-from-and-delete-using
category: computing-software
field: database-administration
product: sql
tags: [sql, update-from-and-delete-using]
level: practitioner
status: docs-checked
description: "Update or delete rows based on another table using UPDATE FROM and DELETE USING."
sources: ["https://www.postgresql.org/docs/current/sql-update.html", "https://www.postgresql.org/docs/current/sql-delete.html", "https://www.sqlite.org/lang_update.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UPDATE FROM and DELETE USING joins

- PostgreSQL: `UPDATE t SET v = s.v FROM s WHERE t.id = s.id;` and `DELETE FROM t USING s WHERE t.id = s.id;`. FROM and USING are PostgreSQL extensions to the standard. Do not repeat the target table in FROM unless you want a self-join, and then give it an alias.
- SQLite supports UPDATE FROM since 3.33.0 (2020-08-14), modelled on PostgreSQL. The FROM item can be a subquery, for example an aggregate of a sales table.
- Other engines differ. SQL Server needs the target table named again in FROM (`UPDATE t SET ... FROM t, s WHERE ...`). MySQL puts the join between UPDATE and SET (`UPDATE t JOIN s USING (id) SET ...`) and can update several tables in one statement. Take care when porting.
- Gotcha: if the join gives several rows for one target row, only one of them is used and which one is not predictable (SQLite: arbitrary, may change between runs or releases).
- PostgreSQL notes a sub-select alternative is safer here, though often slower and harder to read: with `SET (a, b) = (SELECT ...)` more than one matching row raises an error and no match sets NULL, whereas the FROM join silently leaves unmatched rows alone.
- PostgreSQL `RETURNING` shows the rows actually updated or deleted. The `UPDATE count` tag counts matched rows even if the values did not change.
- Preview first with the same join as a SELECT; run inside a transaction.
- Self-check: the affected row count equals the preview count.

## Checked

2026-11-08. Confirmed against the PostgreSQL UPDATE and DELETE reference pages (FROM, USING, join cardinality note, sub-select comparison, RETURNING, command tag) and the SQLite UPDATE page (version gate, arbitrary row choice, SQL Server and MySQL forms). Replaced the PostgreSQL docs root and the SQLite lang.html root with specific pages.

Method: documentation only; no commands were run.
