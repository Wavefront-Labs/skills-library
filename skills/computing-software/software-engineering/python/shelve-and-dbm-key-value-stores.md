---
id: computing-software.software-engineering.python.shelve-and-dbm-key-value-stores
name: shelve-and-dbm-key-value-stores
category: computing-software
field: software-engineering
product: python
tags: [python, py-serialization, shelve-dbm, shelve, dbm, key-value-store, persistence, dbm-sqlite3]
level: practitioner
status: docs-checked
description: "Persist small key-value data with dbm and shelve: backends, mutation gotchas (writeback), pickle risk, concurrency limits and when to move to sqlite3."
sources: ["https://docs.python.org/3/library/shelve.html", "https://docs.python.org/3/library/dbm.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# shelve and dbm key-value stores

## dbm: bytes keys to bytes values
```python
import dbm
with dbm.open("cache", "c") as db:          # 'r' read, 'w' read-write, 'c' create, 'n' always new
    db[b"user:1"] = b"ada"                   # keys/values are stored as bytes (str is converted with the default encoding)
    db.get(b"user:2", b"default")
    list(db.keys())
dbm.whichdb("cache")                         # which backend wrote this file
```
Backends: `dbm.sqlite3` (new in **3.13**), `dbm.gnu`, `dbm.ndbm`, and `dbm.dumb` (slow but simple, used when none of the others is installed). The `dbm.gnu` and `dbm.ndbm` file formats are incompatible with each other.

## shelve: dict of pickled objects
```python
import shelve
with shelve.open("state") as db:
    db["config"] = {"retries": 3}
    cfg = db["config"]
    cfg["retries"] = 5                       # NOT saved: you mutated a copy
    db["config"] = cfg                       # reassign to persist
with shelve.open("state", writeback=True) as db:   # cache entries, write all back on close/sync
    db.setdefault("list", []).append(1)      # mutation persists, at the cost of memory and slow close
```

## Gotchas
- **Security:** shelve values are pickles; opening a shelf from an untrusted source runs code (see pickle security).
- Keys of `shelve` must be `str`.
- No concurrent read/write support: multiple simultaneous readers are safe, but while a program has a shelf open for writing no other program should open it. Unix file locking can help but differs across systems.
- Which dbm package is used depends on what is available, so do not open the file directly with `dbm`; the underlying dbm limits apply (keep pickled values fairly small).
- On macOS `dbm.ndbm` can silently corrupt the database on updates.
- `sync()` writes back the writeback cache.

## When to leave
Need queries, multiple processes, or schema changes: use `sqlite3` with a two-column table; it is as simple and robust.

## Verify
- [ ] Restart test: write, close, reopen in a new process, read back.
- [ ] A test demonstrates the mutation-without-reassign pitfall so nobody reintroduces it.

## Checked

- 2026-11-03: checked against the CPython docs `library/shelve.rst` and `library/dbm.rst`: `dbm.open` flags and bytes storage, `whichdb`, backend list and `dbm.dumb` fallback, `dbm.sqlite3` new in 3.13, incompatible gnu/ndbm formats, shelve pickle insecurity, `writeback` semantics, string keys, concurrency limits, macOS ndbm warning.
- Removed: multi-file suffix claim, crash corruption claim, class importability note, `flag="r"` advice.

Method: documentation only; no commands were run.
