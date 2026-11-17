---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.hybrid-sync-behavior
name: hybrid-sync-behavior
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, hybrid-sync, config-cache, incremental-sync, dbless-lmdb, hybrid-mode]
level: advanced
status: docs-checked
description: "How Kong hybrid data planes receive and cache configuration: push on change, dbless.lmdb cache, behaviour when the control plane is down, and recovery steps."
sources:
  - https://developer.konghq.com/gateway/hybrid-mode/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hybrid configuration sync and cache

- The control plane pushes configuration changes to connected data planes immediately.
- Data planes cache the latest configuration on disk in `dbless.lmdb` under `prefix`. The cache is unencrypted by default; it can be encrypted, in which case the DP uses the cluster certificate key to decrypt it at startup.
- While disconnected, a DP keeps serving traffic from its cache and keeps retrying the connection.
- On reconnect, the CP pushes the latest configuration, not a replay of queued older changes.
- Gateway 3.9.x and earlier: every change triggers a full cluster-wide configuration update. 3.10.x and later: incremental config sync sends only changed parts.

Recovery when a DP cannot reach the CP:
1. Remove `dbless.lmdb`.
2. Set `declarative_config` (or `KONG_DECLARATIVE_CONFIG`) to a YAML file holding the full configuration.

Alternatively, copy `config.json.gz` or `dbless.lmdb` from a connected DP to seed a new DP during a CP outage.

A DP with no cache file uses `declarative_config` as a fallback before it first connects.

Konnect telemetry from DPs flushes every second by default (`analytics_flush_interval`); while disconnected they buffer up to 100000 requests (`analytics_buffer_size_limit`) and then drop older data.

## Checked

2026-11-04. Confirmed against the Hybrid mode page: immediate push, `dbless.lmdb` cache and encryption note, behaviour while disconnected and on reconnect, 3.9.x versus 3.10.x sync, recovery steps, `config.json.gz`, declarative_config fallback, the 1 second telemetry interval and 100000 request buffer. Reworded the encryption sentence to match the page.
Method: documentation only; no commands were run.
