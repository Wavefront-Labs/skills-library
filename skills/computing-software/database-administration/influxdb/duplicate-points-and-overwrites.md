---
id: computing-software.database-administration.influxdb.duplicate-points-and-overwrites
name: duplicate-points-and-overwrites
category: computing-software
field: database-administration
product: influxdb
tags: [duplicate-points, line-protocol, timestamps, field-merge, schema]
level: practitioner
status: docs-checked
description: "Why a write can overwrite an existing point: identity is measurement plus tag set plus timestamp, fields merge, and how to keep both points."
sources:
  - https://docs.influxdata.com/influxdb/v2/write-data/best-practices/duplicate-points/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A point is identified by its measurement, tag set and timestamp. Writing a point with the same identity as an existing one is not an error; InfluxDB merges them:

- Field sets are merged into one point.
- If a field key appears in both, the newest written value replaces the old one.
- Field keys present only in one point are kept.

So two readings stamped with the same second and the same tags collapse into one. To preserve both, make the identity differ:

1. Add a tag with a unique value per point (the page uses `uniq=1`, `uniq=2`). The tag sets then differ, so the schemas of the two points differ, which may make querying harder.
2. Or increment the timestamp by 1 nanosecond for the duplicate.

## Checked

2026-11-08: confirmed against the Markdown source of the cited page in the InfluxData docs repository (read in full): point identity, union of field sets, new value wins for matching field keys, the two preservation strategies and the schema caveat. Removed the coarse-precision remark and the cardinality pointer, which the page does not state.
Method: documentation only; no commands were run.
