---
id: computing-software.web-development.directus.config-cache
name: config-cache
category: computing-software
field: web-development
product: directus
tags: [cache-config, cache-ttl, cache-auto-purge, cache-store-redis]
level: practitioner
status: docs-checked
description: "Enable Directus data caching with CACHE_ENABLED, TTL, auto purge and a Redis store, and understand the schema cache and assets cache headers."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/configuration/cache.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Data caching stores request output per user and exact query, and sets accurate cache-control headers for CDNs and browsers.

Key variables (defaults in parentheses):
- `CACHE_ENABLED` (false)
- `CACHE_TTL` (`5m`; human values like `2 days`, `7 hrs`)
- `CACHE_AUTO_PURGE` (false): purge the data cache on data-changing actions, keeping the API real-time
- `CACHE_AUTO_PURGE_IGNORE_LIST` (`directus_activity,directus_presets`): changes to these collections do not purge; clear the cache manually when you need fresh results
- `CACHE_STORE` (`memory`): use `redis` for larger projects
- `CACHE_NAMESPACE` (`system-cache`), `CACHE_STATUS_HEADER` (set a header name to return HIT or MISS)
- `CACHE_VALUE_MAX_SIZE` (false), `CACHE_SKIP_ALLOWED` (false; lets `Cache-Control: no-store` skip caching)
- `CACHE_CONTROL_S_MAXAGE` (0)
- `CACHE_SCHEMA` (true), `CACHE_SYSTEM_TTL`: internal schema cache, unaffected by `CACHE_ENABLED`

Settings marked with superscript 5 in the docs (`CACHE_SYSTEM_TTL`, `CACHE_NAMESPACE`, `CACHE_STORE`) may still be used by the caching system when `CACHE_ENABLED` is off; this cannot be turned off.

Assets: `Cache-Control` and `Last-Modified` for `/assets` are separate from the data cache (`Last-Modified` comes from `modified_on`).

## Checked

2026-11-04: defaults, TTL parsing, purge ignore list, store options, status header values and assets note confirmed against the Directus cache configuration page. Removed an unsupported "Verify" line.

Method: documentation only; no commands were run.
