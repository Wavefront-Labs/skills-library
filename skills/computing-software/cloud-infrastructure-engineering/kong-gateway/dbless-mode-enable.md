---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.dbless-mode-enable
name: dbless-mode-enable
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, database-off, declarative-config, lmdb, db-less]
level: practitioner
status: docs-checked
description: "Run Kong Gateway without a database: database=off, loading kong.yml via declarative_config or /config, LMDB sizing, and the read-only Admin API behaviour."
sources:
  - https://developer.konghq.com/gateway/db-less-mode/
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enabling DB-less mode

Set `database=off` in `kong.conf` or export `KONG_DATABASE=off`, then start Kong.

Check it with `curl -i -X GET http://localhost:8001`: the response shows `database` as `off`.

Generate a sample file with `kong config init` (creates `kong.yml` in the current directory).

Load configuration one of three ways:
- `declarative_config` = path to the file (startup)
- `declarative_config_string` = inline content (startup)
- the `/config` Admin API endpoint (runtime)

Entities live in an LMDB cache: `lmdb_environment_path` defaults to `dbless.lmdb` (relative to `prefix`) and `lmdb_map_size` to `2048m`. Keep headroom in the map size. All entities must also fit in `mem_cache_size` (default `128m`).

Limits to remember:
- Nodes are independent; a `/config` call changes only the node that receives it, so load each node.
- Entity endpoints reject POST, PATCH, PUT and DELETE with HTTP 405 (GET works).
- decK cannot be used because it needs a database.
- Some plugins need a database and are unsupported.

## Checked

2026-11-04. Confirmed against the DB-less mode page and kong.conf.default: `database=off`/`KONG_DATABASE`, the root GET check, `kong config init`, the load methods, `lmdb_environment_path`, `lmdb_map_size` 2048m, `mem_cache_size` 128m, independent nodes, HTTP 405, decK limitation, plugin compatibility. Nothing removed.
Method: documentation only; no commands were run.
