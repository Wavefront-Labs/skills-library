---
id: computing-software.cloud-infrastructure-engineering.google-cloud.memorystore-redis-and-memcached
name: memorystore-redis-and-memcached
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, memorystore, redis, memcached, valkey, memorystore-for-redis-cluster, redis-cluster, standard-tier, basic-tier, read-replicas, redis-auth, in-transit-encryption, maxmemory-policy, eviction, rdb-snapshots, aof-persistence, private-services-access, psc-memorystore, cache-design]
level: practitioner
status: docs-checked
description: "Pick and run Memorystore: Redis standard tier vs Redis Cluster vs Valkey vs Memcached, PSA or PSC networking, AUTH and TLS, eviction, read replicas, maintenance and failover."
sources: ["https://cloud.google.com/memorystore/docs/redis/memorystore-for-redis-overview", "https://cloud.google.com/memorystore/docs/cluster/overview", "https://cloud.google.com/memorystore/docs/valkey/overview", "https://cloud.google.com/memorystore/docs/memcached/overview", "https://cloud.google.com/memorystore/docs/redis/high-availability", "https://cloud.google.com/memorystore/docs/redis/memory-management-best-practices", "https://cloud.google.com/memorystore/docs/redis/persistence"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memorystore for Redis, Valkey and Memcached

**Goal:** a managed cache or in-memory store that fails over without losing the app, never
runs out of memory silently, and is reachable only from the VPC with AUTH and TLS.

## 1. Which product
| Product | Shape | Use |
|---|---|---|
| **Memorystore for Redis** (standard tier) | single primary + replica, up to 5 read replicas, 300 GB, zonal failover | sessions, rate limits, queues under ~100k ops/s |
| Memorystore for Redis (basic tier) | single node, no SLA, data lost on failure | dev only |
| **Memorystore for Redis Cluster** | sharded (OSS cluster protocol), 3-250 shards, multi-zone, zero-downtime scaling, PSC | >100k ops/s or >300 GB, high write throughput |
| **Memorystore for Valkey** | open-source Redis fork, cluster-mode or standalone, PSC, newest features (persistence, cross-region replication) | new deployments — Google's forward path |
| **Memorystore for Memcached** | multi-node, no persistence/replication, client-side hashing | pure cache with simple semantics |
Clients must support **cluster mode** for Redis Cluster/Valkey cluster; standalone-protocol apps need standard tier or Valkey standalone.

## 2. Create (standard tier)
```bash
gcloud redis instances create cache-prod --region=europe-west1 --tier=STANDARD --size=10 \
  --redis-version=redis_7_2 --network=projects/<HOST>/global/networks/prod-vpc \
  --connect-mode=PRIVATE_SERVICE_ACCESS --replica-count=2 --read-replicas-mode=READ_REPLICAS_ENABLED \
  --enable-auth --transit-encryption-mode=SERVER_AUTHENTICATION \
  --redis-config=maxmemory-policy=allkeys-lru,notify-keyspace-events="" \
  --maintenance-window-day=SUNDAY --maintenance-window-hour=3 --persistence-mode=RDB --rdb-snapshot-period=1h
gcloud redis instances get-auth-string cache-prod --region=europe-west1   # store in Secret Manager
```
Redis Cluster / Valkey: `gcloud redis clusters create … --shard-count=3 --replica-count=1 …` with a **service connection policy** (`gcloud network-connectivity service-connection-policies create`) for PSC in the subnet.

## 3. Memory and eviction (the pager)
- `maxmemory-policy`: `allkeys-lru` for caches; `volatile-lru`/`volatile-ttl` when some keys must never be evicted; `noeviction` for queues/locks (writes fail instead of data vanishing). Default `volatile-lru` on Memorystore evicts nothing if keys lack TTLs → OOM.
- `maxmemory-gb` defaults to the full size; set it to ~80 % of instance size to leave room for replication buffers, fragmentation, and the **RDB fork**. Alert on `redis.googleapis.com/stats/memory/usage_ratio` > 0.8 and `system_memory_usage_ratio`.
- Scaling `--size` is online for standard tier but triggers a failover-like blip; replicas resync.
- `activedefrag` yes if fragmentation ratio > 1.5.

## 4. HA, replicas, persistence
- Standard tier failover: replica promoted, same IP, clients see a connection reset (seconds). Test with `gcloud redis instances failover cache-prod --data-protection-mode=limited-data-loss` (or `force-data-loss`).
- **Read replicas** expose a separate read endpoint (`readEndpoint`); replication is async — reads can be stale.
- Persistence: **RDB** snapshots to the instance's storage every 1/6/12/24 h (recovery to last snapshot). AOF on Valkey/Cluster for finer recovery. For "must not lose", Memorystore is still a cache — keep the source of truth elsewhere.
- Export/import to GCS (`gcloud redis instances export gs://B/cache.rdb`) for migrations; import flushes the instance.

## 5. Connectivity and security
- PSA (standard tier) needs an allocated range in the host VPC; Shared VPC service projects need `roles/compute.networkUser` and the Memorystore service agent granted on the host.
- Serverless clients (Cloud Run, Functions) reach it via Direct VPC egress or a Serverless VPC Access connector; GKE pods via VPC-native routing — no extra setup.
- AUTH string + TLS (`SERVER_AUTHENTICATION` = TLS with Google CA; download the CA with `gcloud redis instances describe … serverCaCerts`); rotate AUTH with `update --enable-auth` (new string, old stops working — coordinate).
- No public IP ever; firewall is implicit (any VPC client), so AUTH is the only authn.

## Gotchas
- `KEYS *` and large `SMEMBERS` block the single thread; use `SCAN`. Guard access with AUTH and application discipline.
- Maintenance restarts the primary (standard tier) → a failover; set the window and build reconnect logic.
- Memcached has no auth/TLS at all; VPC reachability is the security boundary.
- Clients that pin the IP across a Redis Cluster resize break; use the discovery endpoint.
- Transit encryption adds latency (~10-20 %); size CPU accordingly.

## Verify
- [ ] `redis-cli --tls --cacert ca.pem -h <IP> -a <AUTH> PING` from a VM returns PONG; without `-a` it returns NOAUTH.
- [ ] `CONFIG GET maxmemory-policy` returns the intended policy; a load test past `maxmemory` evicts rather than errors (for caches).
- [ ] Manual failover: app error burst < 30 s, data present afterwards (limited-data-loss mode).
- [ ] Memory usage ratio alert fires at 80 % in a test.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: the nonexistent --psc-auth-mode flag, the client library and redirect names, and the claim that FLUSHALL cannot be disabled.

Method: documentation only; no commands were run.
