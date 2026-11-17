---
id: computing-software.database-administration.influxdb.update-bucket-name-and-retention
name: update-bucket-name-and-retention
category: computing-software
field: database-administration
product: influxdb
tags: [bucket, influx-bucket-update, rename, retention]
level: practitioner
status: docs-checked
description: "Rename a bucket or change its retention with influx bucket update by ID, and know which assets break when a bucket name changes."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/buckets/update-bucket/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`influx bucket update` needs the bucket ID (from `influx bucket list`) and the organization name or ID.

```sh
# rename
influx bucket update -i 034ad714fdd6f000 -n my-new-bucket

# change retention
influx bucket update -i 034ad714fdd6f000 -r 1209600000000000ns
```

Retention units are `ns`, `us`/`µs`, `ms`, `s`, `m`, `h`, `d`, `w`; the minimum is one hour.

Renaming affects every asset that references the bucket by name: queries, dashboards, tasks, Telegraf configurations and templates. If you rename a bucket, update the bucket in each of those places as well. In the UI go to Data (Load Data) > Buckets > Settings > Rename, click "I understand, let's rename my bucket", enter the new name and click Change Bucket Name.

Retention can also be edited in the UI: Data (Load Data) > Buckets > Settings, edit the retention period, then Save Changes. The page points to separate bucket naming restrictions for permitted names.

## Checked

2026-11-08: confirmed against the Markdown source of the cited page in the InfluxData docs repository (read in full): CLI requirements and both examples, retention units and one-hour minimum, the list of assets affected by a rename, and the UI rename and retention steps. Removed the naming rules, which the page does not state itself, and the "keep pointing at the old name" wording.
Method: documentation only; no commands were run.
