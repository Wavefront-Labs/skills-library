---
id: computing-software.database-administration.sql.savepoints-and-partial-rollback
name: savepoints-and-partial-rollback
category: computing-software
field: database-administration
product: sql
tags: [sql, savepoints-and-partial-rollback]
level: practitioner
status: docs-checked
description: "Use SAVEPOINT to recover from errors inside a transaction."
sources: ["https://www.postgresql.org/docs/current/sql-savepoint.html", "https://www.postgresql.org/docs/current/sql-rollback-to.html", "https://www.sqlite.org/lang_savepoint.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Savepoints and partial rollback

- `BEGIN; SAVEPOINT s1; ...; ROLLBACK TO SAVEPOINT s1; RELEASE SAVEPOINT s1; COMMIT;`
- PostgreSQL: savepoints exist only inside a transaction block, and several can be defined. `ROLLBACK TO` undoes everything after the savepoint, starts a new subtransaction, keeps that savepoint valid for further rollbacks, and destroys savepoints created after it. `RELEASE` destroys a savepoint but keeps the work done since.
- A transaction that has aborted on an error can be restored with `ROLLBACK TO SAVEPOINT`; any cursor whose execution caused the abort can no longer be used.
- Reusing a name: the older savepoint stays hidden until the newer one is released; rollback and release use the newest.
- Cursors are not fully transactional: a cursor opened inside a rolled-back savepoint is closed, and FETCH motion and CLOSE are not undone.
- SQLite supports the same SAVEPOINT / RELEASE / `ROLLBACK TO` commands. Outside a transaction an outermost SAVEPOINT acts like BEGIN DEFERRED, `ROLLBACK TO` keeps the savepoint on the stack, and releasing the outermost savepoint is the same as COMMIT.
- Self-check: after a forced error, ROLLBACK TO lets the next statement run.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual pages sql-savepoint.html and sql-rollback-to.html and the SQLite lang_savepoint.html page; the draft's driver-mapping and subtransaction-overhead remarks were removed because the pages do not cover them.
