---
id: computing-software.database-administration.influxdb.delete-data-with-influx-delete
name: delete-data-with-influx-delete
category: computing-software
field: database-administration
product: influxdb
tags: [delete, delete-predicate, influx-delete, compaction, api]
level: practitioner
status: docs-checked
description: "Delete points by time range and predicate with influx delete or POST /api/v2/delete, with the predicate limits and the no-delete-by-field rule."
sources:
  - https://docs.influxdata.com/influxdb/v2/write-data/delete-data/
  - https://docs.influxdata.com/influxdb/v2/reference/syntax/delete-predicate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

CLI:

```sh
influx delete --bucket example-bucket \
  --start 2020-03-01T00:00:00Z --stop 2020-11-14T00:00:00Z \
  --predicate '_measurement="example-measurement" AND exampleTag="exampleTagValue"'
```

API: `POST /api/v2/delete` with query parameters `org` and `bucket` and a JSON body holding `start`, `stop` and `predicate`. Omitting the predicate deletes everything in the time range.

The CLI also accepts `-p` as the short form of `--predicate`. Supported delete criteria are time range, measurement (`_measurement`) and tag; the docs state that deleting by field is not supported.

Predicate limits: only `AND` (no `OR`), only equality `=` (no `!=`), no regular expressions, and no filtering on the `_time`, `_field` or `_value` columns.

Once a delete request completes, the data is no longer queryable but remains on disk until the compaction service runs, so disk usage does not drop immediately.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 pages delete-data and delete-predicate syntax, both read in full as downloaded text.

Confirmed: CLI flags, `/api/v2/delete` query parameters and body fields, no-predicate behaviour, predicate limits, compaction note. Corrected: an earlier note claimed the predicate page uses `_field` in examples; the page now lists `_field` as unsupported.