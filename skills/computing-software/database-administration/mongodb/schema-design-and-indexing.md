---
id: computing-software.database-administration.mongodb.schema-design-and-indexing
name: schema-design-and-indexing
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, nosql, document-database, schema-design, data-modelling, embedding, referencing, compound-index, esr-rule, equality-sort-range, explain, executionstats, ttl-index, 16mb-limit]
level: practitioner
status: docs-checked
description: "Model MongoDB documents (embed vs reference, 16 MiB limit), build compound indexes with the ESR guideline, and confirm with explain() executionStats."
sources:
  - https://www.mongodb.com/docs/manual/data-modeling/
  - https://www.mongodb.com/docs/manual/indexes/
  - https://www.mongodb.com/docs/manual/reference/explain-results/
  - https://www.mongodb.com/docs/manual/reference/limits/
  - https://www.mongodb.com/docs/manual/tutorial/equality-sort-range-guideline/
  - https://www.mongodb.com/docs/manual/core/indexes/index-types/index-compound/
  - https://www.mongodb.com/docs/manual/tutorial/analyze-query-plan/
  - https://www.mongodb.com/docs/manual/core/index-ttl/
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# MongoDB schema design and indexing: model for the queries, index with ESR

**Goal:** documents shaped around how the application reads them, indexes that let each hot query examine about as many keys as it returns, proven with `explain()`.

## 1. Start from access patterns
Fields can hold other documents, arrays and arrays of documents, so one-to-one, one-to-many and many-to-many relationships are modelled by **embedding** or **referencing**. Choose per relationship for your access patterns. Embedding lets you avoid joins across collections and return related data in one query (the data-modeling page's own example embeds department information in the employee document). The model can change over time as the application evolves.

Limits (limits page): the maximum BSON document size is **16 mebibytes**; a collection can have no more than 64 indexes; a compound index can have no more than 32 fields. Keep arrays that can grow without bound out of embedded documents (use a separate collection), so a document never nears the size limit.

## 2. Compound indexes: the ESR guideline
Order index keys **Equality, Sort, Range**:
- Equality fields first. Several equality keys may appear in any order relative to each other, but all must precede sort and range fields. More selective equality matches make the indexed query more efficient.
- Sort next, to avoid an in-memory sort. An index supports a sort on a subset of its keys only when the query has equality conditions on all prefix keys before the sort keys.
- Range last. If the range predicate is very selective, putting it before the sort (ERS) can be better, at the cost of an in-memory sort.
- `$ne`, `$nin` and `$regex` are range operators. `$in` alone is equality; with `.sort()`, fewer than 201 elements behave like equality, 201 or more like a range (the page says this threshold is not guaranteed across versions).

Example from the guideline page: query `{ directors: "David Lynch", runtime: { $lt: 130 } }` sorted by `year` is best served by
```js
db.movies.createIndex({ directors: 1, year: 1, runtime: 1 })
```
Prefix rules: a compound index supports queries on any index prefix, so with `{ item: 1, location: 1, stock: 1 }` the prefixes are `{item}` and `{item, location}`. It cannot support `location`, `stock` or `location` plus `stock` alone. If neither index is sparse or unique, an index on a prefix is redundant and can be removed. Sort order (1 or -1) can decide whether a compound index supports a sort.

TTL indexes: `createIndex` on a date field (or array of dates) with `expireAfterSeconds`, an integer between 0 and 2147483647 inclusive.

## 3. Prove it with explain
```js
db.movies.find({ year: { $gte: 2000, $lte: 2005 } }).explain("executionStats")
```
Read:
- `queryPlanner.winningPlan.stage`: `COLLSCAN` is a collection scan (generally expensive); `FETCH` over `IXSCAN` means an index was used. `rejectedPlans` lists plans the planner rejected.
- `executionStats.nReturned`, `totalKeysExamined`, `totalDocsExamined`: the tutorial shows a good result as keys examined matching documents returned, and a large gap between examined and returned as a sign an index may help.
- To compare indexes, use `.hint({...})` with `.explain("executionStats")`: in the tutorial `{ rated: 1, year: 1 }` examined 235 keys for 235 results against 246 for `{ year: 1, rated: 1 }`.
- Explain output can change between MongoDB versions.

## Verify
- [ ] Growing arrays have an upper bound or live in their own collection.
- [ ] Each hot query's index follows ESR and its explain shows IXSCAN without an in-memory sort.
- [ ] Keys and documents examined are close to documents returned.
- [ ] Redundant prefix indexes removed.

## Checked
2026-11-09. Read in full: ESR guideline, compound indexes, "Interpret Explain Plan Results" and the data-modeling and indexes overview pages. Limits (16 MiB, 64 indexes, 32 fields) confirmed by searching the limits page; the TTL and explain-results pages were searched for the quoted fields and bounds, not read end to end. Removed because not supported by the cited pages: the subset, extended-reference, bucket and computed patterns, the embed-versus-reference decision table, schema validation (`collMod` validator), partial indexes, the TTL lag remark, the index build advice, and the `$bsonSize` query.
Method: documentation only; no commands were run.
