---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mod-cache-disk-and-socache
name: mod-cache-disk-and-socache
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-cache, cacheenable, cachequickhandler, htcacheclean, socache, mod-file-cache]
level: advanced
status: docs-checked
description: "Run an HTTP cache with mod_cache: CacheEnable disk or socache, CacheQuickHandler security effects, freshness defaults, htcacheclean and mod_file_cache."
sources:
  - https://httpd.apache.org/docs/2.4/caching.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_cache with disk and socache
```apache
CacheRoot   "/var/cache/apache/"
CacheEnable disk /
CacheDirLevels 2
CacheDirLength 1
```
```apache
CacheEnable socache /
CacheSocache shmcb:/path/to/datafile(512000)
```
Other socache providers: `memcache:host:11211,...` and `dbm:/path`. `CacheDisable` excludes URLs; exclude IP-gated content because cached entries are not re-authorised.

## CacheQuickHandler
`On` (default): runs early like a front reverse proxy, bypassing authentication and authorisation; requests with `Authorization` are neither cached nor served. `Off`: runs in the normal handler phase.

## mod_cache_disk
Each URL hashes to 22 characters split by `CacheDirLevels`/`CacheDirLength`; entries use `.header`, `.data` and `.vary`. Disk use is not limited; use `htcacheclean` as a daemon or from cron (large caches can take an hour or more, avoid overlap, use `nice`, leave grow room).

## Freshness
The origin sets freshness with `Cache-Control` `max-age`/`s-maxage` or `Expires`. A client request `Cache-Control` can override it; the lowest of request and response wins. With none, the default is one hour (`CacheDefaultExpire`). `CacheLastModifiedFactor` sets a heuristic from `Last-Modified`; `CacheMaxExpire` caps the lifetime. Stale entries revalidate with `If-None-Match` or `If-Modified-Since`; a 304 marks the entry fresh again.

## mod_file_cache
`CacheFile` opens files and `MMapFile` maps them at startup; later changes are not picked up and each child replicates mapped memory. Operating systems usually cache file data well already.

## Checked
2026-11-04. Confirmed against the Caching Guide: CacheEnable disk and socache examples, memcache and dbm providers, CacheQuickHandler phases and security effect, Authorization header rule, 22-character hash and file names, htcacheclean advice, freshness rules, CacheFile and MMapFile behaviour. Corrected the lowest-value rule (it applies between request and response, not Cache-Control versus Expires). Removed the claim that file caching "often suffices" in favour of the page's wording.
Method: documentation only; no commands were run.
