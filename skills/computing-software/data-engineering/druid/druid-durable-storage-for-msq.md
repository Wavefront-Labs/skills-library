---
id: computing-software.data-engineering.druid.druid-durable-storage-for-msq
name: druid-durable-storage-for-msq
category: computing-software
field: data-engineering
product: druid
tags: [durable-storage, msq, intermediate-storage, s3, temp-dir]
level: advanced
status: docs-checked
description: "Enable durable storage for SQL-based ingestion and queries from deep storage."
sources:
  - https://github.com/apache/druid/blob/master/docs/operations/durable-storage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Durable storage improves querying from deep storage and SQL-based ingestion. S3, Google Storage and Azure Blob Storage are supported. For deep storage queries it is where results are written; for SQL-based ingestion it temporarily holds intermediate files, which can improve reliability.

Enabling it also lets tasks use local disk for temporary files such as intermediate sort files, bounded by the task storage size configuration. If that limit is too low you may see `NotEnoughTemporaryStorageFault`.

Set these common service properties, shown for S3:

```
druid.msq.intermediate.storage.enable=true
druid.msq.intermediate.storage.type=s3
# Remote storage location
druid.msq.intermediate.storage.bucket=YOUR_BUCKET
druid.msq.intermediate.storage.prefix=YOUR_PREFIX
# Local temporary directory (on each Druid server)
druid.msq.intermediate.storage.tempDir=/path/to/your/temp/dir
```

For Google Storage the `type` is `google` with the same bucket and prefix settings. For Azure Blob Storage the `type` is `azure` and you set `druid.msq.intermediate.storage.container` instead of the bucket. If tasks run out of temporary space, revisit the task storage size configuration.

Using it:
- SQL-based ingestion: set the query context parameter `durableShuffleStorage` to `true`. For worker fault tolerance set `faultTolerance` to `true`, which sets `durableShuffleStorage` to `true` automatically.
- Queries from deep storage: results go to task reports by default, which can time out for large result sets. Set the context parameter `selectDestination` to `durableStorage` to write final results to durable storage instead. Workers' intermediate results go to a different location, so you can enable one without the other. Results are cleaned up when the task is removed from the metadata store.

Cleanup: a periodic cleaner removes directories with no running controller task, configured with `druid.msq.intermediate.storage.cleaner.enabled` and `druid.msq.intermediate.storage.cleaner.delaySeconds`. Use the location only for the cluster's MSQ task output, because other files or directories there get cleaned up too.

## Checked

2026-11-08. Read operations/durable-storage.md in full. Fixed the Google Storage type value (google, not goog), added Azure settings, context parameters and the cleaner.

Method: documentation only; no commands were run.
