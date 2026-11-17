---
id: computing-software.data-engineering.druid.druid-query-from-deep-storage
name: druid-query-from-deep-storage
category: computing-software
field: data-engineering
product: druid
tags: [deep-storage, query-from-deep-storage, load-rules, centralized-schema, slow-queries]
level: advanced
status: docs-checked
description: "Query Druid segments held only in deep storage: prerequisites, load rules to keep them off Historicals, and the async SQL statements API."
sources:
  - https://github.com/apache/druid/blob/master/docs/querying/query-from-deep-storage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Druid can query segments stored only in deep storage. It is slower than querying segments on Historicals, but suits infrequently accessed data or cases where low latency is unnecessary, and widens queryable data without scaling Historicals. It uses the multi-stage query (MSQ) task engine.

## Prerequisites

The datasource must meet one of:
- At least one of its segments (any) is loaded on a Historical so Druid can plan the query (visible in the console).
- The centralized datasource schema feature is enabled (experimental). For datasources created before enabling it, load segments from deep storage onto a Historical so the schema backfills in the metadata database. Only dimensions present in the loaded segments' schema are queryable, so load all segments if you need all dimensions. Afterwards you can unload them.

## Keeping segments only in deep storage

All ingested data is already in deep storage. To avoid loading segments onto Historicals use a load rule with `tieredReplicants` empty (`{}`) and `useDefaultTierForNull` false, for example `loadByInterval` over the chosen interval. Segments outside it follow the default or other rules. Set it in the console (Datasources, Actions, Edit retention rules, JSON tab).

Verify: `SELECT "segment_id", "replication_factor" FROM sys."segments" WHERE "replication_factor" = 0 AND "datasource" = '<datasource>'`, or the Replication factor column on the Segments page. Replication factor 0 means the query runs directly against deep storage. Actual replicas can differ temporarily while rules are processed.

## Running a query

- Submit with `POST /druid/v2/sql/statements` on the Router (or the console). Same body as the normal SQL endpoint, with `query` in the JSON.
- Extra context parameters: `executionMode` (required) set to `ASYNC`; `selectDestination` (optional) set to `durableStorage` to write SELECT results to durable storage. Use `durableStorage` for result sets over 3000 rows; it requires durable storage for MSQ to be enabled. Context can also be given with `SET` statements before the query.
- The response carries `queryId`, `state` (`ACCEPTED`), `createdAt`, `schema`, `durationMs`.
- Status: `GET /druid/v2/sql/statements/{queryId}`. Wait for `SUCCESS` before fetching results. A successful status includes `numTotalRows`, `sampleRecords` and `pages` (each with `numRows`, `sizeInBytes`, `id`).
- Results: `GET /druid/v2/sql/statements/{queryId}/results?page=<n>&resultFormat=<fmt>`. Only the submitting user can fetch results. Formats: `arrayLines`, `objectLines`, `array`, `object` (default), `csv`. If you get an error that the query is still running, wait and retry.

## Checked

2026-11-08. Read the cited query-from-deep-storage page in full. Expanded the draft with the load-rule recipe, verification query and the statements API flow.

Method: documentation only; no commands were run.
