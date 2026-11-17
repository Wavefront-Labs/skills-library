---
id: computing-software.database-administration.time-series-databases.influxdb-series-cardinality
name: influxdb-series-cardinality
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-cardinality, influxdb-series-cardinality, influxdb, flux]
level: practitioner
status: docs-checked
description: "Measure how many series exist and find which tags cause growth."
sources:
  - https://docs.influxdata.com/flux/v0/stdlib/influxdata/influxdb/cardinality/
  - https://docs.influxdata.com/flux/v0/stdlib/influxdata/influxdb/schema/tagvalues/
  - https://docs.influxdata.com/influxdb/v2/write-data/best-practices/resolve-high-cardinality/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Series cardinality diagnosis

**Goal:** Measure how many series exist and find which tags cause growth.

## Steps
- Total: `import "influxdata/influxdb"` then `influxdb.cardinality(bucket: "b", start: -30d)`.
- Per measurement: `influxdb.cardinality(bucket:"b", start:-30d, predicate: (r) => r._measurement == "cpu")`.
- Tag values: `import "influxdata/influxdb/schema"` then `schema.tagValues(bucket:"b", tag:"host") |> count()`.
- Each unique set of indexed data elements (measurement and tags) forms a series key; tags holding unique IDs, hashes or random strings cause high cardinality, a primary driver of high memory use.
- Cure: move unbounded tags to fields (unique or frequently changing values belong in fields) and rework the schema; see the resolve-high-cardinality page.

**Gotcha:** `influxdb.cardinality()` is time bounded and reports the cardinality of data matching the `start`, `stop` and `predicate` you pass, not the bucket as a whole.

## Verify
- Cardinality stops growing after the fix.

## Checked

2026-11-03. Confirmed in the `influxdb.cardinality()` and `schema.tagValues()` Flux pages (imports, `bucket`, `start`, `predicate`, `tag` parameters) and the resolve-high-cardinality page (causes, fields for unique values, memory impact). Removed: the product-of-tag-counts formula, `tagexclude`, the million-series rule of thumb, the index-shrink claim and the compaction-cycle claim.
Method: documentation only; no commands were run.

