---
id: computing-software.web-development.vapor.vapor-fluent-setup-drivers
name: vapor-fluent-setup-drivers
category: computing-software
field: web-development
product: vapor
tags: [vapor, fluent, fluent-drivers, orm, postgres, sqlite, mysql, mongodb]
level: intro
status: docs-checked
description: "Add Fluent and a database driver to a Vapor project, configure Postgres, SQLite, MySQL or MongoDB, then a first model, migration and queries."
sources:
  - https://docs.vapor.codes/fluent/overview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get Fluent (the ORM) connected to a database and run a first model, migration and query.

## Add dependencies
`vapor new` can include Fluent and a driver if you answer yes. For an existing project add `vapor/fluent` (from 4.0.0) plus a driver:

```swift
.package(url: "https://github.com/vapor/fluent.git", from: "4.0.0"),
.package(url: "https://github.com/vapor/fluent-<db>-driver.git", from: <version>),
// target:
.product(name: "Fluent", package: "fluent"),
.product(name: "Fluent<db>Driver", package: "fluent-<db>-driver"),
```

Then in `configure.swift`: `app.databases.use(<db config>, as: <identifier>)`.

## Drivers
- PostgreSQL (the recommended driver; package `fluent-postgres-driver` from 2.0.0):
```swift
app.databases.use(.postgres(configuration: .init(
    hostname: "localhost", username: "vapor", password: "vapor",
    database: "vapor", tls: .disable)), as: .psql)
// or: try app.databases.use(.postgres(url: "<connection string>"), as: .psql)
```
- SQLite (`fluent-sqlite-driver` 4.0.0): `app.databases.use(.sqlite(.file("db.sqlite")), as: .sqlite)` or `.sqlite(.memory)`. In-memory can lose data (use for testing); with it, migrate via `--auto-migrate` or `try await app.autoMigrate()` after adding migrations.
- MySQL (`fluent-mysql-driver` 4.0.0, also supports MariaDB): `.mysql(hostname:username:password:database:)` as `.mysql`, or `.mysql(url:)`. For a local no-SSL connection (e.g. MySQL 8 in Docker) pass a `TLSConfiguration.makeClientConfiguration()` with `certificateVerification = .none` as `tlsConfiguration:`. Do not disable verification in production.
- MongoDB (`fluent-mongo-driver` 1.0.0, MongoKitten-based): `try app.databases.use(.mongo(connectionString: "<connection string>"), as: .mongo)`.

## First model, migration, query
```swift
final class Galaxy: Model, Content {
    static let schema = "galaxies"
    @ID(key: .id) var id: UUID?
    @Field(key: "name") var name: String
    init() { }
    init(id: UUID? = nil, name: String) { self.id = id; self.name = name }
}

struct CreateGalaxy: AsyncMigration {
    func prepare(on database: Database) async throws {
        try await database.schema("galaxies").id().field("name", .string).create()
    }
    func revert(on database: Database) async throws {
        try await database.schema("galaxies").delete()
    }
}
```
Register with `app.migrations.add(CreateGalaxy())`, then run `swift run App migrate` (or add `migrate` as an argument in the Xcode scheme); it prompts y/n. Routes:

```swift
app.get("galaxies") { req async throws in try await Galaxy.query(on: req.db).all() }
app.post("galaxies") { req async throws -> Galaxy in
    let galaxy = try req.content.decode(Galaxy.self)
    try await galaxy.create(on: req.db)
    return galaxy
}
```

## Relation preview
A `Star` model with `@Parent(key: "galaxy_id") var galaxy: Galaxy` is set in init via `self.$galaxy.id = galaxyID`. Its migration uses `.field("galaxy_id", .uuid, .references("galaxies", "id"))`; add `CreateStar` after `CreateGalaxy` because migrations run in order. On `Galaxy`, `@Children(for: \.$galaxy) var stars: [Star]` plus `.with(\.$stars)` on the query returns stars inline.

## Log generated SQL
Drivers log SQL at debug level: `app.logger.logLevel = .debug`.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) fluent/overview, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
