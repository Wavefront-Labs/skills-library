---
id: computing-software.web-development.vapor.vapor-fluent-enum-group-dto
name: vapor-fluent-enum-group-dto
category: computing-software
field: web-development
product: vapor
tags: [vapor, fluent, fluent-model, enum, group, dto, codable, database-space]
level: advanced
status: docs-checked
description: "Fluent @Enum, @Group, Codable models versus DTOs (PATCH and response shaping), and model database space."
sources:
  - https://docs.vapor.codes/fluent/model/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: pick the right Fluent property type for enums and nested data, and keep your API decoupled from your models.

## @Enum
Stores a `String`-backed `RawRepresentable` type as a native database enum (type safety, possibly faster than raw).

```swift
enum Animal: String, Codable { case dog, cat }
final class Pet: Model {
    @Enum(key: "type") var type: Animal
}
```
Use `@OptionalEnum` for optionals. The database must be prepared via a migration (see the schema enum builder). Any enum backed by a Codable type (String, Int) can instead go in a plain `@Field`, stored as its raw value.

## @Group
A nested set of fields that stays queryable, stored flat with keys joined by `_`. Define the nested type with `Fields` (like a Model with no id or schema; may hold `@Field`, `@Enum`, another `@Group`):

```swift
final class Pet: Fields {
    @Field(key: "name") var name: String
    @Field(key: "type") var type: String
    init() { }
}
final class User: Model {
    @Group(key: "pet") var pet: Pet
}
User.query(on: database).filter(\.$pet.$name == "Zizek").all()
```
Access with dot syntax (`user.pet.name`). Columns appear as `pet_name`, `pet_type`. Contrast: a Codable struct in `@Field` is not freely filterable.

## Codable and DTOs
Models are `Codable`; add `extension Planet: Content { }` to return them from routes. Serialization uses property names (not keys), relations become nested structures, and eager-loaded data is included. The docs recommend DTOs for almost all API input and output: models expose database details (e.g. a password hash), and DTOs let schema and API change independently.

PATCH with a DTO (decoding the Model would fail on missing fields):

```swift
struct PatchUser: Decodable { var firstName: String?; var lastName: String? }
app.patch("users", ":id") { req async throws -> User in
    let patch = try req.content.decode(PatchUser.self)
    guard let user = try await User.find(req.parameters.get("id"), on: req.db) else { throw Abort(.notFound) }
    if let firstName = patch.firstName { user.firstName = firstName }
    if let lastName = patch.lastName { user.lastName = lastName }
    try await user.save(on: req.db)
    return user
}
```
Response shaping: a `GetUser: Content` struct with `id` and a computed `name` built from `firstName` and `lastName`, mapped from fetched users using `try user.requireID()`. DTOs can live in a shared package, with `Content` conformance added in the Vapor app.

## Database space
`public static let space: String? = "mirror_universe"` next to `schema` places a model in a PostgreSQL schema, MySQL database, or attached SQLite database; Fluent uses it for all queries. MongoDB does not support spaces.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) fluent/model, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
