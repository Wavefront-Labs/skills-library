---
id: computing-software.cloud-infrastructure-engineering.azure.redis-client-timeouts-and-connection-troubleshooting
name: redis-client-timeouts-and-connection-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, redis-cache, redis-timeouts, redis-troubleshooting, stackexchange-redis, connection-multiplexer]
level: advanced
status: docs-checked
description: "Troubleshoot Azure Cache for Redis timeouts and connection drops: StackExchange.Redis error fields, thread pool, server load, bandwidth, failovers."
sources: ["https://learn.microsoft.com/azure/azure-cache-for-redis/cache-troubleshoot-timeouts", "https://learn.microsoft.com/azure/azure-cache-for-redis/cache-troubleshoot-connectivity", "https://learn.microsoft.com/azure/azure-cache-for-redis/cache-best-practices-connection"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redis client timeouts and connection troubleshooting

**Goal:** turn "timeout exception" into a specific cause and fix.

Note: Microsoft has announced a retirement timeline for all Azure Cache for Redis SKUs and recommends moving to Azure Managed Redis. The troubleshooting below is from the current Azure Cache for Redis pages.

## Read the exception
A StackExchange.Redis timeout message looks like `timeout performing EVAL, inst: 8, mgr: Inactive, queue: 0, qu: 0, qs: 0, ... in: 64221 ... IOCP: (Busy=6,Free=999,Min=2,Max=1000), WORKER: (Busy=7,Free=8184,Min=2,Max=8191)`.
- If `Busy` is greater than `Min` in the IOCP or WORKER section, the ThreadPool settings need adjusting so the pool scales up quickly under traffic bursts.
- `in: N` is the number of bytes received by the client kernel socket but not yet read by the application. A large value means the application is not reading as fast as the server sends.
- StackExchange.Redis 1.1.603 and later includes `local-cpu` in the message; use the latest package version.
- The **Errors (Type: UnresponsiveClients)** metric shows whether client hosts keep up with spikes.

## Client-side causes
| Cause | What to do |
|---|---|
| Too many client connections (possible leak) | Check **Max aggregate for Connected Clients** against the limit for the cache size; review code for connections not reused or closed; upgrade the cache if all are legitimate |
| High client CPU | Keep system-wide client CPU under 80%; watch system CPU rather than process CPU; use a larger VM |
| Large key values | Find with `redis-cli --bigkeys`; use more keys with smaller values, more VM bandwidth, or round-robin over multiple connection objects |
| Client memory pressure | Watch the `Page Faults/Sec` counter; reduce usage or use a bigger VM |
| Client network bandwidth | Reduce traffic or use a VM size with more network capacity |
| `RedisSessionStateProvider` | Set `retryTimeoutInMilliseconds` higher than `operationTimeoutInMilliseconds`, otherwise no retries occur |
| Linux TCP defaults | Some Linux defaults can leave connections failing for 13 minutes or more; Microsoft recommends `net.ipv4.tcp_retries2` = 5 |

## Server-side causes
- **High memory**: fragmentation is likely when stored data sizes vary widely; if `used_memory_rss` exceeds 1.5 times `used_memory` there is fragmentation. Set a memory policy and key expirations, configure `maxmemory-reserved` and `maxfragmentationmemory-reserved`, alert on used memory, or scale up.
- **High server load**: watch the **Server Load** metric for spikes matching timeouts. On C0 and C1 caches, internal Defender scanning can cause short load spikes and extra latency because those tiers have one core; scale to C2 or higher if it hurts production. Scale out to more shards or up to more cores (scaling itself is CPU and memory intensive).
- **Long-running commands**: Redis command processing is single-threaded, so one slow command blocks others. Avoid `KEYS` (O(N)) in favour of `SCAN`. Investigate with `CLIENT LIST`, `INFO` (a `server_load` of 100 means never idle), `SLOWLOG GET`, and `MONITOR` (which itself degrades performance).
- **Server bandwidth**: watch the **Cache Read** and **Cache Write** metrics; reduce demand or scale to a larger size.
- **Maintenance and failover**: a failover moves connections to the surviving node and server load can spike; in-flight operations may time out. Check the **Errors** metric split by ErrorType and look for Failover. Use update channel and maintenance-window settings and AzureRedisEvents notifications.

## Connection practices
- Retry commands with exponential backoff.
- Use a connect timeout of about five seconds; very short connect timeouts can create a connect, fail, retry loop. Start with a command timeout under five seconds and adjust for your value sizes.
- With StackExchange.Redis set `abortConnect=false` and let the `ConnectionMultiplexer` reconnect. Use a singleton multiplexer; in rare cases of failed reconnection call `ForceReconnectAsync()` for connection and socket exceptions, and for timeouts only with generous `ReconnectMinInterval` and `ReconnectErrorThreshold`. In ASP.NET with Microsoft.Extensions.Caching.StackExchangeRedis, set `UseForceReconnect`.
- Stagger reconnects across many clients to avoid connection spikes, and close old connections when recreating them.
- Idle connections are closed after 10 minutes; set client keepalive below that or send `PING`.
- Connect to `<cachename>.redis.cache.windows.net` on port 6380 rather than the privatelink name. Firewalls and proxies must allow `*.redis.cache.windows.net` on ports 6379 and 6380, and clustered caches may need more; with a service mesh such as Istio reserve ports 13000-13019 or 15000-15019 for clustered caches.
- Test resiliency by rebooting the cache to simulate a patch.

## Verify
- [ ] Timeout rate drops after the fix and the exception text no longer shows Busy greater than Min.

## Checked
Method: docs-checked 2026-11-09 against cache-troubleshoot-timeouts (read in full), cache-best-practices-connection (read in full) and cache-troubleshoot-connectivity (searched for port and firewall guidance), downloaded with curl as Learn markdown. Dropped the connection-string sample, the 100 KB and 80%/70% thresholds not on these pages, az and redis-cli sample commands, and the cache-troubleshoot-client source (not read).
