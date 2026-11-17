---
id: computing-software.collaboration-platform-administration.mattermost.redis-cache-setup
name: redis-cache-setup
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [redis, cache-settings, elasticache, scaling]
level: advanced
status: docs-checked
description: "Add Redis as Mattermost's external cache for very large deployments: server setup, CacheSettings, AWS ElastiCache sizing and what to monitor."
sources: ["https://docs.mattermost.com/administration-guide/scale/redis.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Redis as an external cache

Mattermost can use Redis as an external cache to cut database load at scale. It is highly recommended above 100K users and not recommended below that. A useful trigger is the cache invalidation rate, sum(rate(mattermost_cache_mem_invalidation_total[5m])); the docs give an example that with more than 10 cluster nodes and an invalidation rate above 10 you should consider Redis. Run Redis on a separate machine from the Mattermost server in production.

Set up the server: install the latest Redis 7.x, secure it so only trusted systems reach it, and for HA consider a Redis cluster.

Configure Mattermost: System Console > Environment > Cache, set Cache Type to redis, enter Redis Address (for example redis.example.com:6379), optionally Redis Password and Redis Database (default -1, which means Redis's default database), save, and restart Mattermost. The config.json equivalent is the CacheSettings block with CacheType, RedisAddress, RedisPassword, RedisCachePrefix, RedisDB (-1) and DisableClientCache (false).

AWS ElastiCache: create an ElastiCache for Redis instance on Redis OSS 7.1 or later; load testing suggests starting with cache.m7g.2xlarge for over 100,000 users; point Mattermost at the endpoint.

Performance: Redis is single-threaded, so CPU is the bottleneck rather than memory; scale on CPU utilisation. Monitor CPU, memory, connected clients, cache hit ratio, operation latency and Mattermost's mattermost_db_cache_time metric (labels cache_name and operation). Mattermost uses the rueidis client library for automatic pipelining, client-side caching and tuning such as MaxFlushDelay.

## Checked

Confirmed against the Redis page: 100K user guidance, invalidation-rate trigger, Redis 7.x, System Console path and CacheSettings block, ElastiCache sizing, CPU bottleneck, monitored metrics and the rueidis library. Nothing removed.

Method: docs-checked 2026-11-09 against the full administration-guide/scale/redis page (source rst from the mattermost/docs repo).
