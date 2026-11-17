---
id: computing-software.database-administration.influxdb.restore-to-new-server-and-recover-failed-restore
name: restore-to-new-server-and-recover-failed-restore
category: computing-software
field: database-administration
product: influxdb
tags: [restore, disaster-recovery, influx-setup, engine-path, tmp]
level: advanced
status: docs-checked
description: "Restore a backup onto a fresh server by seeding it with the source admin token first, and recover from an interrupted restore from the engine tmp files."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/backup-restore/restore/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Restoring to a new InfluxDB server:

1. Retrieve the admin (operator) token from the source instance.
2. Set up the new instance using that token: `influx setup --token My5uP3rSecR37t0keN`.
3. Run `influx restore /backups/2020-01-20_12-00/ --full`.

If you skip step 2, the restore fails. The first restore call authenticates with the auto-generated token and overwrites the entire key-value store, including that token. The second call then uploads time series data using the now-overwritten token and fails to authenticate, as do later attempts.

If the backup came from an instance with token hashing (default in OSS 2.9.0 and later), it holds no plaintext operator token; pass it to a full restore with `--operator-token <token>` (influx-cli v2.8.0 or later).

Recovering from a failed restore: InfluxDB preserves previous data in a `tmp` directory inside the target engine path (default `~/.influxdbv2/engine`). To recover:

1. Copy the temporary files back into the `engine` directory.
2. Remove the `.tmp` extension from each copied file.
3. Restart `influxd`.

## Checked

Method: docs-checked 2026-11-09 against the Restore data page, read in full from the hashed-token note to the failed-restore recovery section.
