---
id: computing-software.cloud-infrastructure-engineering.aws.elasticache-memcached-auto-discovery
name: elasticache-memcached-auto-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elasticache, auto-discovery, memcached, consistent-hashing]
level: advanced
status: docs-checked
description: "Use ElastiCache for Memcached auto discovery: the configuration endpoint, config get cluster, cluster clients and consistent hashing so node changes need no redeploy."
sources: ["https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/AutoDiscovery.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/AutoDiscovery.HowAutoDiscoveryWorks.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memcached auto discovery

## 1. Configuration endpoint
A node-based Memcached cluster has a configuration endpoint (shown in the console and in `describe-cache-clusters`
with `--show-cache-node-info`) whose DNS name resolves to one of the nodes; any node can return the node list.
```bash
echo "config get cluster" | nc <CONFIG_ENDPOINT> 11211
# CONFIG cluster 0 136
# 12
# myCluster.pc4ldq.0001.use1.cache.amazonaws.com|10.82.235.120|11211 myCluster.pc4ldq.0002.use1.cache.amazonaws.com|10.80.249.27|11211
# END
```
(The output above is the User Guide's example payload: the second line, here 12, is the config version, then a list of
`hostname|ip-address|port` groups separated by spaces.)
The second line is the config version, which increases by one each time a node is added or removed. `config get cluster`
needs cache engine 1.4.14 or higher (older versions use the `get AmazonElastiCache:cluster` form). Auto Discovery is
available for Memcached only, not Valkey or Redis OSS.

## 2. Clients
- The ElastiCache Cluster Client (available for Java, PHP and .NET) resolves the configuration endpoint, asks a node for
  the node list, connects to all nodes and refreshes the list once per minute (adjustable). The client hashes each key
  to pick the node.
- Use a client-side hashing scheme that tolerates membership changes (for example consistent hashing in your client library)
  so adding or removing a node remaps only part of the keyspace; check your client's documentation.
- Clients without auto discovery need the node list in config and a redeploy on every scaling change.
- With a dual-stack network type, Auto Discovery returns only IPv4 or IPv6 addresses, depending on your selection.

## 3. Scaling
```bash
aws elasticache modify-cache-cluster --cache-cluster-id my-cache --num-cache-nodes 6 \
  --az-mode cross-az --new-availability-zones <AZ_A> <AZ_B> --apply-immediately
```
`--az-mode` accepts `single-az` or `cross-az`; `--new-availability-zones` names the AZs for added nodes. Always take node
endpoints from the configuration endpoint, because cluster metadata is updated on all nodes at the same time.

## 4. Serverless Memcached
Serverless Memcached caches are managed differently and have no node list to discover; see the ElastiCache
serverless documentation for connection details.

## Verify
- [ ] After adding a node, the client logs a config version change and `GetHits` recovers within the expected warm-up.

## Checked
Date: 2026-10-27. Sources: ElastiCache User Guide pages AutoDiscovery, AutoDiscovery.HowAutoDiscoveryWorks (once-per-minute
refresh), AutoDiscovery.AddingToYourClientLibrary (`config get cluster`, output format, engine version 1.4.14),
AutoDiscovery.Using (client languages); botocore `elasticache` model (ModifyCacheCluster `AZMode`,
`NewAvailabilityZones`, `NumCacheNodes`). Corrected: `--preferred-availability-zones` belongs to cluster creation,
modify uses `--az-mode` and `--new-availability-zones`; removed the ketama and 1/N claims, treated as client-library
specific. The `describe-cache-clusters --show-cache-node-info` flag is from the API model (`ShowCacheNodeInfo`), the output format is from the User Guide output format section.
Method: documentation only; no commands were run.
