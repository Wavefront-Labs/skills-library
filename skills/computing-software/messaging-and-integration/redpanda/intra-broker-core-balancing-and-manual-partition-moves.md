---
id: computing-software.messaging-and-integration.redpanda.intra-broker-core-balancing-and-manual-partition-moves
name: intra-broker-core-balancing-and-manual-partition-moves
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [core-balancing, rebalance-cores, rpk-cluster-partitions-move, shards, partition-assignment]
level: advanced
status: docs-checked
description: "Rebalance partitions across CPU cores inside a broker, and reassign replicas explicitly with rpk cluster partitions move after turning automatic balancing off."
sources:
  - https://docs.redpanda.com/streaming/current/manage/cluster-maintenance/cluster-balancing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Across cores.** Each partition replica is assigned to a CPU core. Topic-aware intra-broker balancing evens a topic's replicas across a broker's cores.

| Property | Meaning |
|---|---|
| `core_balancing_on_core_count_change` | Rebalance after startup if core count changed; default true |
| `core_balancing_continuous` | Rebalance at runtime; needs an enterprise license, and defaults to true with one |

Trigger manually and inspect:
```bash
curl -X POST http://localhost:9644/v1/partitions/rebalance_cores
curl http://localhost:9644/v1/partitions
```
Use the CPU public metrics to decide when it is needed.

**Manual replica moves.** With balancing enabled Redpanda may override you, so first:
```bash
rpk cluster config set partition_autobalancing_mode off
```
Show replica sets with `rpk topic describe test -p`, then move partition 1 from `[0 1 2]` to `[3 1 2]` and partition 2 from `[0 1 3]` to `[2 1 3]`:

```bash
rpk cluster partitions move test -p 1:3,1,2 -p 2:2,1,3
rpk cluster partitions move -p test/1:3,1,2 -p test/2:2,1,3
```

The output lists OLD-REPLICAS and NEW-REPLICAS and says "Successfully began 2 partition movement(s)". Follow progress with `rpk cluster partitions move-status` or `rpk topic describe -p TOPIC`.
## Checked

2026-11-04. The core balancing properties, Admin API calls and the move example and output were confirmed on the Cluster Balancing page. An unsupported closing reminder was removed.

Method: documentation only; no commands were run.
