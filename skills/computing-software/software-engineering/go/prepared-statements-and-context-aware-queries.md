---
id: computing-software.software-engineering.go.prepared-statements-and-context-aware-queries
name: prepared-statements-and-context-aware-queries
category: computing-software
field: software-engineering
product: go
tags: [go, go-database, go-sql-prepared, prepared-statements, querycontext, database-sql]
level: practitioner
status: docs-checked
description: "Use database/sql prepared statements, QueryContext and rows handling correctly, including Close, Err and connection pinning."
sources:
  - https://pkg.go.dev/database/sql
  - https://go.dev/doc/database/prepared-statements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prepared statements and context-aware queries

**Goal:** parameterised, cancellable queries that never leak connections.

```go
ctx, cancel := context.WithTimeout(ctx, 3*time.Second)
defer cancel()

rows, err := db.QueryContext(ctx, `SELECT id, name FROM users WHERE org_id = $1`, orgID)
if err != nil { return err }
defer rows.Close()                       // releases the connection
for rows.Next() {
    var u User
    if err := rows.Scan(&u.ID, &u.Name); err != nil { return err }
    out = append(out, u)
}
if err := rows.Err(); err != nil { return err } // iteration errors surface here

stmt, err := db.PrepareContext(ctx, `INSERT INTO ev(kind, at) VALUES ($1, $2)`)
defer stmt.Close()
for _, e := range evs { stmt.ExecContext(ctx, e.Kind, e.At) }
```

The `args` of `QueryContext`, `ExecContext` and `QueryRowContext` are for the placeholder parameters in the query; the placeholder syntax depends on the driver (the go.dev example uses `?`; the example above uses `$1`, PostgreSQL style), so check your driver. Pass values as arguments, not by formatting them into the SQL text.

A `Stmt` prepared on a `DB` stays usable for the lifetime of the DB and prepares itself automatically on any new underlying connection. A `Stmt` prepared on a `Tx` or `Conn` is bound to that single connection forever and is unusable once the `Tx` or `Conn` closes. Prepared statements take up server resources: call `stmt.Close()` when finished (the go.dev guide says closing releases resources such as underlying connections; `defer stmt.Close()` suffices for a local variable).
`QueryRowContext` always returns a non-nil `*Row` whose errors are deferred to `Scan`; `Scan` returns `sql.ErrNoRows` when no row is selected, so check `errors.Is(err, sql.ErrNoRows)`.

## Gotchas
- `Rows.Close` is idempotent. When `Next` returns false and there are no more result sets, the rows are closed automatically, and you check `rows.Err()`, which may be called after the close. On an early return, close the rows yourself.
- If the context passed to `BeginTx` is cancelled, the `sql` package rolls the transaction back and `Tx.Commit` returns an error.
- `Conn` returns a single connection, so queries on the same `Conn` run in the same database session.

## Checked
2026-11-09. Confirmed on pkg.go.dev/database/sql (`QueryContext`, `PrepareContext`, `QueryRowContext`, `ErrNoRows`, `Rows.Close`/`Err`, `Stmt` binding rules, `BeginTx` context, `Conn`, `DBStats` fields) and the go.dev prepared statements guide (Stmt creation functions, close advice).
Removed claims not on the pages: the placeholder table by database, the injection-prevention statement, the identifier allow-list, "early return pins a connection and exhausts the pool", the `Tx` holds-a-connection claim and the MySQL `RowsAffected` behaviour.
Method: documentation only; no commands were run.

## Verify
`db.Stats()` (`InUse`, `WaitCount`) shows connections in use returning to baseline after a burst; a test with a cancelled context returns an error promptly.
