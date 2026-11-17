---
id: computing-software.web-development.vapor.vapor-fluent-timestamps-softdelete
name: vapor-fluent-timestamps-softdelete
category: computing-software
field: web-development
product: vapor
tags: [vapor, fluent, fluent-model, timestamp, soft-delete, modelmiddleware, lifecycle, swift]
level: practitioner
status: docs-checked
description: "Use Fluent @Timestamp triggers and formats, soft delete with restore and withDeleted, and model lifecycle middleware."
sources:
  - https://docs.vapor.codes/fluent/model/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: have Fluent maintain created/updated/deleted dates, soft-delete rows, and hook into model events.

## @Timestamp
A `@Field` holding a `Date?`, set by Fluent on a trigger; initialize it to `nil`.

```swift
@Timestamp(key: "created_at", on: .create) var createdAt: Date?
@Timestamp(key: "updated_at", on: .update) var updatedAt: Date?
```
Triggers: `.create` (new model saved), `.update` (existing model saved), `.delete` (model deleted, see soft delete).

Format via `format:`. `.default` is an efficient driver `datetime` (Date); `.iso8601` is a String (supports `withMilliseconds`); `.unix` is a Double of seconds since epoch.

```swift
@Timestamp(key: "updated_at", on: .update, format: .iso8601)
var updatedAt: Date?
```
The migration for the `.iso8601` example must store `.string`: `.field("updated_at", .string)`. Raw value access: `model.$updatedAt.timestamp = "2020-06-03T16:20:14+00:00"`.

## Soft delete
Adding a `.delete`-trigger timestamp enables it:

```swift
@Timestamp(key: "deleted_at", on: .delete) var deletedAt: Date?
```
Soft-deleted rows stay in the database but are not returned by queries. You may set the timestamp to a future date as an expiry. Then:
- `model.delete(force: true, on: database)` removes it for real.
- `model.restore(on: database)` clears the timestamp.
- `Planet.query(on: database).withDeleted().all()` includes soft-deleted rows.

## Lifecycle middleware
Events: `create`, `update`, `delete(force:)`, `softDelete`, `restore`; each runs before the event. Conform to `ModelMiddleware` or `AsyncModelMiddleware`; every method has a default, so implement only what you need. A method may return early, fail, or call `next`; work after the event goes after `next` completes.

```swift
struct PlanetMiddleware: AsyncModelMiddleware {
    func create(model: Planet, on db: Database, next: AnyAsyncModelResponder) async throws {
        model.name = model.name.capitalized()
        try await next.create(model, on: db)
        print("Planet \(model.name) was created")
    }
}
app.databases.middleware.use(PlanetMiddleware(), on: .psql)
```
(The future form uses `ModelMiddleware`, `AnyModelResponder` and returns `next.create(model, on: db).map { ... }`.)

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) fluent/model, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
