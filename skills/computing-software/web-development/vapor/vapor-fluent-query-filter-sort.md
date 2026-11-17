---
id: computing-software.web-development.vapor.vapor-fluent-query-filter-sort
name: vapor-fluent-query-filter-sort
category: computing-software
field: web-development
product: vapor
tags: [vapor, fluent, fluent-query, query-builder, filter, sort, pagination, aggregate]
level: practitioner
status: docs-checked
description: "Read models with Fluent's query builder in Vapor: all, first, filter operators, or-groups, sort, range, paginate, aggregates, chunking and field selection."
sources:
  - https://docs.vapor.codes/fluent/query/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: fetch the right models with Fluent. `import Fluent` in any file with queries. Create a builder with `Planet.query(on: database)` or `database.query(Planet.self)`.

## Fetch
- `.all()` returns an array; `.all(\.$name)` returns only that field.
- `.first()` returns an optional (first result or `nil`).

## Filter
Multiple filters must all match.
- Value: `.filter(\.$type == .gasGiant)`. Operators: `==`, `!=`, `>=`, `>`, `<`, `<=`.
- Field vs field: `.filter(\.$firstName == \.$lastName)`.
- Subset: `.filter(\.$type ~~ [.gasGiant, .smallRocky])` (`~~` in set, `!~` not in set); any `Collection` of the field's type works.
- String contains (string fields only): `~~` contains, `!~` not contains, `=~` prefix, `!=~` not prefix, `~=` suffix, `!~=` not suffix. Example: `.filter(\.$name =~ "M")`.
- OR group (top level is an and-group; groups nest):
```swift
Planet.query(on: database).group(.or) { group in
    group.filter(\.$name == "Earth").filter(\.$name == "Mars")
}.all()
```

## Sort, range, paginate
- `.sort(\.$name)`; extra `.sort` calls are tie-break fallbacks in order added.
- `.range(..<5)` first five; `.range(2...)` skips two. Values are unsigned, from zero.
- `paginate(for: req)` reads `page` and `per` from the URI (`GET /planets?page=2&per=5`) and returns `items` plus `metadata` with `page`, `per`, `total`. Pages start at 1. Manual: `.paginate(PageRequest(page: 1, per: 2))`.

## Aggregates
`count()`, and with a key path `sum`, `average`, `min`, `max` (e.g. `.min(\.$name)`). All but `count` return the field's value type; `count` returns an integer.

## Chunk and field
- `.chunk(max: 64) { planets in ... }` handles big reads in pieces; closure runs zero or more times, each item a `Result` (model or decode error).
- `.field(\.$id).field(\.$name)` selects a subset. Unselected fields are uninitialized and reading them directly is a fatal error; check `planet.$name.value` instead.
- `.unique()` returns distinct results, e.g. `User.query(on: database).unique().all(\.$firstName)`. Avoid selecting ids with it.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) fluent/query, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
