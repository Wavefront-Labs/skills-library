---
id: computing-software.software-engineering.go.database-sql-connection-pools-and-transactions
name: database-sql-connection-pools-and-transactions
category: computing-software
field: software-engineering
product: go
tags: [go, go-stdlib, database-sql, connection-pool, transactions, pgx, sql-injection, context, go-database, go-sql-null, go-pgx]
level: practitioner
status: verified
description: "Use Go's database/sql well: pool sizing and lifetimes, contexts on every query, closing rows, transaction helpers with rollback, NULL handling and prepared statements."
sources:
  - https://pkg.go.dev/database/sql
  - https://go.dev/doc/database/manage-connections
  - https://go.dev/doc/database/execute-transactions
  - https://go.dev/doc/database/sql-injection
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# database/sql connection pools and transactions

**Goal:** a database layer that does not exhaust connections, leak them, or leave transactions open.

## 1. Open once, tune the pool
```go
db, err := sql.Open("pgx", dsn)          // lazy: does not connect
if err != nil { return err }
db.SetMaxOpenConns(20)                   // default unlimited: can overwhelm the database
db.SetMaxIdleConns(20)                   // default 2: churn under load
db.SetConnMaxLifetime(30 * time.Minute)  // rotate behind LBs/failovers
db.SetConnMaxIdleTime(5 * time.Minute)
ctx, cancel := context.WithTimeout(ctx, 5*time.Second); defer cancel()
if err := db.PingContext(ctx); err != nil { return fmt.Errorf("db ping: %w", err) }
```
`*sql.DB` is a pool, safe for concurrent use: create one per database for the process lifetime. Size so `instances x MaxOpenConns` stays below the server's `max_connections` (or use PgBouncer). Monitor `db.Stats()` (`WaitCount`, `WaitDuration`, `InUse`).

## 2. Queries with context and parameters
```go
var name string
err := db.QueryRowContext(ctx, `SELECT name FROM customers WHERE id = $1`, id).Scan(&name)
if errors.Is(err, sql.ErrNoRows) { return ErrNotFound }

rows, err := db.QueryContext(ctx, `SELECT id, total FROM orders WHERE customer_id = $1`, cid)
if err != nil { return err }
defer rows.Close()                       // otherwise the connection is never returned
for rows.Next() {
    var o Order
    if err := rows.Scan(&o.ID, &o.Total); err != nil { return err }
    out = append(out, o)
}
return rows.Err()                        // errors during iteration surface here
```
Placeholders: `$1` (Postgres), `?` (MySQL/SQLite). Never build SQL with `fmt.Sprintf` from input; for dynamic identifiers (ORDER BY column) whitelist values.

## 3. Transactions
```go
func withTx(ctx context.Context, db *sql.DB, fn func(*sql.Tx) error) (err error) {
    tx, err := db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
    if err != nil { return err }
    defer func() {
        if p := recover(); p != nil { tx.Rollback(); panic(p) }
        if err != nil { tx.Rollback(); return }
        err = tx.Commit()
    }()
    return fn(tx)
}
```
- Inside a transaction use only `tx.*` methods; calling `db.*` grabs another connection (and can deadlock with a pool of 1).
- `Rollback` after `Commit` is harmless but returns `sql.ErrTxDone` (ignore it); a deferred `tx.Rollback()` right after Begin is the simplest safety net.
- Retry serialization failures (Postgres `40001`) by re-running the whole function.

## 4. NULLs
`sql.NullString`, `sql.NullInt64`, generic `sql.Null[T]` (1.22+), or pointer fields (`*string`). Scanning NULL into a plain `string` errors.

## 5. Driver choice
Postgres: `pgx` (use `pgx/v5/stdlib` for database/sql, or native `pgxpool` for more features and speed). Query helpers: `sqlc` generates type-safe code from SQL; `sqlx` adds struct scanning.

## Gotchas
- Forgetting `rows.Close()` or `rows.Err()`, or returning early in the loop without close, leaks connections until the pool is exhausted (requests hang at `WaitCount` growth).
- A `Stmt` prepared on a `Tx` or `Conn` is bound to that one connection and dies with it; one prepared on the `DB` stays usable and is re-prepared on other connections as needed (`go doc database/sql.Stmt`). Behind a transaction-mode pooler such as PgBouncer, check that pooler's docs for prepared-statement support.

## Verify
- Load test while watching `db.Stats()`: `InUse` stays below `MaxOpenConns`, `WaitCount` does not grow unbounded, and an integration test proves rollback on error (row absent after a failing fn).

## Checked
2026-10-21, Go 1.27.3 + modernc.org/sqlite (pure Go) and pgx v5: `withTx` committed, and rolled back on an error (row count unchanged); pool of 1 with an unclosed `rows` or with a `db.*` call inside an open tx hit `context deadline exceeded` and `WaitCount` rose; scanning NULL into `string` errors, `sql.Null[string]` does not; `sql.Open("pgx", ...)` returns nil and only `PingContext` fails (no server); `Rollback` after `Commit` returns `sql.ErrTxDone`; default MaxIdleConns of 2 and Null[T] from `go doc`; Postgres `40001` = serialization_failure from the Postgres errcodes appendix; `pgxpool` exists. No Postgres server was available: the `$1` placeholder style and `40001` handling rest on the Postgres documentation, and the pool/transaction mechanics were run against SQLite.
