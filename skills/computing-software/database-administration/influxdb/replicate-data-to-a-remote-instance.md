---
id: computing-software.database-administration.influxdb.replicate-data-to-a-remote-instance
name: replicate-data-to-a-remote-instance
category: computing-software
field: database-administration
product: influxdb
tags: [replication, influx-remote, influx-replication, queue, remote-write]
level: advanced
status: docs-checked
description: "Stream writes from a local bucket to a remote instance with influx remote and influx replication, with queue size and age defaults."
sources:
  - https://docs.influxdata.com/influxdb/v2/write-data/replication/replicate-data/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

1. Create a remote connection:

```sh
influx remote create --name REMOTE --remote-url https://remote.example.com \
  --remote-api-token REMOTE_TOKEN --remote-org-id REMOTE_ORG_ID
```

2. Create the replication stream:

```sh
influx replication create --name STREAM --remote-id REMOTE_ID \
  --local-bucket-id LOCAL_BUCKET_ID --remote-bucket REMOTE_BUCKET_NAME
```

`influx replication list` shows the queue size and the latest status. API endpoints are `/api/v2/remotes` and `/api/v2/replications`.

Queue settings: `maxAgeSeconds` default 604800 (7 days), `maxQueueSizeBytes` default 67108860 with a minimum of 33554430, and `dropNonRetryableData` to discard data the remote rejects permanently. For an InfluxDB Enterprise 1.x target use `db/rp` as the remote bucket. To replicate downsampled data, write it to a bucket with a task using `to()` and replicate that bucket. Replication service-level metrics are available from the local `/metrics` endpoint.

## Checked

- Date: 2026-11-04
- Confirmed against: https://docs.influxdata.com/influxdb/v2/write-data/replication/replicate-data/ and the influx replication create CLI reference.
- Scope: commands and flags, queue defaults, Enterprise db/rp syntax, downsample note, /metrics.
- Removed: the unconfirmed `replications_queue_*` metric name.
Method: documentation only; no commands were run.
