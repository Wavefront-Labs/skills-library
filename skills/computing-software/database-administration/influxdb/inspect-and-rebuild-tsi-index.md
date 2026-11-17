---
id: computing-software.database-administration.influxdb.inspect-and-rebuild-tsi-index
name: inspect-and-rebuild-tsi-index
category: computing-software
field: database-administration
product: influxdb
tags: [tsi, influxd-inspect, dump-tsi, build-tsi, index, corruption]
level: advanced
status: docs-checked
description: "Rebuild a corrupt TSI index (stop influxd, delete _series and index directories, run influxd inspect build-tsi) and inspect index files with dump-tsi."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/internals/tsi/rebuild-index/
  - https://docs.influxdata.com/influxdb/v2/admin/internals/tsi/inspect/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Rebuild, used to purge corrupt index files or remove outdated indexed data:

1. Stop `influxd`. Rebuilding while it runs could make some data unqueryable.
2. Go to the `data` directory under the InfluxDB engine path (the path depends on the operating system or a custom engine path setting).
3. Delete every `_series` directory (by default `/data/<bucket-id>/_series`, but check the whole `data` tree).
4. Delete every `index` directory (by default `/data/<bucket-id>/autogen/<shard-id>/index`, again check the whole tree).
5. Run the rebuild:

```sh
influxd inspect build-tsi
```

Inspect:

```sh
influxd inspect dump-tsi \
  --series-file <engine>/data/<bucket-id>/_series \
  <engine>/data/<bucket-id>/autogen/<shard-id>/index
```

`--series-file` (path to the bucket `_series` directory) is required. The default output lists each log (`.tsl`) and index (`.tsi`) file with counts of measurements, tag keys, tag values and series. Add `--series` to output raw series data or `--measurements` for measurement data.

`influxd inspect export-index` exports the index as SQL for inspection and debugging; it takes `--series-path` (the `_series` directory) and `--index-path` (the shard `index` directory). `influxd inspect report-tsi --bucket-id <id>` reports on the cardinality of a bucket's index.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 pages "Rebuild the TSI index" and "Inspect TSI indexes", article bodies read from the downloaded text.

Removed: the unconfirmed note about longer startup or run times on large datasets. Added the export-index and report-tsi flags from the inspect page.
