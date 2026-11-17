---
id: computing-software.data-engineering.druid.druid-deep-storage-options
name: druid-deep-storage-options
category: computing-software
field: data-engineering
product: druid
tags: [deep-storage, local-storage, s3, hdfs, durability, segment-cache]
level: practitioner
status: docs-checked
description: "Choose and configure deep storage, which Druid does not provide itself and which defines data durability."
sources:
  - https://github.com/apache/druid/blob/master/docs/design/deep-storage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deep storage is where segments are stored. Druid does not provide it; the storage you choose defines your durability. As long as Druid processes can see the deep storage and fetch segments from it, you do not lose data however many Druid nodes you lose. If segments disappear from deep storage, you lose them.

Deep storage is also the backing store for query from deep storage, and the load rules you set decide whether segments live only in deep storage or also on Historicals.

Local storage is intended for a single server, or several servers sharing a filesystem such as NFS. For multi-server production clusters the docs recommend cloud storage (Amazon S3, Google Cloud Storage, Azure Blob Storage), S3-compatible storage such as Minio, or HDFS, which are more convenient, scalable and robust than a shared filesystem.

For local storage set in `common.runtime.properties`:
- `druid.storage.type=local`
- `druid.storage.storageDirectory` to a local directory. It must differ from `druid.segmentCache.locations` and `druid.segmentCache.infoDir`.
- `druid.storage.zip` (default `false`) controls whether segments are written as directories or zip files.

Other backends are provided by extensions: `druid-s3-extensions` (S3 or S3-compatible), `druid-google-extensions`, `druid-azure-extensions` and `druid-hdfs-storage`. More options are on the extensions list.

Querying from deep storage is slower than querying segments on Historicals but lowers total storage cost, because you can reach more data without adding Historical capacity.

## Checked

2026-11-08. Read design/deep-storage.md in full. Added druid.storage.zip, the extension names per backend and the query-from-deep-storage trade-off.

Method: documentation only; no commands were run.
