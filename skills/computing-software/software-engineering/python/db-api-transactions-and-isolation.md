---
id: computing-software.software-engineering.python.db-api-transactions-and-isolation
name: db-api-transactions-and-isolation
category: computing-software
field: software-engineering
product: python
tags: [python, py-databases, py-db-dbapi, dbapi-transactions, pep-249, transactions, commit-rollback, parameter-binding, psycopg]
level: practitioner
status: docs-checked
description: "Use Python DB-API 2.0 drivers safely: paramstyle binding, explicit commit and rollback, psycopg 3 and sqlite3 context managers, autocommit modes and nested transaction blocks."
sources: ["https://peps.python.org/pep-0249/", "https://www.psycopg.org/psycopg3/docs/basic/transactions.html", "https://docs.python.org/3/library/sqlite3.html#transaction-control"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DB-API transactions

## Parameter binding (PEP 249)
Parameters are passed as a sequence or mapping to `execute()` and bound by the driver, in a database-specific notation given by the module's `paramstyle`:

| paramstyle | Example |
|---|---|
| `qmark` | `WHERE name=?` |
| `numeric` | `WHERE name=:1` |
| `named` | `WHERE name=:name` |
| `format` | `WHERE name=%s` |
| `pyformat` | `WHERE name=%(name)s` |

Use the driver's placeholder style with a parameter tuple or dict, never string formatting. The module constant `threadsafety` says what may be shared between threads: 0 nothing, 1 the module, 2 module and connections, 3 module, connections and cursors.

## psycopg 3 transactions
- By default any database operation starts a new transaction. Changes are invisible to others until `Connection.commit()` and discarded by `rollback()`. Closing a connection with a transaction open sends no COMMIT.
- After a failed operation the server refuses further commands until `rollback()` is called (`InFailedSqlTransaction`).
- `with psycopg.connect(dsn) as conn:` commits at the end of the block and closes the connection.
- A plain `SELECT` also starts a transaction, so a long-running program can leave the session "idle in transaction" (locks held, table bloat); commit or roll back, or use autocommit.
- Autocommit (`autocommit=True` on `connect()` or `conn.autocommit = True`) suits statements that cannot run in a transaction, such as `CREATE DATABASE` or `VACUUM`; statements are then not atomic as a group.
- `with conn.transaction():` starts a transaction on entry and commits on exit, or rolls back if an exception escapes. On a non-autocommit connection that already has an implicit transaction, the block only manages a savepoint sub-transaction. Blocks can be nested (implemented with `SAVEPOINT`), and raising `Rollback` rolls back a block without failing the program.
- Isolation level, `read_only` and `deferrable` are connection attributes (async connections use `set_isolation_level()` and similar); they can only change when no transaction is active.

```python
import psycopg

with psycopg.connect(dsn) as conn:
    with conn.cursor() as cur:
        cur.execute("UPDATE acct SET bal = bal - %s WHERE id = %s", (amount, src))
        cur.execute("UPDATE acct SET bal = bal + %s WHERE id = %s", (amount, dst))
```

## sqlite3 transactions
- `Connection.commit()` and `rollback()` do nothing if `autocommit` is True or there is no open transaction. The `autocommit` parameter was added in 3.12 and currently defaults to `sqlite3.LEGACY_TRANSACTION_CONTROL` (pre-3.12, non-PEP 249 behaviour governed by `isolation_level`); the default is documented to change to False in a future release. `autocommit=False` is the documented recommended value and keeps a transaction always open.
- `close()` rolls back a pending transaction only when `autocommit` is False; otherwise call `commit()` first.
- Using the connection as a context manager (`with conn:`) commits on success or rolls back on exception; it does not close the connection.
- `check_same_thread=True` (default) raises `ProgrammingError` if another thread uses the connection.
- Tutorial: an INSERT implicitly opens a transaction that needs `commit()` before changes are saved.

## Gotchas
- Keep transactions short; commit or roll back before waiting on user input.
- A pooled connection returned with an open transaction keeps its locks; psycopg docs note middleware such as PgBouncer may discard such connections.

## Verify
- [ ] A test with a failing second statement leaves the first one rolled back.

## Checked
Date: 2026-11-03. Confirmed against PEP 249 (`paramstyle`, `threadsafety`), the psycopg 3 transactions page (default transactions, autocommit, `transaction()` blocks, savepoints, `Rollback`, isolation attributes) and the sqlite3 documentation (autocommit, `LEGACY_TRANSACTION_CONTROL`, context manager, `close`, `check_same_thread`). Removed as unconfirmed: SerializationFailure retry loop and SQLSTATE codes, PostgreSQL default isolation level, `psycopg.sql.Identifier`, `SELECT ... FOR UPDATE`, `psycopg_pool`, `pg_stat_activity` check, named-cursor advice, `asyncpg` placeholder style.
Method: documentation only; no commands were run.
