---
id: computing-software.collaboration-platform-administration.vikunja.redis-keyvalue-cache
name: redis-keyvalue-cache
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, redis-enabled, keyvalue-storage, redis-host, redis-db]
level: practitioner
status: docs-checked
description: "Enable Redis for Vikunja's key-value storage and rate-limit store, with the redis.* options, defaults and when the docs say you need it."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/full-docker-example.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs say Redis is only worth it with more than a handful of users. Its compose example adds a `redis` service (image `redis`) and these variables on the vikunja service: `VIKUNJA_REDIS_ENABLED: 1`, `VIKUNJA_REDIS_HOST: 'redis:6379'`, `VIKUNJA_CACHE_ENABLED: 1`, `VIKUNJA_CACHE_TYPE: redis`.

The config reference documents these options:
- `redis.enabled` (default false), `redis.host` (default `localhost:6379`, include the port), `redis.password`, `redis.db` (0 is the default database).
- `keyvalue.type`: `memory` (default) or `redis`. The key-value store backs metrics and a few cache systems.
- `ratelimit.store`: `keyvalue` (default, follows the keyvalue section), `memory` or `redis`.

If `redis` is chosen for `keyvalue.type` it needs to be configured separately (the `redis.*` options). The `VIKUNJA_CACHE_*` variables in the compose example do not appear in the config reference (config-raw.json), which has no `cache` section; the reference's key-value setting is `keyvalue.type`.

## Checked

2026-11-04: compose example and the "handful of users" remark checked against the full Docker example page (Redis section); options and defaults against config-raw.json (redis, keyvalue, ratelimit.store). Removed the unsourced "state is per process" remark.

Method: documentation only; no commands were run.
