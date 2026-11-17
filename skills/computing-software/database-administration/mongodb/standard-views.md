---
id: computing-software.database-administration.mongodb.standard-views
name: standard-views
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-views, createview, read-only-views, aggregation-pipeline]
level: practitioner
status: verified
description: "Create, modify and secure MongoDB standard (non-materialized) views with db.createView, understand their restrictions and when an on-demand materialized view is better."
sources:
  - https://www.mongodb.com/docs/manual/core/views/
  - https://www.mongodb.com/docs/manual/reference/method/db.createView/
  - https://www.mongodb.com/docs/manual/core/views/create-view/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Standard views

**Goal:** expose a filtered/reshaped, read-only projection of a collection (hide PII fields, pre-join lookup data) without copying data.

## Create
```javascript
db.createView("customers_public", "customers", [
  { $match: { deleted: { $ne: true } } },
  { $project: { _id: 1, name: 1, country: 1, createdAt: 1 } }   // no email, phone
])
```
A view is stored in `system.views`; the pipeline runs on every read. Queries against it are appended to the view pipeline, so indexes on the source are used only by leading `$match`/`$sort` stages.

## Modify / drop
```javascript
db.runCommand({ collMod: "customers_public", viewOn: "customers", pipeline: [ /* new */ ] })
db.customers_public.drop()
```

## Restrictions
- Read-only: inserts/updates fail.
- `find()` projection operators `$`, `$elemMatch`, `$slice`, `$meta` are not supported on views.
- No indexes of its own; `explain()` shows the expanded pipeline over the source.
- Cannot rename a view; drop and recreate.
- `$text` search and `$geoNear` are not supported against views; `mapReduce` on a view errors ("mapReduce on a view is not supported"). View pipelines cannot contain `$out` or `$merge` (docs).
- Collation: a view can be created with a default collation; queries cannot override it ("Cannot override a view's default collation"), and views combined with `$lookup`/`$graphLookup` must have the same collation per the docs.

## Security pattern
Grant users `find` on the view but not on the source:
```javascript
db.createRole({ role: "readCustomersPublic", privileges: [
  { resource: { db: "crm", collection: "customers_public" }, actions: ["find"] } ], roles: [] })
```
Per the views docs, querying a view needs only `find` on the view namespace: no `find` is required on the source collection or on collections named in the view pipeline (including `$lookup` targets). Creating a view is different: it needs `createCollection` on the database.

## Standard vs materialized
| Standard view | On-demand materialized view (`$merge`) |
|---|---|
| Always current | As fresh as the last refresh |
| Computes on every read | Precomputed, indexable |
| Good for light filters/projections | Good for heavy aggregations |

## Verify
`db.getCollectionInfos({ type: "view" })` lists views and pipelines; `db.customers_public.find().explain()` shows `IXSCAN` on the source (namespace of the source collection) when the leading `$match` is indexable.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. `createView` with `$match` + `$project` returned only the live customer; the view is listed in `system.views` and by `getCollectionInfos({type: "view"})` with `readOnly: true`; `explain()` reports the source namespace and an `IXSCAN` when `deleted` is indexed (for both `$ne: true` and `deleted: false` pipelines).
- Errors confirmed: insert and update ("is a view, not a collection"), `$slice`, `$elemMatch`, `$meta` and positional `$` projections, rename ("cannot rename view"), `createIndex`, `$text`, `$geoNear`, `mapReduce`, collation override. `collMod` with `viewOn` and a new pipeline changed the output; `drop()` returned true; `createRole` with a `find` privilege on the view namespace succeeded.
- Docs fetched: views page and create-view page (find privilege on the view only; no `$out`/`$merge` in view pipelines; `$lookup` views need the same collation). The earlier `$lookup`-target privilege claim contradicted the docs and was replaced.
