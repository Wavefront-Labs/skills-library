---
id: computing-software.web-development.vapor.vapor-fluent-mongodb-sql-specifics
name: vapor-fluent-mongodb-sql-specifics
category: computing-software
field: web-development
product: vapor
tags: [vapor, fluent, fluent-mongodb, sqldatabase, fluentsql, mongodb, raw-sql, custom-query]
level: advanced
status: docs-checked
description: "Reach database-specific features from Vapor Fluent: cast to SQLDatabase for raw SQL, use .custom cases, and model MongoDB with ObjectId, Document and regex queries."
sources:
  - https://docs.vapor.codes/fluent/advanced/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use driver-specific features Fluent does not abstract.

## SQL
Any Fluent `Database` (`req.db`, `app.db`, the `database` in a migration) can be cast to `SQLDatabase` (import `FluentSQL`); the cast only succeeds on SQL drivers.
```swift
if let sql = req.db as? SQLDatabase {
    let planets = try await sql.raw("SELECT * FROM planets").all(decoding: Planet.self)
}
```
Specific drivers: import the driver and cast, e.g. `import FluentPostgresDriver` then `req.db as? PostgresDatabase` (`postgres.simpleQuery("SELECT * FROM planets").all()`). Listed: `PostgresDatabase` (fluent-postgres-driver / postgres-nio), `MySQLDatabase` (fluent-mysql-driver / mysql-nio), `SQLiteDatabase` (fluent-sqlite-driver / sqlite-nio).

### `.custom`
Most query and schema types have a `.custom` case:
```swift
let query = Planet.query(on: req.db)
if req.db is PostgresDatabase {
    query.filter(\.$name, .custom("ILIKE"), "earth")
} else {
    query.group(.or) { or in
        or.filter(\.$name == "earth").filter(\.$name == "Earth")
    }
}
```
SQL accepts `String` or `SQLExpression`; FluentSQL adds `.sql(raw:)`, e.g. `query.filter(.sql(raw: "LOWER(name) = 'earth'"))` or in schema `builder.field("name", .sql(raw: "VARCHAR(64)"), .required)` for MySQL.

## MongoDB
Fluent MongoDB uses the MongoKitten driver.
- Id: `@ID(custom: .id) var id: ObjectId?`. If models are shared with SQL, use `UUID` instead.
- Modelling: use nested structures and arrays of related identifiers rather than join tables.
- Flexible data: `@Field(key: "document") var document: Document` (not valid on SQL). Query with a dot-notated key: `Something.query(on: db).filter("document.key", .equal, 5).first()`.
- Regex via `.custom` with a `Document`:
```swift
import FluentMongoDriver
var queryDocument = Document()
queryDocument["name"]["$regex"] = "e"
queryDocument["name"]["$options"] = "i"
let planets = try Planet.query(on: req.db).filter(.custom(queryDocument)).all()
```
- Raw access: `guard let db = req.db as? MongoDatabaseRepresentable else { throw Abort(.internalServerError) }; let mongodb = db.raw` for MongoKitten APIs.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) fluent/advanced, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
