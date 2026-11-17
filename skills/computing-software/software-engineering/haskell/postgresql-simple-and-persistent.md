---
id: computing-software.software-engineering.haskell.postgresql-simple-and-persistent
name: postgresql-simple-and-persistent
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, postgresql-simple, persistent, esqueleto, hasql, sqlite-simple, connection-pool, resource-pool, migrations, postgresql-simple-and-persistent, haskell-database]
level: practitioner
status: docs-checked
description: "Query PostgreSQL with postgresql-simple: query, execute, FromRow/ToRow, withTransaction, fold, SqlError; pointers to persistent, hasql and resource-pool."
sources: ["https://hackage.haskell.org/package/postgresql-simple/docs/Database-PostgreSQL-Simple.html", "https://hackage.haskell.org/package/postgresql-simple/docs/Database-PostgreSQL-Simple-Transaction.html", "https://hackage.haskell.org/package/postgresql-simple/docs/Database-PostgreSQL-Simple-FromRow.html", "https://hackage.haskell.org/package/persistent-postgresql/docs/Database-Persist-Postgresql.html", "https://hackage.haskell.org/package/resource-pool/docs/Data-Pool.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Databases from Haskell

**Goal:** typed, injection-safe database access.

```haskell
{-# LANGUAGE OverloadedStrings #-}
import Database.PostgreSQL.Simple
import Data.Pool

main = do
  conn <- connectPostgreSQL "host=localhost dbname=app user=app"      -- takes a ByteString connection string
  rows <- query conn "SELECT id, name FROM users WHERE age > ?" (Only (30 :: Int)) :: IO [(Int, String)]
  _ <- execute conn "INSERT INTO users (name, age) VALUES (?, ?)" ("bob" :: String, 41 :: Int)
  withTransaction conn $ do                       -- runs the action in a transaction
    _ <- execute_ conn "UPDATE counters SET n = n + 1"
    pure ()
  close conn
```
`FromRow`/`ToRow` instances map rows and parameter lists (`instance FromRow User where fromRow = User <$> field <*> field`). Also exported: `returning`, `executeMany`, `formatQuery`, `fold`/`forEach`, and `Query` literals via OverloadedStrings.

## Alternatives
- `persistent` with `persistent-postgresql` (`createPostgresqlPool`) and `esqueleto`.
- `hasql` (prepared statements are enabled by default) with `hasql-th` for compile-time syntax checking of SQL, and `hasql-pool`.
- `sqlite-simple` (SQLite), `opaleye`, `selda`.
- Pooling: `resource-pool` provides `Data.Pool` (`newPool`, `withResource`); its API differs between 0.x versions, so read the page for your version.
- Migrations: `postgresql-simple-migration`; `persistent-postgresql` exports `Migration` helpers such as `mockMigration`.

## Gotchas
- Never interpolate into SQL strings; use `?` placeholders. `In` for lists: `WHERE id IN ?` with `Only (In ids)`.
- Catch `SqlError` (it has a `sqlState` field) to react to constraint violations.
- For big results, process rows incrementally with `fold` or `forEach` instead of loading a whole list with `query`.

## Self-check
- [ ] No string concatenation builds SQL.
- [ ] Transactions wrap multi-statement changes.

## Checked
2026-11-03. Confirmed against the Haddock pages for `Database.PostgreSQL.Simple` (`connectPostgreSQL`, `query`, `execute`, `execute_`, `executeMany`, `returning`, `formatQuery`, `fold`, `forEach`, `Only`, `In`, `SqlError`, `sqlState`, `close`), `Transaction` (`withTransaction`), `FromRow` (`fromRow`, `field`), `persistent-postgresql` (`createPostgresqlPool`, `mockMigration`), `Data.Pool` (`newPool`, `withResource`) and the hasql, hasql-th, hasql-pool, esqueleto and other package pages. Removed: rollback-on-exception wording, `runMigration`, hasql binary-protocol claim, mysql-simple and beam, dbmate and sqitch, thread-safety and timeout advice.
Method: documentation only; no commands were run.
