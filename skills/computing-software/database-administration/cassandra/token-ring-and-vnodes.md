---
id: computing-software.database-administration.cassandra.token-ring-and-vnodes
name: token-ring-and-vnodes
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, token-ring-vnodes, vnodes, murmur3, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Token ownership, num_tokens and the Murmur3 partitioner"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Token ring, partitioner and vnodes

Goal: reason about which node owns which data.
- Murmur3Partitioner hashes the partition key to a token in -2^63..2^63-1; replicas are the range owner plus the next RF-1 distinct nodes per the replication strategy.
- `num_tokens` (shipped `cassandra.yaml` sets 16; see `allocate_tokens_for_local_replication_factor`) trades streaming parallelism against repair cost.
- `nodetool ring`, `nodetool describering <ks>`, and `nodetool getreplicas` (`getendpoints` is deprecated) show ownership.
- The partitioner and num_tokens cannot change on a live cluster; add a new DC and decommission the old.
Verify: `getreplicas` returns RF endpoints.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: num_tokens: 16, Murmur3Partitioner, describering and ring commands (cassandra.yaml, nodetool sources, FAQ).
Removed: the older-default-256 claim; getendpoints replaced (deprecated in nodetool source).
Method: documentation only; no commands were run.
