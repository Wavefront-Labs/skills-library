---
id: computing-software.database-administration.influxdb.delete-bucket-by-name-or-id
name: delete-bucket-by-name-or-id
category: computing-software
field: database-administration
product: influxdb
tags: [bucket, influx-bucket-delete, delete]
level: intro
status: docs-checked
description: "Delete an InfluxDB v2 bucket with influx bucket delete by name plus org or by ID, or in the UI; confirm the ID with influx bucket list first."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/buckets/delete-bucket/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Delete by name (requires the bucket name and its organization name or ID):

```sh
influx bucket delete -n my-bucket -o my-org
```

Delete by ID (get the ID from `influx bucket list`):

```sh
influx bucket delete -i 034ad714fdd6f000
```

In the OSS UI: Data (Load Data) > Buckets, hover over the bucket, click the delete icon at the far right of the bucket name, then click Delete.

Practical check before deleting: list buckets first and confirm the ID matches the intended bucket.

## Checked

2026-11-08: confirmed against the page's Markdown source in the InfluxData docs repository (the shared delete-bucket file behind the cited page, read in full): UI steps for v2, `influx bucket delete -n/-o` and `-i`, and that `influx bucket list` gives the ID. Removed the "no soft delete" claim, the claim about tasks, dashboards and Telegraf configs referring to the bucket by name, and the `influx delete` pointer, none of which the page states.
Method: documentation only; no commands were run.
