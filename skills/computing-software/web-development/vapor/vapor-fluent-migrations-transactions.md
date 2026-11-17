---
id: computing-software.web-development.vapor.vapor-fluent-migrations-transactions
name: vapor-fluent-migrations-transactions
category: computing-software
field: web-development
product: vapor
tags: [vapor, fluent, fluent-migration, fluent-transaction, migrations, transactions, asyncmigration, database]
level: practitioner
status: docs-checked
description: "Write, register, run and revert Fluent migrations in Vapor, and wrap several saves in an all-or-nothing transaction with req.db.transaction."
sources:
  - https://docs.vapor.codes/fluent/migration/
  - https://docs.vapor.codes/fluent/transaction/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: evolve a Vapor database with Fluent migrations and group related writes in a transaction.

## Define a migration
A migration has `prepare` (apply the change: schema changes or data changes) and `revert` (undo it, if possible). With async/await conform to `AsyncMigration`:

```swift
struct MyMigration: AsyncMigration {
    func prepare(on database: any Database) async throws { /* make a change */ }
    func revert(on database: any Database) async throws { /* undo it */ }
}
```

The future-based form is `Migration`, with `prepare`/`revert` returning `EventLoopFuture<Void>`.

## Register
```swift
import Fluent
import Vapor

app.migrations.add(MyMigration())
app.migrations.add(MyMigration(), to: .myDatabase) // a specific database
```
Without `to`, the default database is used. List migrations in dependency order: if `MigrationB` depends on `MigrationA`, add A first.

## Run
- `swift run App migrate` checks for newly registered migrations and asks for confirmation before running them (also runnable through Xcode).
- `swift run App migrate --revert` finds the last batch run and asks for confirmation before reverting it.
- `swift run App serve --auto-migrate` migrates before running the command. Programmatically: `try app.autoMigrate().wait()` or `try await app.autoMigrate()`.
- Reverting equivalents: `--auto-revert` and `app.autoRevert()`.

Put schema work inside migrations using the schema builder and query builder.

## Transactions
Nothing is saved until the transaction completes; if you or the database throw at any point, none of the changes take effect. Use the `database` supplied to the closure for every query inside it.

```swift
try await req.db.transaction { transaction in
    try await sun.save(on: transaction)
    try await sirius.save(on: transaction)
}
return .ok
```

Future style: `req.db.transaction { database in sun.save(on: database).flatMap { _ in sirius.save(on: database) } }`, optionally followed by `.transform(to: HTTPStatus.ok)`. The transaction commits when the closure returns successfully.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) fluent/migration, fluent/transaction, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
