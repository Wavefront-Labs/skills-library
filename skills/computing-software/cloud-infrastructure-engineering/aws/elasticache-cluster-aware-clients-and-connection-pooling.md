---
id: computing-software.cloud-infrastructure-engineering.aws.elasticache-cluster-aware-clients-and-connection-pooling
name: elasticache-cluster-aware-clients-and-connection-pooling
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elasticache, cluster-client, connection-pooling-redis, valkey, client-configuration]
level: advanced
status: docs-checked
description: "Configure Valkey/Redis OSS clients for ElastiCache cluster mode: slot redirects, topology refresh, replica reads, hash tags, connection reuse and DNS caching."
sources: ["https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/BestPractices.Clients.redis.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/BestPractices.Clients-lettuce.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster-aware clients and connection pooling

## 1. Cluster mode enabled needs a cluster client
Connect to the **configuration endpoint**; the client discovers the topology with the `CLUSTER SLOTS`, `CLUSTER SHARDS`
and `CLUSTER NODES` commands (the IP Discovery setting controls whether they return IPv4 or IPv6 addresses) and
follows `MOVED`/`ASK` redirects. A plain client against one node works until a key lives on another shard.
- Python: `redis.cluster.RedisCluster(host=cfg_endpoint, port=6379)` as in the User Guide's redis-py example (add
  `ssl=True` when in-transit encryption is enabled; valkey-py has the same shape).
- Java Lettuce (the User Guide recommends `enablePeriodicRefresh`, default refresh period 60 s, and
  `enableAllAdaptiveRefreshTriggers`, which refresh on `MOVED_REDIRECT`, `ASK_REDIRECT`, `PERSISTENT_RECONNECTS`,
  `UNCOVERED_SLOT` and `UNKNOWN_NODE`; for cluster mode enabled it suggests at least 3 shards with at least 1 replica
  each for fast failover):
```java
// Lettuce API sketch: check method names against your Lettuce version
ClusterTopologyRefreshOptions topo = ClusterTopologyRefreshOptions.builder()
    .enablePeriodicRefresh(Duration.ofSeconds(60))
    .enableAllAdaptiveRefreshTriggers().build();
client.setOptions(ClusterClientOptions.builder().topologyRefreshOptions(topo)
    .socketOptions(SocketOptions.builder().connectTimeout(Duration.ofMillis(500)).build()).build());
```
Topology refresh is what makes failovers and resharding transparent.

## 2. Multi-key operations
Keys in one `MGET`, transaction or Lua script must hash to one slot: use hash tags, `{user:42}:cart` and
`{user:42}:profile`.

## 3. Replica reads
Enable `READONLY` (it enables read-only queries on a replica connection) through your client's read-from-replica
option for read-heavy, staleness-tolerant data.

## 4. Connections
- Create clients once and reuse (Lambda: outside the handler). New TLS connections are expensive;
  bursts of `NewConnections` raise CPU and latency.
- Pool sizes: enough for concurrency, not hundreds per process; watch `CurrConnections` and `RejectedConnections`
  (connections rejected when `maxclients` is reached).
- Short DNS caching for failover: the User Guide recommends a JVM DNS TTL of 5 to 10 seconds
  (`networkaddress.cache.ttl`) because ElastiCache DNS entries can change.
- Timeouts plus retries with backoff; circuit-break the cache rather than piling on during incidents.

## Verify
- [ ] Failover test (`test-failover`) causes only brief errors and the client resumes without restart.
- [ ] `NewConnections` steady, not proportional to request rate.

## Checked
Date: 2026-10-27. Sources: ElastiCache User Guide pages BestPractices.Clients.redis (topology commands, IP Discovery,
redis-py example, Lettuce client link) and BestPractices.Clients-lettuce (Lettuce refresh options and defaults,
JVM DNS TTL 5 to 10 s, shard/replica advice); CacheMetrics.Redis (`RejectedConnections`, `NewConnections`); botocore
`elasticache` model (`TestFailover`). Corrected the JVM TTL (5 to 10 s) and removed the 65,000 connection limit
(not found in the documentation read). Hash tags (all keys in one operation must hash to the same slot) confirmed on
the Valkey cluster specification page (valkey.io/topics/cluster-spec) and `READONLY` (enables read-only queries on a replica)
on the Redis command reference (redis.io/docs/latest/commands/readonly). The Lettuce code is a sketch of the documented option names.
Method: documentation only; no commands were run.
