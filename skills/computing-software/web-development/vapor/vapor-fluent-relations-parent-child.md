---
id: computing-software.web-development.vapor.vapor-fluent-relations-parent-child
name: vapor-fluent-relations-parent-child
category: computing-software
field: web-development
product: vapor
tags: [vapor, fluent, fluent-relations, parent, children, optionalchild, dto, one-to-many]
level: practitioner
status: docs-checked
description: "Model one-to-one and one-to-many relations in Vapor Fluent with @Parent, @OptionalParent, @OptionalChild and @Children, including schema and DTO advice."
sources:
  - https://docs.vapor.codes/fluent/relations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: connect Fluent models as parent / child(ren).

## @Parent
Stores a reference to another model's `@ID`.
```swift
final class Planet: Model {
    @Parent(key: "star_id")
    var star: Star
}
```
Set it through the inner field: `earth.$star.id = sun.id`, e.g. `self.$star.id = starID` in an `init(name:starID:)` with `starID: Star.IDValue`. Matching schema field (Star has a UUID id):
`.field("star_id", .uuid, .required, .references("star", "id"))` (`.references` is optional).

## @OptionalParent
Same but nullable: `@OptionalParent(key: "star_id") var star: Star?`. Schema omits `.required`: `.field("star_id", .uuid, .references("star", "id"))`.

## Encoding parents: use a DTO
A `@Parent` encodes as an object (`"star": {"id": "..."}`), not a bare id, so decoding a client body into the model fails unless it matches. The docs strongly recommend a DTO:
```swift
struct PlanetDTO: Content {
    var id: UUID?
    var name: String
    var star: Star.IDValue
}
let planetData = try req.content.decode(PlanetDTO.self)
let planet = Planet(id: planetData.id, name: planetData.name, starID: planetData.star)
try await planet.create(on: req.db)
```
Convert to a DTO on the way out too.

## @OptionalChild (one-to-one)
```swift
@OptionalChild(for: \.$planet)
var governor: Governor?
```
`for` is a key path to the child's `@Parent`/`@OptionalParent`. Add with `try await mars.$governor.create(jane, on: database)` (sets parent id automatically). No column on the root model. Enforce one-to-one with a unique constraint on the child's parent column: `.unique(on: "planet_id")`. Without it, several child rows may exist and which one loads is uncontrolled; use `@Children` if you need many.

## @Children (one-to-many)
```swift
final class Star: Model {
    @Children(for: \.$star)
    var planets: [Planet]
}
try await sun.$planets.create(earth, on: database)
```
No schema entry needed on the root.

## Reading
`get(on:)` fetches a relation (`get(reload: true, on:)` forces refetch). `sun.$planets.query(on: database).filter(\.$name =~ "M").all()` queries related models.

Related: vapor-fluent-siblings-eager-loading.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) fluent/relations, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
