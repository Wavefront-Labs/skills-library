---
id: computing-software.database-administration.influxdb.migrate-cloud-data-to-oss-with-a-task
name: migrate-cloud-data-to-oss-with-a-task
category: computing-software
field: database-administration
product: influxdb
tags: [migration, cloud, flux-tasks, secrets, batch, from-host]
level: advanced
status: docs-checked
description: "Pull data from InfluxDB Cloud into OSS with a batching Flux task driven by a migration record, with the token held in a secret."
sources:
  - https://docs.influxdata.com/influxdb/v2/write-data/migrate-data/migrate-cloud-to-oss/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Run a task on the OSS server that reads from Cloud with `from(host:...)`. Store the Cloud token as a secret first (`INFLUXDB_CLOUD_TOKEN`) and read it with `secrets.get`. The task defines a `migration` record:

- `start` and `stop`: overall time range to migrate.
- `batchInterval`: size of each batch.
- `batchBucket`: a bucket that tracks progress.
- `sourceHost`, `sourceOrg`, `sourceToken`, `sourceBucket`: the Cloud source.
- `destinationBucket`: the OSS target.

Each run copies one batch and records it, so the task works through the range over repeated runs. When finished the task fails with `Batch range is beyond the migration range. Migration is complete.` which signals completion; then delete the task.

Setup: create a Cloud API token with read access to the source bucket, add it to OSS as the secret above, create the destination bucket and a separate bucket for batch metadata, then save the task (new tasks are enabled, so migration starts on save). Set `task.every` to `5m` as recommended, since Cloud rate limits and quotas reset every five minutes.

Cloud quotas and rate limits apply to the reads. Dense data needs a shorter `batchInterval`; if you hit `too many requests`, timeouts or a "wrong number of fields" error, use a smaller `batchInterval`.

## Checked

Method: docs-checked 2026-11-09 against the Migrate data from InfluxDB Cloud to OSS page, from the overview through the batch-interval and troubleshooting sections.
