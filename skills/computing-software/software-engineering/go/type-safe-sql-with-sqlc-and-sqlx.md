---
id: computing-software.software-engineering.go.type-safe-sql-with-sqlc-and-sqlx
name: type-safe-sql-with-sqlc-and-sqlx
category: computing-software
field: software-engineering
product: go
tags: [go, golang, sqlc-queries, sqlc, sqlx, pgx, database, code-generation, postgresql]
level: practitioner
status: gated
description: "Write SQL-first Go data access: generate typed query code with sqlc, or scan into structs with sqlx; config, transactions, nullable types and CI checks."
sources: ["https://docs.sqlc.dev/en/stable/", "https://docs.sqlc.dev/en/stable/reference/config.html", "https://jmoiron.github.io/sqlx/", "https://pkg.go.dev/github.com/jmoiron/sqlx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type-safe SQL with sqlc and sqlx

**Goal:** keep real SQL (reviewable, tunable) while removing hand-written `rows.Scan` boilerplate
and catching column/type mismatches at build time.

## sqlc: compile SQL into Go
sqlc.yaml:
```yaml
version: "2"
sql:
  - engine: postgresql        # postgresql, mysql or sqlite
    schema: db/migrations      # same files your migration tool applies
    queries: db/queries
    gen:
      go:
        package: store
        out: internal/store
        sql_package: pgx/v5         # pgx/v4, pgx/v5 or database/sql (default)
        emit_json_tags: true
        emit_interface: true   # outputs a Querier interface (default false), handy for fakes
```
db/queries/users.sql:
```sql
-- name: GetUser :one
SELECT id, email, created_at FROM users WHERE id = $1;

-- name: ListUsers :many
SELECT id, email, created_at FROM users ORDER BY id LIMIT $1 OFFSET $2;

-- name: CreateUser :one
INSERT INTO users (email) VALUES (@email) RETURNING *;
```
```bash
sqlc generate       # builds Go code from your SQL (generated file names: see a generated project) (gated: unconfirmed, source is paywalled or blocked)
sqlc vet            # "examines queries" using your vet rules
sqlc diff           # compares the generated files to the existing files, for CI
```
Usage: `q := store.New(pool); u, err := q.GetUser(ctx, id)`.
Annotations: `:one`, `:many`, `:exec`, `:execrows`, `:execresult`, `:execlastid`, `:copyfrom` (driver-specific), and `:batchexec`/`:batchmany`/`:batchone`, which require PostgreSQL with pgx and Go output.
Named params: `sqlc.arg(name)` (the `@name` shorthand is not on the macros page) (gated: unconfirmed, source is paywalled or blocked); `sqlc.narg(name)` is the same but always nullable; `sqlc.slice(ids)` generates a dynamic query for drivers that cannot pass slices to IN (cannot be used with prepared statements). On Postgres use `= ANY($1::bigint[])` (standard Postgres; not on the sqlc page).

Transactions:
```go
tx, err := pool.Begin(ctx)
defer tx.Rollback(ctx)           // no-op after Commit
qtx := q.WithTx(tx)
...
return tx.Commit(ctx)
```
Nullable columns map to driver null types such as `pgtype.Text` or `sql.NullString` (exact types: gated: unconfirmed, source is paywalled or blocked); the `overrides` config under `gen.go` changes sqlc's default Go type choices. Dynamic queries (optional filters, sort columns) are sqlc's weak spot: use
`(sqlc.narg(x)::text IS NULL OR col = sqlc.narg(x))` patterns, or drop to sqlx/squirrel for those.

## sqlx: lighter, runtime mapping
```go
db := sqlx.MustConnect("pgx", dsn)   // driver name must match a registered database/sql driver
type User struct {
    ID    int64  `db:"id"`
    Email string `db:"email"`
}
var u User
err := db.GetContext(ctx, &u, "SELECT id, email FROM users WHERE id = $1", id)
var us []User
err = db.SelectContext(ctx, &us, "SELECT id, email FROM users LIMIT $1", 50)
query, args, _ := sqlx.In("SELECT * FROM users WHERE id IN (?)", ids)
query = db.Rebind(query)                       // ? -> $1 for postgres
_, err = db.NamedExecContext(ctx, "INSERT INTO users (email) VALUES (:email)", u)
```
Errors appear at runtime (missing destination column), so cover queries with integration tests.

## Choosing
sqlc for stable query sets with strong typing and a schema in migrations; sqlx for dynamic SQL or
when generating code is unwanted. Both beat an ORM when the team writes SQL well; both still use
`database/sql` or pgx pools, so pool tuning and context timeouts still apply.

## Verify
- [ ] `sqlc generate && git diff --exit-code` (or `sqlc diff`) in CI.
- [ ] Integration tests run queries against a real database (testcontainers).
- [ ] No `SELECT *` in sqlc queries whose result structs are part of a public API.

## Checked

2026-11-02. Checked against the sqlc documentation (config, query annotations, macros, CLI reference; the stable URLs now redirect to versioned pages) and the sqlx package page. Confirmed: version 2 config keys, engines postgresql/mysql/sqlite, `sql_package` values, `emit_json_tags`, `emit_interface`, annotations incl. `:execlastid` and the Postgres-only batch commands, `sqlc.narg`, `sqlc.slice` semantics, CLI commands `generate`, `vet`, `diff`; sqlx `MustConnect`, `GetContext`, `SelectContext`, `NamedExecContext`, `In`, `Rebind` signatures. Fixed: batch annotations listed as general, `sqlc.slice` scope. Gated: `@name` shorthand, generated file names, null type mapping, which the fetched pages do not state.

Method: documentation only; no commands were run.
