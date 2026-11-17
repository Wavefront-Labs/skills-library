---
id: computing-software.data-engineering.apache-hadoop.hadoop-metrics-key-names
name: hadoop-metrics-key-names
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, metrics, monitoring, namenode, rpc, percentiles]
level: practitioner
status: docs-checked
description: "Hadoop metrics worth alerting on: NameNode MissingBlocks and UnderReplicatedBlocks, RPC queue and processing times, CallQueueLength, and the RPC and DFS percentile settings."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/Metrics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metrics to watch

The page groups metrics into contexts: jvm, rpc, rpcdetailed, dfs, yarn, ugi, metricssystem, default. Records carry tags such as Hostname (jvm records also ProcessName and SessionID; rpc records the bound port).

NameNode (dfs context):
- `MissingBlocks`: current number of missing blocks
- `UnderReplicatedBlocks`: current number of under-replicated blocks
- `CapacityRemaining`: current remaining capacity in bytes
- `NumLiveDataNodes`: datanodes currently live

RPC context:
- `RpcQueueTimeAvgTime` and `RpcProcessingAvgTime`: average queue and processing time, milliseconds by default (the matching `...NumOps` metrics count calls)
- `CallQueueLength`: current length of the call queue
- `NumOpenConnections`, `numDroppedConnections`
- `RpcAuthenticationFailures` / `Successes`, `RpcAuthorizationFailures` / `Successes`

Settings:
- `rpc.metrics.timeunit`: time unit for RPC metrics (default milliseconds)
- `rpc.metrics.quantile.enable` plus `rpc.metrics.percentiles.intervals`: add `rpcQueueTime<num>s50th...99thPercentileLatency` and `rpcProcessingTime<num>s...` metrics (num is the interval in seconds)
- `dfs.metrics.percentiles.intervals`: percentile metrics for DFS operations; the page says percentile measurement is off by default because no intervals are watched

`FairCallQueueSize_p<Priority>` counts calls in a priority queue of the FairCallQueue. The metricssystem context reports `NumActiveSinks`, `NumAllSinks`, `DroppedPubAll` and per-sink `Sink_<instance>Dropped` and `Sink_<instance>Qsize`.

The page lists metric names and meanings only; it gives no alert thresholds and does not cover sink configuration.

## Checked

Method: 2026-11-08 compared against the Metrics page (apache/hadoop trunk markdown, searched for each name). Names and descriptions match; unsupported alerting advice ("MissingBlocks should be 0", queue length means saturation) and the invented "Verify" step were removed.
