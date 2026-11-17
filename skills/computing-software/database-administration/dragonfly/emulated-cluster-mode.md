---
id: computing-software.database-administration.dragonfly.emulated-cluster-mode
name: emulated-cluster-mode
category: computing-software
field: database-administration
product: dragonfly
tags: [emulated-cluster, cluster-mode, redis-cluster-migration, cluster-announce-ip, dragonfly]
level: practitioner
status: docs-checked
description: "Run one Dragonfly node as an emulated single-shard Redis Cluster so cluster-aware clients work, which helps migrating off Redis Cluster."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/cluster-mode.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/migrating-to-dragonfly/02-from-redis-cluster/00-redis-cluster-to-dragonfly-single-node.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A single Dragonfly instance can usually match the capacity (memory size and QPS) of a multi-node Redis Cluster. To ease migration, it can emulate a cluster:

```bash
dragonfly --cluster_mode=emulated
redis-cli
dragonfly> CLUSTER HELP
```

A cluster-aware client then works, for example `redis.RedisCluster(host='localhost', port=6379)` in redis-py.

Notes from the docs:

- Regular Redis clients that do not use cluster commands also work.
- If `--cluster_mode` is not given, Dragonfly runs in this emulated mode by default.
- In emulated mode `cluster_announce_ip` and `announce_port` can be changed at runtime with `CONFIG SET`; later topology replies use the new values.
- `--lock_on_hashtags` should only be used with `--cluster_mode=emulated|yes`.

The official migration page for Redis Cluster to a single node is a placeholder saying it will be updated soon, and points to a blog post, "Migrating from a Redis Cluster to Dragonfly on a Single Node".

## Checked

2026-11-04. Confirmed in the Cluster Mode page (emulated section and notes), the flags page (`lock_on_hashtags`) and the placeholder migration page. Nothing removed.

Method: documentation only; no commands were run.
