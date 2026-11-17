---
id: computing-software.web-development.vapor.vapor-fluent-query-join-aggregate
name: vapor-fluent-query-join-aggregate
category: computing-software
field: web-development
product: vapor
tags: [vapor, fluent, fluent-query, join, modelalias, bulk-update, bulk-delete, query-builder]
level: advanced
status: docs-checked
description: "Join models in Fluent queries, reuse one model with ModelAlias, read joined data, and run bulk update and delete queries in Vapor."
sources:
  - https://docs.vapor.codes/fluent/query/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: join tables and do multi-row writes with Fluent's query builder.

## Join
```swift
Planet.query(on: database)
    .join(Star.self, on: \Planet.$star.$id == \Star.$id)
    .filter(Star.self, \.$name == "Sun")
    .all()
```
- `on` takes an equality of two fields: one already in the result set, one on the joined model, same value type.
- Methods like `filter` and `sort` accept the joined type first: `.sort(Star.self, \.$name)`.
- The result is still an array of the base model. Read the joined one with `try planet.joined(Star.self)`.

## Model alias (join the same model twice)
Declare `ModelAlias` types referencing the model:
```swift
final class HomeTeam: ModelAlias {
    static let name = "home_teams"
    let model = Team()
}
final class AwayTeam: ModelAlias {
    static let name = "away_teams"
    let model = Team()
}
```
Use them like models:
```swift
let matches = try await Match.query(on: self.database)
    .join(HomeTeam.self, on: \Match.$homeTeam.$id == \HomeTeam.$id)
    .join(AwayTeam.self, on: \Match.$awayTeam.$id == \AwayTeam.$id)
    .filter(HomeTeam.self, \.$name == "Vapor")
    .sort(AwayTeam.self, \.$name)
    .all()
let home = try match.joined(HomeTeam.self)
print(home.name) // fields reachable via @dynamicMemberLookup
```

## Bulk update
```swift
Planet.query(on: database)
    .set(\.$type, to: .dwarf)
    .filter(\.$name == "Pluto")
    .update()
```
`update` supports `set`, `filter` and `range`.

## Bulk delete
```swift
Planet.query(on: database).filter(\.$name == "Vulcan").delete()
```
`delete` supports `filter`.

Related: vapor-fluent-query-filter-sort.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) fluent/query, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
