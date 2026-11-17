---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-cache-sessions-redis-memcached
name: bookstack-cache-sessions-redis-memcached
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, cache-driver, session-driver, redis, memcached, session-lifetime, session-cookie]
level: practitioner
status: docs-checked
description: "Move BookStack cache and sessions to database, Memcached or Redis with CACHE_DRIVER and SESSION_DRIVER, server string formats, and session lifetime and cookie settings."
sources: ["https://www.bookstackapp.com/docs/admin/cache-session-config/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack cache and sessions

By default cache and sessions use the filesystem under `storage/framework`. Set `CACHE_DRIVER` and `SESSION_DRIVER` to `database`, `memcached` or `redis` to change them.

Memcached: `MEMCACHED_SERVERS=HOST:PORT:WEIGHT`, comma-separated, weight splits traffic.
```
MEMCACHED_SERVERS=127.0.0.1:11211:100
MEMCACHED_SERVERS=8.8.8.8:11211:50,8.8.4.4:11211:50
```

Redis: `REDIS_SERVERS=HOST:PORT:DATABASE`, optionally `:PASSWORD`; default per host `127.0.0.1:6379:0`. Several servers are clustered by client-side sharding, which pools memory but gives no failover.

Sessions: `SESSION_LIFETIME` in minutes (default 120), `SESSION_COOKIE_NAME` (default `bookstack_session`), `SESSION_SECURE_COOKIE=true` to send cookies over HTTPS only (default false; use only when served over HTTPS).

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) admin/cache-session-config/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: a closing tip about shared drivers behind a load balancer.
Method: documentation only; no commands were run.
