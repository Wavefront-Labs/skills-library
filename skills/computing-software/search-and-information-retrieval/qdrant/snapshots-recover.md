---
id: computing-software.search-and-information-retrieval.qdrant.snapshots-recover
name: snapshots-recover
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [snapshot-recovery, restore, priority, startup, snap-recover]
level: advanced
status: docs-checked
description: "Recover a Qdrant collection from a snapshot by URL, file URI, upload or at startup, and pick the right recovery priority."
sources:
  - https://qdrant.tech/documentation/snapshots/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

To restore from a URL or a file already on the node, use the recover endpoint with a location. If the target collection does not exist it is created.

```http
PUT /collections/{collection_name}/snapshots/recover
{ "location": "file:///tmp/snapshot-2022-10-10.snapshot",
  "priority": "snapshot" }
```

Three ways to restore:

- URL or local file: `location` is a URL or a `file:///` URI. A URL must be reachable by the Qdrant node being restored. URL recovery is not supported on Qdrant Cloud (outbound traffic is blocked); use a file URI or an upload there.
- Uploaded file: `POST /collections/{collection_name}/snapshots/upload?priority=snapshot` with a multipart form field `snapshot=@file`. Typical for migrating to a new cluster.
- At startup (single-node self-hosted only; not for multi-node deployments or Cloud).

`priority` decides which data wins when the snapshot and existing data conflict:

- `replica` (default): existing data is preferred over the snapshot.
- `snapshot`: snapshot data is preferred.
- `no_sync`: restore with no synchronization, for managing or transferring shards by hand; misuse leaves the cluster broken.

To recover into a new (empty) collection you must set `snapshot`: with the default `replica` priority you end up with an empty collection. The docs recommend `snapshot` when migrating between clusters.

Startup restore without the API takes `<snapshot_file_path>:<target_collection_name>` pairs:

```bash
./qdrant --snapshot /snapshots/test-collection-archive.snapshot:test-collection
```

The target collection must be absent or the program exits with an error. The `--force_snapshot` flag overwrites an existing collection; use it with caution.

Constraints:

- A snapshot restores only to a cluster on the same minor version or the next minor version (a v1.18.1 snapshot restores to v1.18.x with x of 1 or more, or v1.19.x).
- A snapshot holds only the data of the node it was made on, so in a distributed deployment create (and restore) snapshots per node.
- Collection aliases are not in a collection snapshot; migrate them separately.
- Qdrant registers the recovered shards in the cluster; if other active replicas of those shards exist, it replicates them to the recovered node by default.
- Full-storage snapshots (`POST /snapshots`) are for single-node deployments only.

Verify afterwards by comparing point counts and running a few known queries before routing traffic.

## Checked

2026-11-08. Confirmed against the Snapshots page (read from the top through the full-storage section; the remainder is full-storage download and tutorial links): recover endpoint, URL/file/upload/startup methods, Cloud URL restriction, priority values and default, `--snapshot` and `--force_snapshot`, version compatibility, per-node snapshots, aliases. Corrected: restore is to the same or the next minor version, not the previous one. Removed: unsourced advice on verifying shard layout after recovery.
Method: documentation only; no commands were run.
