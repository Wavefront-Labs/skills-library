---
id: computing-software.web-development.bun.sqlite-transactions-wal
name: sqlite-transactions-wal
category: computing-software
field: web-development
product: bun
tags: [sqlite-transactions, wal-mode, sqlite-extensions, sqlite-update-hooks]
level: advanced
status: docs-checked
description: "Use bun:sqlite transactions and savepoints, enable WAL cleanly, load extensions on macOS, register JS functions, and avoid update-hook and async pitfalls."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/sqlite.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
const insert = db.prepare("INSERT INTO cats (name) VALUES ($name)");
const insertCats = db.transaction(cats => {
  for (const cat of cats) insert.run(cat);
  return cats.length;
});
insertCats([{ $name: "Keanu" }]);   // BEGIN; also .deferred / .immediate / .exclusive
```

Commits on return, rolls back on a thrown error (which propagates); nested calls become savepoints. The wrapped function must be synchronous: code after an `await` runs outside the transaction.

WAL:

```ts
db.run("PRAGMA journal_mode = WAL;");
db.run("PRAGMA synchronous = NORMAL;"); // faster; power loss may drop recent commits, not corrupt
// clean up -wal/-shm files everywhere:
import { constants } from "bun:sqlite";
db.fileControl(constants.SQLITE_FCNTL_PERSIST_WAL, 0);
db.run("PRAGMA wal_checkpoint(TRUNCATE);"); db.close();
```
On macOS the `-wal` and `-shm` files persist after close unless you do this.

Extensions and functions:
- macOS system SQLite cannot load extensions: call `Database.setCustomSQLite(path)` to a Homebrew `.dylib` before creating any `Database`, then `db.loadExtension("name")`.
- `db.function(name, fn)` and `db.aggregate(name, {...})`; querying the same `Database` inside them throws `busy executing a query`.

Gotchas: `onInsert/onUpdate/onDelete` hooks fire before commit (rolled-back changes still reported) and cannot query the database.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/sqlite: transaction wrapper, deferred/immediate/exclusive variants, commit on return and rollback on throw with the error propagating, nested savepoints, synchronous-only warning, WAL pragma, synchronous NORMAL note, SQLITE_FCNTL_PERSIST_WAL and TRUNCATE checkpoint cleanup, macOS sidecar persistence, setCustomSQLite before creating a Database, loadExtension, function and aggregate, the busy executing a query error, and update hook rules (fires before commit, cannot query). Nothing removed.
Method: documentation only; no commands were run.
