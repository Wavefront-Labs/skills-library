---
id: computing-software.database-administration.sqlite.in-memory-databases-serialize-deserialize
name: in-memory-databases-serialize-deserialize
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite3-serialize, in-memory-database, sqlite-deserialize, sqlite-backup, memdb]
level: practitioner
status: verified
description: "Use SQLite in-memory databases (:memory:, shared memdb VFS) and sqlite3_serialize/deserialize to snapshot, ship or load whole databases as byte buffers."
sources:
  - https://sqlite.org/inmemorydb.html
  - https://sqlite.org/c3ref/serialize.html
  - https://sqlite.org/c3ref/deserialize.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# In-memory databases and sqlite3_serialize / deserialize

## In-memory databases
```python
con = sqlite3.connect(":memory:")                          # private to this connection
con2 = sqlite3.connect("file:cache1?mode=memory&cache=shared", uri=True)   # shared by connections in-process
con3 = sqlite3.connect("file:/cache1?vfs=memdb", uri=True)  # memdb VFS: shared by name in-process (3.36+), name must start with "/"
```
Checked on 3.50.4: two `:memory:` connections do not see each other's tables, the shared-cache URI and the `/cache2` memdb URI do, but
`file:cache3?vfs=memdb` (no leading slash) was not shared. Data disappears when the last connection closes. Useful for tests, caches, temp processing.

## Serialize: database → bytes
```c
sqlite3_int64 sz;
unsigned char *buf = sqlite3_serialize(db, "main", &sz, 0);   /* copy; free with sqlite3_free */
```
The result is the exact file image (as if written to disk), usable to store in a blob column, send over the network, or write to a file.

## Deserialize: bytes → database
```c
sqlite3_deserialize(db, "main", buf, sz, sz,
    SQLITE_DESERIALIZE_FREEONCLOSE | SQLITE_DESERIALIZE_RESIZEABLE);
```
The connection now operates on the in-memory image. Without `RESIZEABLE` the database cannot grow. Both C calls were run through ctypes against SQLite 3.50.4: with `FREEONCLOSE|RESIZEABLE` an insert of about 2 MB succeeded, with `FREEONCLOSE` alone it failed with `SQLITE_FULL` (13). (The buffer passed to `deserialize` must come from `sqlite3_malloc64` when `FREEONCLOSE` is set.)

## Python 3.11+
```python
data = con.serialize()                      # bytes
mem = sqlite3.connect(":memory:")
mem.deserialize(data)
```

## Shell
```bash
sqlite3 --deserialize app.db     # load the file into memory; changes are not written back
```
Checked on 3.54.1: an INSERT through `--deserialize` was visible in that session while the file still held the old row count.
`.open --deserialize file.db` does the same from inside the shell, and `.save out.db` writes the in-memory database to disk (the saved file had the new row, the original did not).

## Alternatives
- Backup API between `:memory:` and file databases (`con.backup(dest)`) for incremental copying.
- `VACUUM INTO 'file.db'` writes a compacted copy of any database.

## Gotchas
- WAL mode is not used for memory databases (`PRAGMA journal_mode=wal` on `:memory:` returned `memory`). `serialize()` of a file database that is in WAL mode keeps the WAL format flag (header bytes 18 and 19 were 2 and 2), while an image of a `:memory:` database had 1 and 1.
- Deserializing untrusted bytes: treat as untrusted input; `PRAGMA integrity_check` first and use `SQLITE_DBCONFIG_DEFENSIVE`.
- Large images double memory temporarily during serialize (copy) unless `SQLITE_SERIALIZE_NOCOPY` is used (which only avoids the copy when the database is already a contiguous in-memory image).
- `con.backup(dest)` on a connection that still has an uncommitted write in Python 3.14 blocked indefinitely in a test; commit first.
- Python's `deserialize()` image accepted writes that grew the database (to about 5 MB in a test), unlike a C deserialize without `SQLITE_DESERIALIZE_RESIZEABLE`.

## Verify
Round trip: serialize, deserialize into a new connection, compare `SELECT count(*)` and `PRAGMA integrity_check` returns `ok`.
