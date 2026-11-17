---
id: computing-software.database-administration.sqlite.migrations-with-pragma-user-version
name: migrations-with-pragma-user-version
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-alter-table, user-version, schema-migration, embedded-database, mobile-app-storage, application-id, migration-runner]
level: practitioner
status: verified
description: "Version an embedded SQLite schema with PRAGMA user_version and a tiny ordered migration runner that applies each step in a transaction on app start."
sources:
  - https://sqlite.org/pragma.html#pragma_user_version
  - https://sqlite.org/pragma.html#pragma_application_id
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema migrations with PRAGMA user_version

**Goal:** every installed copy of an app's SQLite database upgrades itself to the
current schema exactly once, in order, without a migrations table.

## The mechanism
`PRAGMA user_version` is a 32-bit integer stored in the database header
(offset 60), default 0, free for the application to use. Reading and setting it
is cheap and transactional.

## Runner (Python example; same shape in any language)
```python
import sqlite3
MIGRATIONS = [
    # index i upgrades version i -> i+1
    "CREATE TABLE notes(id INTEGER PRIMARY KEY, body TEXT NOT NULL, created_at TEXT NOT NULL);",
    "ALTER TABLE notes ADD COLUMN pinned INTEGER NOT NULL DEFAULT 0;",
    "CREATE INDEX notes_pinned_created ON notes(pinned, created_at);",
]

def migrate(db_path):
    con = sqlite3.connect(db_path, isolation_level=None)   # manage transactions explicitly
    current = con.execute("PRAGMA user_version").fetchone()[0]
    if current > len(MIGRATIONS):
        raise RuntimeError(f"database v{current} is newer than this app (v{len(MIGRATIONS)})")
    for v in range(current, len(MIGRATIONS)):
        con.execute("BEGIN IMMEDIATE")
        try:
            for stmt in filter(None, (s.strip() for s in MIGRATIONS[v].split(";"))):
                con.execute(stmt)
            con.execute(f"PRAGMA user_version = {v + 1}")
            con.execute("COMMIT")
        except Exception:
            con.execute("ROLLBACK")
            raise
    return con
```
Each migration's statements and its version bump commit together, so a crash
mid-migration leaves the database at the previous version. (The naive `split(";")`
is fine for simple DDL; a `CREATE TRIGGER` body contains semicolons and failed with `incomplete input` when split, so use one statement per list entry (no splitting) for those.)
`PRAGMA user_version = N` cannot take a bound parameter (Python: `near "?": syntax error`); format the integer in.
The runner above was run on SQLite 3.50.4: a fresh file ended at version 3 (header bytes 60-63 were `00000003`), a fourth migration with a failing second statement rolled back both the DDL and the version bump, and a database at v3 refused to open with a 2-entry list.

## Rules
- Migrations are append-only: never edit one that has shipped.
- Steps ALTER TABLE cannot do use the 12-step rebuild inside the migration.
- Refuse to open databases with a higher version than the app knows (downgrade protection).
- Set `PRAGMA application_id` once so tools can identify your file format.
- Android's `SQLiteOpenHelper.onUpgrade` uses the same idea: its `getVersion`/`setVersion` run `PRAGMA user_version` (AOSP `SQLiteDatabase.java`). GRDB's `DatabaseMigrator` does not: it records applied migration identifiers in a `grdb_migrations` table.

## Gotchas
- Python's `executescript()` issues a COMMIT first (Python docs, for legacy transaction control; in a test with `isolation_level=None` it also ended an open `BEGIN`: `in_transaction` was False afterwards); that's why the runner executes statements individually.
- Back up (or `VACUUM INTO`) before destructive migrations on user devices.

## Verify
Open an old fixture database with the new app: `PRAGMA user_version` equals the
number of migrations and the schema matches a fresh install (`sqlite3 db .schema` diff).
