---
id: computing-software.web-development.vapor.vapor-fluent-model-fields-ids
name: vapor-fluent-model-fields-ids
category: computing-software
field: web-development
product: vapor
tags: [vapor, fluent, fluent-model, id, field, uuid, orm, swift]
level: practitioner
status: docs-checked
description: "Define Fluent models: schema name, @ID and custom identifiers, @Field and @OptionalField, empty init, save, create, update, find."
sources:
  - https://docs.vapor.codes/fluent/model/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: write a correct Fluent `Model` and persist and look up instances. Models describe data only; constraints, indexes and foreign keys live in migrations.

## Skeleton
```swift
final class Planet: Model {
    static let schema = "planets"          // table or collection name

    @ID(key: .id) var id: UUID?
    @Field(key: "name") var name: String

    init() { }                              // required
    init(id: UUID? = nil, name: String) { self.id = id; self.name = name }
}
```
`schema` is a static get-only string, typically the class name pluralized and lowercased. The empty `init()` is required (Fluent uses it for query results and reflection); a convenience init that sets everything makes adding properties safer later.

## Identifier
- `@ID(key: .id)` with `UUID` is the supported default: `.id` resolves to `"id"` for SQL and `"_id"` for NoSQL, and UUID is the only identifier type all drivers support. Fluent generates the UUID on create.
- `@ID` is optional; `try planet.requireID()` returns it or throws.
- `planet.$id.exists` is false for a new model, true after save or fetch (mutable).
- Custom: `@ID(custom: "foo") var id: Int?` (fine for SQL auto-increment, not NoSQL). Choose generation with `generatedBy`: `.user` (set before saving), `.random` (type must conform to `RandomGeneratable`), `.database`. If omitted Fluent infers it; `Int` defaults to `.database`.

## Fields
`@Field(key: "name")` needs an explicit database key, which need not match the property name; the docs recommend snake_case keys and camelCase properties. Values can be any `Codable`; nested structs/arrays work but filtering is limited (see `@Group`). Use `@OptionalField(key: "tag") var tag: String?` for optionals.

Warning: a non-optional field with a `willSet` observer that reads its current value, or a `didSet` that reads `oldValue`, causes a fatal error.

## Save, create, update, find
```swift
try await planet.save(on: database)       // create or update depending on exists
try await Planet(name: "Earth").create(on: database)
[earth, mars].create(on: database)        // batch, single query
guard let p = try await Planet.find(req.parameters.get("id"), on: database) else { throw Abort(.notFound) }
p.name = "Earth"
try await p.update(on: database)
let all = try await Planet.query(on: database).all()
```
`find` returns `nil` when not found. Gotcha: after a batch create, models using `@ID(custom:)` with the `.database` generator (usually auto-increment `Int`) do not get their new ids; call `create` on each model instead.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) fluent/model, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
