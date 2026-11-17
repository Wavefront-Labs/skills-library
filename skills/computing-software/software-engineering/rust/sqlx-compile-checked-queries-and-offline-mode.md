---
id: computing-software.software-engineering.rust.sqlx-compile-checked-queries-and-offline-mode
name: sqlx-compile-checked-queries-and-offline-mode
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-databases, rust-sqlx, sqlx, compile-time-queries, offline, migrations, postgres]
level: practitioner
status: docs-checked
description: "Use sqlx query macros verified at compile time, the offline .sqlx cache for CI, migrations with sqlx-cli and nullability overrides."
sources:
  - https://docs.rs/sqlx/latest/sqlx/macro.query.html
  - https://raw.githubusercontent.com/launchbadge/sqlx/main/sqlx-cli/README.md
  - https://docs.rs/sqlx/latest/sqlx/struct.Transaction.html
  - https://docs.rs/sqlx/latest/sqlx/struct.QueryBuilder.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# sqlx compile-checked queries and offline mode

**Goal:** typos in SQL and type mismatches fail at compile time.

```bash
cargo install sqlx-cli --no-default-features --features rustls,postgres
export DATABASE_URL=postgres://app:secret@localhost/app_dev
sqlx database create
sqlx migrate add create_users          # creates migrations/<timestamp>_create_users.sql
sqlx migrate run
cargo sqlx prepare --workspace         # writes .sqlx/ query metadata (commit it)
```
```rust
let user = sqlx::query_as!(User, "SELECT id, name, email FROM users WHERE id = $1", id)
    .fetch_one(&pool).await?;            // checked at compile time against the live DB or the .sqlx cache
```

- The `query!` family needs `DATABASE_URL` set at build time, or a `.sqlx` directory at the workspace root.
- `cargo sqlx prepare` saves metadata to `.sqlx` in the current directory (it must be run as `cargo sqlx`); `--workspace` generates a single `.sqlx` at the workspace root. Commit the directory and an active database is no longer needed to build.
- `cargo sqlx prepare --check` exits non-zero if `.sqlx` is out of date with the schema or queries; it is intended for CI.
- A `DATABASE_URL` takes precedence over `.sqlx`. To force offline builds set `SQLX_OFFLINE=true` (this can go in `.env`; `prepare` still connects to the database).
- Queries behind feature flags or in tests need `cargo sqlx prepare -- --all-targets --all-features`.
- Nullability overrides: select `foo as "foo!"` (Postgres/SQLite; backticks on MySQL) to force non-null, or `"foo?"` to force nullable when inference is wrong.
- `sqlx migrate add -r name` creates reversible up/down scripts (all later migrations are then reversible too); `sqlx migrate revert` undoes the last.

## Gotchas
- A forgotten `.sqlx` refresh after changing a query breaks CI builds that run offline.
- A transaction that is neither committed nor rolled back before going out of scope is rolled back on drop.
- Runtime features (for example `runtime-tokio`) must be enabled: without at least one, nearly any async API call panics. If more than one TLS feature is on, `tls-native-tls` takes precedence.
- Dynamic SQL (optional filters) should use `QueryBuilder` with `push_bind`, not string concatenation, to avoid SQL injection.

## Verify
Change a column name in SQL and watch `cargo check` fail; run `cargo sqlx prepare --check` in CI.

## Checked
Method: docs-checked 2026-11-09 against the sqlx-cli README, docs.rs query macro, Transaction and QueryBuilder pages, and the crate root features text. Dropped unconfirmed claims about pool options, the migrate! macro, FromRow and executor syntax.
