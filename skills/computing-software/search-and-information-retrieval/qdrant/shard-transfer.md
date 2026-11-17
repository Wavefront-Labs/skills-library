---
id: computing-software.search-and-information-retrieval.qdrant.shard-transfer
name: shard-transfer
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [shard-transfer, replicas, listener, wal-delta]
level: advanced
status: docs-checked
description: "Move or copy Qdrant shards between peers with stream_records, snapshot or wal_delta, remove a peer, and run a Listener node."
sources:
  - https://qdrant.tech/documentation/scaling/distributed_deployment/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Shards can be moved or replicated between peers with the cluster API.

```http
POST /collections/{collection_name}/cluster
{ "move_shard": { "shard_id": 0, "from_peer_id": 1, "to_peer_id": 2,
                  "method": "snapshot" } }
```

Transfer methods (the `method` field; available as of v1.7.0):

- `stream_records` is the default. It streams the shard's records to the target in batches. Index and quantization data do not transfer, so the target re-indexes and re-quantizes, and update ordering is weak. It is simple and robust, the safest choice on an unstable or resource-starved cluster.
- `snapshot` creates a snapshot automatically, transfers and restores it, then removes it from both nodes. HNSW index and quantization data transfer, so the shard is ready immediately; ordering can be strong. It needs extra disk on both nodes and uses the REST port (6333) as well as the internal gRPC port (6335).
- `wal_delta` transfers only the operations the target missed, resolved from the WALs of both shards. It only works for a shard that already exists on the target, and the WAL normally holds no more than 64MB of recent operations, so it suits a node that restarted quickly. If the delta cannot be resolved it falls back to `stream_records`. Since Qdrant 1.9.0 it is used for automatic replication that recovers dead shards.

Related items:

- Without `method`, the move or replicate request uses the default method (`stream_records`).
- `replicate_shard` (same fields) adds a replica instead of moving; `drop_replica` with `shard_id` and `peer_id` removes one. A collection must keep at least one active replica of each shard.
- After a move completes, the old shard is deleted from the source node.
- To downscale, move all shards off a peer, then call `DELETE /cluster/peer/{peer_id}`; the node is excluded from consensus and can be shut down.
- On Qdrant Cloud, automatic rebalancing can undo a manual move that leaves shard count or size outside the balance target; disable it first. Self-hosted clusters rebalance manually. Changing `replication_factor` on an existing self-hosted collection does nothing by itself: create or drop replicas manually.
- A Listener node (`node_type: "Listener"` under `storage:` in the config) accepts writes but does not take part in search. Its shards are in the Listener state and its writes are processed with `wait=false`. It is experimental. Uses: a backup or long-term store, or syncing data to another region.
- Cluster port 6335 must be reachable between peers and isolated from outside access.

## Checked

2026-11-08. Confirmed against the Distributed Deployment page: move_shard and replicate_shard, drop_replica, the three transfer methods and their comparison table, WAL 64MB, fallback to stream_records, 1.9.0 wal_delta recovery, remove-peer API, Listener mode and config key, port 6335. Page read in full. Removed unconfirmed claims: per-node concurrency limit of 1, a `force` option on remove-peer, and "no recovery in clusters under 3 nodes".
Method: documentation only; no commands were run.
