---
id: computing-software.cybersecurity-defensive.authelia.session-redis-sentinel-high-availability
name: session-redis-sentinel-high-availability
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, redis-sentinel, high-availability, session-storage, route-by-latency, failover]
level: advanced
status: docs-checked
description: "Configure Authelia sessions against Redis Sentinel with sentinel_name, node list, separate sentinel credentials and routing options."
sources:
  - https://www.authelia.com/configuration/session/redis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Defining `session.redis.high_availability` switches Authelia to Redis Sentinel connections. The documentation notes Redis Cluster might be added in future, but it is not offered today.

```yaml
session:
  redis:
    host: '127.0.0.1'
    port: 6379
    password: '<REDIS_PASSWORD>'
    high_availability:
      sentinel_name: 'mysentinel'
      sentinel_username: 'sentinel_user'
      sentinel_password: '<SENTINEL_PASSWORD>'
      nodes:
        - host: 'sentinel-node1'
          port: 26379
        - host: 'sentinel-node2'
          port: 26379
      route_by_latency: false
      route_randomly: false
```

Notes:

- `sentinel_name` is the master name your Sentinels monitor.
- `sentinel_name` is required and is the master name from your Sentinel configuration, not a hostname.
- `nodes` lists the Sentinel instances (each with `host` and `port`, port defaulting to 26379), not the Redis servers. The list is added to `redis.host`, and you must define either the Redis host or at least one Sentinel node; the `host` must itself be a Sentinel host, not a regular Redis server. Individual Redis hosts are discovered with Sentinel commands.
- If `sentinel_username` is set, Authelia authenticates to Sentinel with ACL credentials; otherwise it uses traditional `requirepass` authentication with `sentinel_password`. `sentinel_password` is marked required and can be a secret; a 64+ character random alphanumeric value is recommended.
- `route_by_latency` prioritises low-latency Sentinel nodes and `route_randomly` picks nodes randomly; both default to false.

The `session.secret` encrypts session data in Redis; the page does not say how replicas should share it, but sessions must be readable by whichever replica serves a request, so use the same secret on all of them.

Check: kill the current Redis master during a test and confirm logged-in users remain logged in after Sentinel promotes a replica.

## Checked

2026-11-08. Read in full: configuration/session/redis. Removed unsupported 'two or more nodes' advice, added that the host must be a Sentinel host, node port default 26379 and required fields.

Method: documentation only; no commands were run.
