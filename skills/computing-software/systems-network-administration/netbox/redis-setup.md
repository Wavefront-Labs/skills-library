---
id: computing-software.systems-network-administration.netbox.redis-setup
name: redis-setup
category: computing-software
field: systems-network-administration
product: netbox
tags: [redis, redis-security, tasks-caching]
level: practitioner
status: docs-checked
description: "Install Redis 6.0 or later and treat it as trusted infrastructure."
sources: ["https://netboxlabs.com/docs/netbox/installation/2-redis/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Redis setup

Goal: provide NetBox with caching and queuing.

Redis is an in-memory key-value store NetBox uses for caching and for queuing background jobs.

**Install and verify**
```
sudo apt install -y redis-server
redis-server -v
redis-cli ping
```
The version must be at least v6.0, and `redis-cli ping` should return `PONG`. The configuration may live at `/etc/redis.conf` or `/etc/redis/redis.conf`; in most cases defaults are sufficient.

**Security.** NetBox background workers execute jobs read from Redis, so anyone able to write to the tasks database can run arbitrary code on a worker. Therefore:

- Keep Redis bound to localhost (the default) or a private network.
- Enable authentication if any other host can reach it.

**Two databases.** The `REDIS` setting in `configuration.py` needs separate `tasks` and `caching` entries. They may use the same Redis service but each should have a unique numeric database ID (the example uses `0` for tasks and `1` for caching). Per-entry keys shown: `HOST`, `PORT` (6379), `PASSWORD`, `DATABASE`, `SSL`.

**Checklist**

1. Version at least 6.0.
2. Bound to localhost or private network.
3. Distinct DATABASE ids for tasks and caching.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Redis page: Redis at least v6.0, redis-cli ping, security note about worker code execution, separate tasks/caching database IDs; REDIS keys from the required-parameters page. Removed: Nothing.

Method: documentation only; no commands were run.
