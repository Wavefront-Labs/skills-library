---
id: computing-software.database-administration.influxdb.find-and-resolve-high-cardinality
name: find-and-resolve-high-cardinality
category: computing-software
field: database-administration
product: influxdb
tags: [cardinality, series, schema, influxdb-cardinality, tags, performance]
level: advanced
status: docs-checked
description: "Measure series cardinality with Flux or InfluxQL and trace it to the offending tag, then fix the schema and delete the unwanted data."
sources:
  - https://docs.influxdata.com/influxdb/v2/write-data/best-practices/resolve-high-cardinality/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

InfluxDB indexes the measurement and tags; each unique set of those forms a series key. Tags holding highly variable data (unique IDs, hashes, random strings) create very many series, and high series cardinality is a primary driver of high memory usage.

Measure it per bucket with the Flux function `influxdb.cardinality()` or the InfluxQL command `SHOW SERIES CARDINALITY`; both return the number of unique series keys.

To find the culprit, count unique values per tag with the `influxdata/influxdb/schema` package: `schema.tagKeys(bucket: ...)` lists tags and `schema.tagValues(bucket: ..., tag: ...)` followed by `count()` counts the values of one tag. Look for tags with values orders of magnitude higher than the others. If the combined query times out under runaway cardinality, run `tagKeys` first and then the per-tag count one tag at a time. Check again after 24 hours to see which tags are growing.

Common causes listed on the page:

- Log messages written to tags (a unique timestamp, pointer value or string makes each value unique).
- Timestamps written to tags, usually by accident in client code.
- Unique tag values that grow over time, such as a user ID tag as the user base grows.

Resolve it in three steps, for each bucket if there are several: review tags, improve the schema (see the schema design practices), and delete the high-cardinality data you no longer need by deleting the whole bucket or a range of data.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 "Resolve high cardinality" page, read from line 580 to the end of the article in the downloaded text.

Removed: the `start: -1y` call arguments, the series definition that included field keys, the `storage_bucket_series_num` metric, and advice to move values to fields or let retention expire old series, none of which the page states.
