---
id: computing-software.database-administration.influxdb.restore-with-influx-restore
name: restore-with-influx-restore
category: computing-software
field: database-administration
product: influxdb
tags: [restore, influx-restore, full-restore, new-bucket, operator-token]
level: practitioner
status: docs-checked
description: "Restore all data, one bucket, or everything including users and tokens with influx restore; it cannot overwrite existing buckets without --new-bucket."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/backup-restore/restore/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Key rule: `influx restore` cannot restore into existing buckets. Either restore into a new name with `--new-bucket`, or delete the existing bucket first to keep its name.

```sh
# all time series data
influx restore /backups/2020-01-20_12-00/

# one bucket
influx restore /backups/2020-01-20_12-00/ --bucket example-bucket
influx restore /backups/2020-01-20_12-00/ --bucket-id 000000000000

# restore under a different name
influx restore /backups/2020-01-20_12-00/ \
  --bucket example-bucket --new-bucket new-example-bucket

# replace everything, including key-value data (tokens, users, dashboards)
influx restore /backups/2020-01-20_12-00/ --full
```

If the backup came from an instance with token hashing (default in OSS 2.9.0+):

```sh
influx restore --full --operator-token <OPERATOR_TOKEN> /path/to/backup
```

Restores are not supported on InfluxDB Cloud. InfluxDB moves existing data and metadata to a temporary location during restore and deletes it only if the restore succeeds.

## Checked

- Date: 2026-11-04
- Confirmed against: https://docs.influxdata.com/influxdb/v2/admin/backup-restore/restore/
- Scope: restore flags, new-bucket rule and operator-token flag.
Method: documentation only; no commands were run.
