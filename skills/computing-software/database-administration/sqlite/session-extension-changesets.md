---
id: computing-software.database-administration.sqlite.session-extension-changesets
name: session-extension-changesets
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, session-extension, changeset, patchset, sqlite-sync, sqlite-backup]
level: practitioner
status: verified
description: "Record changes to SQLite tables with the session extension, apply changesets or patchsets to other databases with conflict handlers, for sync and audit."
sources:
  - https://sqlite.org/sessionintro.html
  - https://sqlite.org/session/intro.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Session extension changesets

**Goal:** capture inserts/updates/deletes made on one database and replay them elsewhere (offline-first sync, audit, undo), without diffing whole files.

## Concepts
- A **session** attaches to a connection and records changes to chosen tables (must have PRIMARY KEYs).
- A **changeset** contains old and new values (supports conflict detection and inversion/undo); a **patchset** is smaller, with new values and PKs only.
- Build requires `SQLITE_ENABLE_SESSION` and `SQLITE_ENABLE_PREUPDATE_HOOK` (sessionintro.html). The 3.54.1 sqlite.org shell lists both and has `.session`; the Python 3.14 module (SQLite 3.50.4) lists neither.

## C API flow
(The Python 3.50.4 module has no session support, so this flow was exercised through APSW 3.54.1.0, which wraps the same C calls: create, attach, changeset, apply with a conflict callback, invert.)
```c
sqlite3session *s;
sqlite3session_create(db, "main", &s);
sqlite3session_attach(s, NULL);                 /* NULL = all tables */
/* ... application makes changes ... */
int n; void *buf;
sqlite3session_changeset(s, &n, &buf);           /* serialise */
sqlite3session_delete(s);

/* on the other database */
sqlite3changeset_apply(db2, n, buf, NULL, conflict_cb, NULL);
```
Conflict handler returns `SQLITE_CHANGESET_OMIT`, `REPLACE` or `ABORT` for conflict types `DATA` (row differs), `NOTFOUND`, `CONFLICT` (PK exists on insert), `CONSTRAINT`, `FOREIGN_KEY`.

## Shell
```text
.session open main s1
.session s1 attach orders
-- make changes
.session s1 changeset orders.changeset
.session s1 patchset orders.patchset
.session s1 close
```
Run on 3.54.1: one INSERT and one UPDATE on `orders` gave a 43-byte changeset and a 39-byte patchset; `.session` also has `enable`, `filter`, `indirect`, `isempty` and `list`. The shell writes the files but has no apply command, so apply from code.

## Other operations
- `sqlite3changeset_invert` produces an undo changeset.
- `sqlite3changeset_concat` / changegroup merges many changesets.
- `sqldiff --changeset` creates one from two database files.
- Language bindings: Python's standard `sqlite3` module lacks session support (`hasattr(sqlite3.Connection, 'session')` was False); APSW 3.54.1.0 has `apsw.Session`, `apsw.Changeset.apply/invert/iter` and `apsw.ChangesetBuilder`. In a test, applying the changeset to a copy where `orders.v` had been edited called the conflict handler with reason `SQLITE_CHANGESET_DATA` (1), and returning `SQLITE_CHANGESET_OMIT` (0) left the edited row alone while the INSERT applied.
- Constants (APSW values): `DATA` 1, `NOTFOUND` 2, `CONFLICT` 3, `CONSTRAINT` 4, `FOREIGN_KEY` 5; handler returns `OMIT` 0, `REPLACE` 1, `ABORT` 2.

## Gotchas
- Tables without primary keys are ignored (an attached `nopk` table with one insert produced no entry in the changeset); rows with a NULL in a PRIMARY KEY column are ignored (sessionintro.html).
- Changes are recorded only while the session is attached on that connection; other connections' writes are not captured.
- Schema must match on the target (same tables and PK columns).

## Verify
Apply a changeset to a copy of the origin's previous state and `sqldiff` it against the origin: no differences.
