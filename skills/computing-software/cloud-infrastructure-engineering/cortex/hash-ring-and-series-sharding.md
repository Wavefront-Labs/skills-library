---
id: computing-software.cloud-infrastructure-engineering.cortex.hash-ring-and-series-sharding
name: hash-ring-and-series-sharding
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [hash-ring, consistent-hashing, tokens, replication-factor, kv-store]
level: advanced
status: docs-checked
description: "Understand how Cortex shards series across ingesters with consistent hashing, tokens and the replication factor."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Distributors use consistent hashing plus a replication factor to choose which ingesters receive a series. Two hashing strategies exist:

1. Hash the metric name and tenant ID (default).
2. Hash the metric name, labels and tenant ID, enabled with `-distributor.shard-by-all-labels=true`. Writes are better balanced across ingesters, but each query must contact all ingesters because a metric's series may be spread over any of them.

The hash ring lives in a KV store. Every ingester registers with a set of tokens, each a random unsigned 32-bit number. A distributor hashes the series and finds the smallest token larger than the hash; that token's ingester gets the series. With replication factor above 1, the next tokens clockwise that belong to different ingesters are added. Each token therefore owns a hash range: with tokens 0, 25 and 50, a hash of 3 goes to the owner of 25, which covers the range 1-25.

Supported KV stores for the ring are Consul, Etcd and gossip memberlist.

## Checked

Method: docs-checked 2026-11-09 against the Cortex architecture page (raw markdown, read in full). A claim that other components reuse the ring when sharding is enabled was dropped as not on this page.
