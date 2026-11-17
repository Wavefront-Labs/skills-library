---
id: computing-software.database-administration.redis.loading-redis-modules
name: loading-redis-modules
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, redis-modules, module-load, loadmodule, redis-programmability, redis-stack]
level: practitioner
status: docs-checked
description: "Load and manage Redis modules with loadmodule and MODULE LOAD/LOADEX, check versions, handle persistence and replication requirements, and avoid unsafe modules."
sources:
  - https://redis.io/docs/latest/develop/reference/modules/
  - https://redis.io/docs/latest/commands/module-load/
  - https://redis.io/docs/latest/commands/module-loadex/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loading modules

**Goal:** add capabilities (search, JSON, time series, Bloom in pre-8 Redis; third-party modules) safely and consistently across a deployment.

## Load at startup (preferred)
```text
# redis.conf
loadmodule /opt/redis/modules/redisearch.so
loadmodule /opt/redis/modules/rejson.so
```
Load the same modules (and compatible versions) on every primary **and** replica so that module data types in RDB/AOF files can be loaded and replicated.

## Load at runtime
```text
MODULE LOAD /opt/redis/modules/redistimeseries.so
MODULE LOADEX /opt/redis/modules/x.so CONFIG x.maxsize 100 ARGS foo   # 7.0+
MODULE LIST                      # name, ver, path, args
MODULE UNLOAD timeseries         # name as shown by MODULE LIST; modules that define data types cannot be unloaded
```
From 7.0 redis.conf has `enable-module-command no|yes|local`; `MODULE` commands are blocked by default (`local` allows local connections only).

## Redis 8 note
Search, JSON, time series and probabilistic types are bundled into Redis Open Source 8; separate module files are no longer needed there. Check `MODULE LIST` before adding them again.

## Safety
- A module runs inside the server process: a crash or memory bug takes down Redis. Load only maintained, version-matched builds.
- Managed services may restrict which modules you can load; check before designing around one.
- Upgrades: upgrade module and server together and test RDB compatibility on a copy.

## Verify
`MODULE LIST` shows identical names/versions on all nodes and a restart loads the dataset without errors.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed: MODULE LOADEX since 7.0 with optional repeated `CONFIG name value` and `ARGS` blocks; MODULE UNLOAD takes the module name from MODULE LIST and cannot unload modules that define their own data types; `enable-module-command` (no, yes, local) is in the 7.0 redis.conf and these commands are blocked by default; Redis 8 builds all previously modular functionality into Redis Open Source. Removed unconfirmed: module arguments in the loadmodule example, the Unknown RDB module type error, the unload-only-without-keys rule, managed-service statements.
Method: documentation only; no commands were run.
