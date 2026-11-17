---
id: computing-software.database-administration.influxdb.export-and-migrate-oss-data
name: export-and-migrate-oss-data
category: computing-software
field: database-administration
product: influxdb
tags: [migration, export-lp, line-protocol, influxd-inspect, backup]
level: advanced
status: docs-checked
description: "Move bucket data between OSS servers by exporting line protocol with influxd inspect export-lp and writing it into the target."
sources:
  - https://docs.influxdata.com/influxdb/v2/write-data/migrate-data/migrate-oss/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

On the source server, export a bucket (bucket ID, engine path and output path are required):

```sh
influxd inspect export-lp \
  --bucket-id BUCKET_ID \
  --engine-path /path/to/engine \
  --output-path /path/to/export.lp
```

Optional flags: `--start`, `--end` (time bounds), `--compress` (gzip the output) and `--measurement` (limit to one measurement). If the target is InfluxDB Cloud, export in time-based batches to stay within its rate limits and quotas.

Then write the line protocol into the target bucket:

```sh
influx write --bucket TARGET_BUCKET --file /path/to/export.lp
```

## Checked

- Date: 2026-11-04
- Confirmed against: https://docs.influxdata.com/influxdb/v2/write-data/migrate-data/migrate-oss/
- Scope: export-lp flags and write step.
- Removed: the stopped-influxd claim, the RFC3339 wording and the closing advice on when to use backup instead.
Method: documentation only; no commands were run.
