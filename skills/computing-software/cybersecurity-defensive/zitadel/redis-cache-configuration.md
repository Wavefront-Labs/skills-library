---
id: computing-software.cybersecurity-defensive.zitadel.redis-cache-configuration
name: redis-cache-configuration
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, cache, redis, performance, connectors]
level: advanced
status: docs-checked
description: "Enable ZITADEL's experimental object caches, choose a connector, and understand Redis limits and auto prune."
sources:
  - https://zitadel.com/docs/self-hosting/manage/cache
  - https://zitadel.com/docs/self-hosting/manage/requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZITADEL can cache frequently needed objects. Unlike an HTTP cache between ZITADEL and applications, its built-in cache is actively invalidated when an object changes. The documentation labels it an experimental beta feature.

Structure under `Caches`: connectors are defined once and objects choose one.

```yaml
Caches:
  Connectors:
    SomeConnector:
      Enabled: true
  SomeObject:
    Connector: "SomeConnector"
    MaxAge: 1h
    LastUsage: 10m
```

When an object cache has no connector, nothing is cached; that is the default. A connector must be enabled to be used.

Auto prune: connectors without built-in expiry take an `AutoPrune` option with `Interval` and `TimeOut`. It scans and removes expired or invalidated objects, which costs resources.

Redis: supported in simple (standalone) mode only; Cluster and Sentinel are not supported yet. A circuit breaker prevents a single point of failure if Redis becomes unavailable. Benefits are a central cache, consistent invalidation, speed at low network latency and built-in expiry without a pruner. Costs are running Redis, and cross-region round trips that can cancel the benefit. Provide the connection with a URL.

Start with one object cache and measure.

## Checked

2026-11-08. Read in full: the caches page and the requirements page. The caches page says simple mode and the requirements page says standalone mode for Redis; both are stated.

Method: documentation only; no commands were run.
