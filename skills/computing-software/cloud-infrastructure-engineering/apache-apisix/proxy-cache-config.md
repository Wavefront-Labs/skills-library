---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.proxy-cache-config
name: proxy-cache-config
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, proxy-cache, caching, cache-zone, cache-key, cache-ttl, plugin]
level: practitioner
status: docs-checked
description: "Cache upstream responses in APISIX with proxy-cache: memory or disk strategy, zones in config.yaml, cache_key, cache_ttl, status codes, bypass rules and Apisix-Cache-Status."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/proxy-cache.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# proxy-cache config

Defaults:
- `cache_strategy`: `disk` (or `memory`); `cache_zone`: `disk_cache_one`, must match the strategy.
- `cache_key`: `["$host","$request_uri"]`; `cache_method`: `["GET","HEAD"]`; `cache_http_status`: `[200,301,404]`.
- `cache_ttl`: 300 seconds (memory only; disk TTL is set in config.yaml).
- `cache_bypass`, `no_cache`: variables; skip retrieval or storage when a value is non-empty and not `0`.
- `consumer_isolation`: true. `hide_cache_headers`: false. `max_resp_body_size`: 67108864.
- `cache_control` and `cache_set_cookie` (both false) apply to the memory strategy only.

Zones in `conf/config.yaml` (reload after changes):

```yaml
apisix:
  proxy_cache:
    cache_ttl: 10s
    zones:
      - name: disk_cache_one
        memory_size: 50m
        disk_size: 1G
        disk_path: /path/to/cache
        cache_levels: 1:2
      - name: memory_cache
        memory_size: 50m
```

Memory example: `"proxy-cache": {"cache_strategy":"memory","cache_zone":"memory_cache","cache_ttl":10}`.

Responses carry `Apisix-Cache-Status`: MISS, HIT, EXPIRED or BYPASS. Upstream `Cache-Control` of private, no-store or no-cache is never cached; `Vary: *` is not cached. The page documents no purge procedure.

## Checked

2026-11-04. Confirmed against the APISIX proxy-cache plugin page: attribute defaults, memory and disk strategies, Apisix-Cache-Status values, Vary and Cache-Control handling, the absence of a purge procedure. Nothing removed.

Method: documentation only; no commands were run.

