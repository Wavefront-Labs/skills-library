---
id: computing-software.database-administration.time-series-databases.influxdb-tags-vs-fields
name: influxdb-tags-vs-fields
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-data-model, influxdb-tags-vs-fields, influxdb, flux]
level: practitioner
status: docs-checked
description: "Decide which attributes become tags (indexed) and which become fields (values) to keep series count low and queries fast."
sources:
  - https://docs.influxdata.com/influxdb/v2/write-data/best-practices/schema-design/
  - https://docs.influxdata.com/influxdb/v2/reference/key-concepts/data-elements/
  - https://docs.influxdata.com/influxdb/v2/write-data/best-practices/resolve-high-cardinality/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tags versus fields

**Goal:** Decide which attributes become tags (indexed) and which become fields (values) to keep series count low and queries fast.

## Steps
- Tags: indexed, always strings; store values as tags if they can reasonably be indexed, are used in `filter()` or `group()`, or are shared metadata across points.
- Fields: not indexed; values can be strings, floats, integers or booleans. Store numeric, unique or frequently changing values (readings, counters, ids) as fields.
- Each unique set of indexed elements (measurement plus tags) forms a series key.
- Keep measurements and keys simple: do not encode data in the measurement name or in field keys, and avoid keywords and special characters in keys.

**Gotcha:** Tags holding highly variable data such as unique IDs, hashes or random strings cause high series cardinality, which slows reads and writes and drives memory use.

## Verify
- `import "influxdata/influxdb"` then `influxdb.cardinality(bucket:"b", start:-30d)` returns a count in the expected range.
- Common dashboards filter only on tags.

## Checked

2026-11-03. Confirmed in the schema-design page (tags indexed and fields not, when to use each, keep measurements and keys simple), the data-elements page (tags stored as strings; field value types) and the resolve-high-cardinality page. Removed: the per-device measurement example, the series-multiplication wording and the "never filter or group by it" rule of thumb as stated.
Method: documentation only; no commands were run.

