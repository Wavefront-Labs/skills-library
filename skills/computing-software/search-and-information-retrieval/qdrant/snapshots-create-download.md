---
id: computing-software.search-and-information-retrieval.qdrant.snapshots-create-download
name: snapshots-create-download
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [snapshots, backup, tar, storage, snap-create]
level: practitioner
status: docs-checked
description: "Create, list and download collection and full-storage snapshots, and store them locally or in S3, GCS or Azure."
sources:
  - "https://qdrant.tech/documentation/snapshots/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A snapshot is a tar archive of a collection's data and configuration on one node at one time. Creating one is a synchronous request:

```http
POST /collections/{collection_name}/snapshots
GET  /collections/{collection_name}/snapshots
GET  /collections/{collection_name}/snapshots/{snapshot_name}
```

Facts from the docs:

- Snapshots are per node and per collection. In a cluster, snapshot every node that holds shards.
- The file is created in the snapshots path (`./snapshots` by default) and can be downloaded over REST.
- A full-storage snapshot (`POST /snapshots`) covers the whole storage; it can be restored only through the Qdrant CLI at startup.
- `snapshots_storage` can be `local`, `s3`, `gcs` or `azure`.
- A snapshot can only be restored to a cluster running the same minor version or the next minor version.

## Checked

2026-11-03. Confirmed on the Qdrant snapshots page: tar archive per collection per node, synchronous creation into the snapshot path, full-storage snapshots restored only through the CLI at startup, `snapshots_storage` values `local`, `s3`, `gcs`, `azure`, the minor-version restore rule. Removed the unconfirmed aliases claim and the generic operational tips.

Method: documentation only; no commands were run.
