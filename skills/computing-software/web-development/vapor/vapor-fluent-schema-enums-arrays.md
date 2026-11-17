---
id: computing-software.web-development.vapor.vapor-fluent-schema-enums-arrays
name: vapor-fluent-schema-enums-arrays
category: computing-software
field: web-development
product: vapor
tags: [vapor, fluent, fluent-schema, enum, dictionary, array, migration, sql]
level: advanced
status: docs-checked
description: "Fluent schema for native enums, dictionary and array columns, plus why schema building is stringly typed and decoupled from models in migrations."
sources:
  - https://docs.vapor.codes/fluent/schema/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: define columns for enum, dictionary and array model fields, and write migrations that survive model changes.

## Dictionary
For nested `Codable` structs or `[String: V]` stored in a `@Field`. SQL drivers store them in JSON columns. Keys must be strings.

```swift
@Field(key: "pet") var pet: Pet            // Pet is Codable
.field("pet", .dictionary, .required)       // heterogeneous: no `of`
.field("numbers", .dictionary(of: .int), .required)  // homogeneous [String: Int]
```

## Array
```swift
@Field(key: "tags") var tags: [String]
.field("tags", .array(of: .string), .required)
```
Swift arrays are homogeneous, so give `of:`. Custom Codable types that write heterogeneous values to an unkeyed container use plain `.array`.

## Native enums
Create (cases), then `read()` to get a data type for fields:

```swift
database.enum("planet_type").case("smallRocky").case("gasGiant").case("dwarf").create()

let planetType = try await database.enum("planet_type").read()
try await database.schema("planets").field("type", planetType, .required).update()

database.enum("planet_type").deleteCase("gasGiant").update()   // cases can be deleted
database.enum("planet_type").delete()
```
Pairs with a model's `@Enum` property for string-backed enums.

## Model coupling
Schema building is intentionally stringly typed with no key paths, because migrations already in production may reference model properties that no longer exist, and old migrations must stay valid. Example: after renaming `name` into `first_name` and `last_name`, a migration adds the two fields with `.update()`, copies data, then deletes `name`:

```swift
try await User.query(on: database)
    .set(["first_name": .sql(embed: "name")])
    .run()
```
The page notes this copy cannot be expressed without custom SQL, and that splitting a name needs database-specific syntax. Its `revert` re-adds `name`, sets it with `.sql(embed: "concat(first_name, ' ', last_name)")`, then deletes the new fields. Keep the original create migration untouched.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) fluent/schema, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
