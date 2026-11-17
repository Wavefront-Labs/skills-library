---
id: computing-software.data-engineering.druid.druid-schema-design-basics
name: druid-schema-design-basics
category: computing-software
field: data-engineering
product: druid
tags: [schema-design, datasource, dimensions, metrics, timestamp, data-model]
level: practitioner
status: docs-checked
description: "Apply Druid's data model: datasources, mandatory timestamp, dimensions versus metrics."
sources:
  - https://github.com/apache/druid/blob/master/docs/ingestion/schema-design.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Druid data lives in datasources, similar to tables in an RDBMS. A datasource can be ingested with or without rollup.

Core rules of the data model:
- Every row must have a timestamp. Data is always partitioned by time and every query has a time filter. Results can be broken down by time buckets.
- All columns other than the timestamp are either dimensions or metrics, following standard OLAP naming.
- Typical production datasources have tens to hundreds of columns.
- Dimension columns are stored as-is, so they can be filtered on, grouped by or aggregated at query time. They are single Strings, arrays of Strings, single Longs, single Doubles or single Floats.
- Metric columns are stored pre-aggregated, so they can only be aggregated at query time, not filtered or grouped by. They are often numbers but can be complex objects such as HyperLogLog or approximate quantile sketches.

The page then gives tips for users arriving from other kinds of systems, and general common practices.

## Checked

Method: 2026-11-09 docs-only read of the cited source page (opening rules section checked line by line). All claims match the page; unchanged.
