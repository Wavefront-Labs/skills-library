---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.running-multiple-grafana-instances
name: running-multiple-grafana-instances
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-multi-instance, grafana-remote-cache, grafana-ha, alerting-ha-peers, grafana-database-config]
level: advanced
status: docs-checked
description: "Run Grafana with several replicas: shared Postgres/MySQL, remote cache, alerting HA peers or Redis, single-node evaluation, Live HA engine, image renderer."
sources: ["https://grafana.com/docs/grafana/latest/setup-grafana/set-up-for-high-availability/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/#remote_cache", "https://grafana.com/docs/grafana/latest/alerting/set-up/configure-high-availability/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running multiple Grafana instances

## Architecture
Two or more Grafana servers behind a load balancing reverse proxy, active-active. The load balancer needs a listener on a shared cluster hostname. SSL termination at the load balancer is recommended. Sessions live in the shared database, so no session affinity is needed.

## Requirements
- Shared database: PostgreSQL or MySQL, not the default embedded SQLite (which is not recommended for production). Make the database itself highly available; that is out of scope of the Grafana guide.
```ini
[database]
type = postgres
host = pg.example.com:5432
name = grafana
user = grafana
ssl_mode = require
```
`ssl_mode` for Postgres takes any libpq sslmode (`disable`, `require`, `verify-full`...); for MySQL `true`, `false` or `skip-verify`. A `url` setting (`type://user:password@host:port/name`) is an alternative to the separate fields.
- Remote cache (optional): caches authentication tokens and other temporary auth data. `type` is `redis`, `memcached` or `database` (default `database`). It does NOT control user sessions, which are always in the main database.
```ini
[remote_cache]
type = redis
connstr = addr=redis:6379,pool_size=100,db=0,ssl=false
```
- Grafana Enterprise: license token in the name of the cluster's shared hostname, and set `root_url` on each node to that hostname.

## Alerting HA
Every instance evaluates all alert rules by default, so data-source query load is multiplied by the instance count and the duplication shows in state history. Alertmanagers gossip to avoid duplicate notifications (best effort: duplicates or out-of-order notifications are preferred over none) and also replicate silences. Notifications and silences are persisted to the database periodically and on graceful shutdown.

Memberlist (preferred); gossip uses TCP and UDP port 9094:
```ini
[unified_alerting]
ha_peers = grafana-alerting.grafana:9094
ha_listen_address = ${POD_IP}:9094
ha_advertise_address = ${POD_IP}:9094
ha_peer_timeout = 15s
```
- `ha_peers` needs at least one instance; `ha_advertise_address` is optional and for NAT such as Kubernetes services; `ha_peer_timeout` defaults to 15s.
- On Kubernetes expose the pod IP as `POD_IP` via the downward API, open 9094 for TCP and UDP, and use a headless service so `ha_peers` resolves to pod IPs.
- Redis alternative (use only if TCP/UDP between servers is blocked): `ha_redis_address`, with optional `ha_redis_cluster_mode_enabled`, `ha_redis_sentinel_mode_enabled`, `ha_redis_prefix`, credentials and TLS fields; Redis needs pub/sub support.
- `ha_single_node_evaluation = true` makes one primary evaluate rules (requires Memberlist or Redis HA); expect a brief evaluation gap on failover.
- To avoid duplicate notifications entirely, use a shared external Alertmanager.
- Check `grafana_alertmanager_cluster_members` and `grafana_alertmanager_peer_position` (prefixed `grafana_` from Grafana v12.4). They are on `/metrics` and must be scraped.

## Grafana Live and rendering
- Live HA is experimental: `[live] ha_engine = redis` (the only value) and `ha_engine_address` (host:port or a redis:// or rediss:// URL).
- Image rendering: run the renderer as a separate service with `[rendering] server_url`; set `callback_url` when it runs on another server.

## Checked
2026-11-08. Confirmed in the Grafana HA setup page, the alerting Configure high availability page and the configuration reference ([database], [remote_cache], [rendering], [live]). Removed: the claim that the remote cache stores sessions (the docs say it does not), `/api/health`, provisioning rollout advice, the "rule evaluation multiplies state history writes" detail beyond what the page states, `$__file` database password example, the Verify checklist.
Method: documentation only; no commands were run.
