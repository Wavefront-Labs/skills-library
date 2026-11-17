---
id: computing-software.database-administration.influxdb.optimize-line-protocol-writes
name: optimize-line-protocol-writes
category: computing-software
field: database-administration
product: influxdb
tags: [writes, batching, gzip, precision, rate-limit, telegraf]
level: practitioner
status: docs-checked
description: "Tune write throughput: batch 5000 lines, sort tags, use the coarsest timestamp precision, gzip the body, keep NTP in sync and throttle influx write with --rate-limit."
sources:
  - https://docs.influxdata.com/influxdb/v2/write-data/best-practices/optimize-writes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Practices from the optimize-writes page:

- Batch points: the page gives 5000 lines of line protocol as the optimal batch size. Delimit lines with a newline.
- Sort tags by key in lexicographic order before writing (results should match Go `bytes.Compare`).
- Use the coarsest timestamp precision that fits your data. InfluxDB writes nanosecond precision by default; specify the precision when writing.
- Compress: set `content_encoding = "gzip"` on the Telegraf InfluxDB output, or gzip the body and send the `Content-Encoding: gzip` header to `/api/v2/write`.
- Synchronise hosts with NTP. If a point has no timestamp, InfluxDB assigns the host's local time (UTC), so unsynchronised clocks give inaccurate timestamps.
- Limit write speed with the CLI, for example:

```sh
influx write --rate-limit "5MB/5min" -b example-bucket -f data.lp
```

The `--rate-limit` value is `COUNT(B|kB|MB)` or `COUNT(B|kB|MB)/TIME(s|sec|m|min)`, where COUNT is a decimal number and TIME a positive whole number; spaces are ignored. An invalid format makes `influx write` print the format and its regular expression. The flag also works with `influx write dryrun`.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 optimize-writes page, relevant sections read from the downloaded text.

Removed: the "up to 5x" benchmark figure (not on the page) and the old 300 MB example value.
