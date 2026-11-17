---
id: computing-software.web-development.vapor.vapor-fluent-siblings-eager-loading
name: vapor-fluent-siblings-eager-loading
category: computing-software
field: web-development
product: vapor
tags: [vapor, fluent, fluent-relations, siblings, pivot, eager-loading, many-to-many, with]
level: advanced
status: docs-checked
description: "Build many-to-many relations in Vapor Fluent with @Siblings and a pivot model, attach and detach, and eager or lazily load relations with with and get."
sources:
  - https://docs.vapor.codes/fluent/relations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: many-to-many with a pivot, and efficient relation loading.

## Pivot model
Any model with at least two `@Parent` relations (one per side) works; extra properties are allowed.
```swift
final class PlanetTag: Model {
    static let schema = "planet+tag"
    @ID(key: .id) var id: UUID?
    @Parent(key: "planet_id") var planet: Planet
    @Parent(key: "tag_id") var tag: Tag
    @OptionalField(key: "comments") var comments: String?
    init() { }
}
```
Prevent duplicates in the pivot schema: `.unique(on: "planet_id", "tag_id")`.

## @Siblings (both sides)
```swift
// on Planet
@Siblings(through: PlanetTag.self, from: \.$planet, to: \.$tag)
public var tags: [Tag]
// on Tag
@Siblings(through: PlanetTag.self, from: \.$tag, to: \.$planet)
public var planets: [Planet]
```
`through` is the pivot type; `from` points to the pivot parent for the root model; `to` to the related one.

## Attach / detach
```swift
try await earth.$tags.attach(inhabited, on: database)
try await earth.$tags.attach(inhabited, on: database) { pivot in
    pivot.comments = "This is a life-bearing planet."
}
try await earth.$tags.attach([volcanic, oceanic], on: database) { pivot in ... }
try await earth.$tags.attach(inhabited, method: .ifNotExists, on: database)
try await earth.$tags.detach(inhabited, on: database)  // deletes the pivot
earth.$tags.isAttached(to: inhabited)
```
Pivots are created and saved as needed. `method:` is for attaching a single model.

## Eager loading
`with` preloads relations: one extra query per relation regardless of result count; only works with `all` and `first`.
```swift
let planets = try await Planet.query(on: database).with(\.$star).all()
for planet in planets { print(planet.star.name) } // synchronous access
```
Nested (no depth limit):
```swift
Planet.query(on: database).with(\.$star) { star in star.with(\.$galaxy) }.all()
```

## Lazy loading
`try await planet.$star.get(on: database)` then `planet.star.name`; `get(reload: true, on:)` bypasses the cache. `planet.$star.value != nil` tells whether the relation is loaded. Set manually with `planet.$star.value = star`, no query.

Related: vapor-fluent-relations-parent-child.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) fluent/relations, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
