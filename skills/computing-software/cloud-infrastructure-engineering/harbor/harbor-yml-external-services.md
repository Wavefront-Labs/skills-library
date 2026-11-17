---
id: computing-software.cloud-infrastructure-engineering.harbor.harbor-yml-external-services
name: harbor-yml-external-services
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [external-database, external-redis, storage-service, sentinel, harbor-yml]
level: advanced
status: docs-checked
description: "Point Harbor at external PostgreSQL, Redis (including Sentinel) and non-filesystem registry storage via harbor.yml optional parameters."
sources:
  - https://goharbor.io/docs/main/install-config/configure-yml-file/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Optional parameters are commented with `#`; uncomment them by deleting the leading `#`.

- `external_url`: use an external proxy. When enabled, `hostname` is no longer used.
- `storage_service`: by default images and charts live on the local filesystem. The registry backend can be `filesystem` (default), `azure`, `gcs`, `s3`, `swift` or `oss`. `maxthreads` limits threads to the provider, default 100. `ca_bundle` is a custom root CA path injected into the trust store. Backend options follow the Distribution configuration reference; for Swift, set `username`, `password`, `authurl`, `tenant`, `domain`, `region`, `container` under `storage_service.swift`.
- `external_database`: use only if the local `database` option is deactivated. Only PostgreSQL is supported; you must create the database for Harbor core, and tables are created automatically at startup. Under `harbor` give `host`, `port`, `db_name`, `username` and `password`.
- `external_redis`: `host` as `redis_host:redis_port`; with Sentinel use `host_sentinel1:port_sentinel1,host_sentinel2:port_sentinel2` and set `sentinel_master_set`. Also `password`, `registry_db_index` and `jobservice_db_index`.
- `metric`: `enabled`, `port` (default 9090), `path` (default /metrics).
- `trace`: see the distributed tracing skill.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Configure the Harbor YML File.
Method: documentation only; no commands were run.
