---
id: computing-software.database-administration.mongodb.graphlookup-recursive-traversal
name: graphlookup-recursive-traversal
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, aggregation-pipeline, graphlookup, hierarchies, recursive-query, org-chart]
level: practitioner
status: verified
description: "Traverse hierarchies and graphs in MongoDB with $graphLookup: org charts, category trees, depth limits, filters, indexes, and the 100 MB memory limit."
sources:
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/graphLookup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# $graphLookup recursive traversal

## Shape
```js
db.employees.aggregate([
  { $match: { _id: "e42" } },
  { $graphLookup: {
      from: "employees",            // collection to search (same db; can be the same collection)
      startWith: "$managerId",      // first value(s) to look up
      connectFromField: "managerId",// field whose value is followed at each step
      connectToField: "_id",        // field matched against
      as: "chain",                  // output array
      maxDepth: 10,                 // 0 = only direct matches
      depthField: "level",          // records depth per result
      restrictSearchWithMatch: { active: true }   // filter applied at every step
  } }
])
```
This walks **up** the management chain. To walk **down** (all reports of a manager):
`startWith: "$_id", connectFromField: "_id", connectToField: "managerId"`.

## Category trees
```js
db.categories.aggregate([
  { $match: { slug: "laptops" } },
  { $graphLookup: { from: "categories", startWith: "$parentId", connectFromField: "parentId",
                    connectToField: "_id", as: "ancestors", depthField: "d" } },
  { $set: { breadcrumb: { $sortArray: { input: "$ancestors", sortBy: { d: -1 } } } } }
])
```
Results in `as` are **unordered**; sort with `depthField` as above.

## Performance
- Index `connectToField` in the `from` collection (`{ _id: 1 }` is free; `{ managerId: 1 }` for
  downward traversal). Without it every step scans the collection.
- Always set `maxDepth` on user-driven queries, and `restrictSearchWithMatch` to prune.
- Memory: the stage is subject to the 100 MB RAM limit; see the `$graphLookup` docs for the `allowDiskUse` behaviour on your version.
- Cycles are handled (a document is not revisited), so loops in data don't hang the query.
- Sharded `from` collections: the `$graphLookup` page is marked "Changed in version 5.1"; read its Sharded Collections section.

## Alternatives
- Materialized path or ancestors array stored in each document (`ancestors: ["root","electronics"]`)
  with a multikey index: fast reads, more work on moves.
- For deep, heavy graph workloads, a graph database may fit better.

## Verify
Compare the traversal result count against a known small subtree; `explain("executionStats")`
on the pipeline shows the `$graphLookup` stage and index usage on the `from` collection.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. On a five-level chain: full walk with `depthField`, `maxDepth: 0` (only the direct match, level 0), `maxDepth: 1`, `restrictSearchWithMatch` pruning at an inactive node (returned nothing), downward traversal, a cycle (each document returned once), and the `$sortArray` breadcrumb by `d` descending all behaved as written. Result order was not depth order.
- Docs fetched: `$graphLookup` page (marked Changed in version 5.1 for sharded collections). The 6.0 spill claim was not confirmed and was replaced by a pointer.
