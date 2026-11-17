---
id: computing-software.search-and-information-retrieval.qdrant.distributed-setup
name: distributed-setup
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [cluster, distributed, raft, bootstrap, cluster-setup]
level: advanced
status: docs-checked
description: "Start a Qdrant cluster by enabling cluster mode, bootstrapping peers on port 6335 and creating replicated collections."
sources:
  - "https://qdrant.tech/documentation/scaling/distributed_deployment/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Enable cluster mode with the setting or the environment variable:

```bash
QDRANT__CLUSTER__ENABLED=true
```

Start the first peer with its own URI, and every other peer pointing at it:

```bash
./qdrant --uri 'http://qdrant_node_1:6335'
./qdrant --bootstrap 'http://qdrant_node_1:6335'
```

Facts from the docs:

- Peers talk on the internal port 6335. Keep it isolated from clients; from v1.20.0 the API key is enforced on it by default through `enforce_internal_auth`.
- The Raft consensus protocol keeps the cluster topology and collection structure consistent across nodes.
- `shard_number` defaults to the number of nodes. It cannot be changed after creation, and should be a multiple of the node count; the docs recommend at least 2 shards per node. Resharding is a Cloud feature.
- A new node joins empty; data does not move to it automatically. Create a replicated collection with `replication_factor` of 2 or more and a shard number that is a multiple of the node count.

```http
PUT /collections/{collection_name}
{ "vectors": { "size": 300, "distance": "Cosine" },
  "shard_number": 6, "replication_factor": 2 }
```

## Checked

2026-11-03. Confirmed on the Qdrant distributed deployment page: cluster mode, `--uri` and `--bootstrap` commands, internal port 6335 and its isolation, v1.20.0 enforcement, Raft, `shard_number` default and immutability, multiple-of-nodes rule, at least 2 shards per node, resharding on Cloud only, empty new nodes. Removed the unconfirmed 'at least three nodes' advice.

Method: documentation only; no commands were run.
