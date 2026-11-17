---
id: computing-software.devops-ci-cd.renovate.repository-cache
name: repository-cache
category: computing-software
field: devops-ci-cd
product: renovate
tags: [repository-cache, cache-dir, redis, renovate]
level: advanced
status: docs-checked
description: "Speed up self-hosted runs with repositoryCache, cacheDir, Redis and package cache TTL settings."
sources:
  - https://docs.renovatebot.com/self-hosted-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Self-hosted Renovate can cache work to shorten runs.

- `repositoryCache` (default `disabled`; values `disabled`, `enabled`, `reset`): `enabled` keeps a JSON cache per repository inside `cacheDir`, next to the file-based package cache, to speed up extractions. `reset` bypasses the cache and overwrites it.
- `repositoryCacheType` (default `local`) can be set to an S3 URI such as `s3://bucket-name` for an S3-backed repository cache; Renovate uses the AWS SDK for JavaScript v3, so its authentication methods apply. This caches extracted dependencies, not lookups (use `redisUrl` for those). `repositoryCacheForceLocal` keeps a local copy after uploading to S3. `s3Endpoint` sets the S3 client endpoint and `s3PathStyle` enables `forcePathStyle`.
- `cacheDir` is where Renovate stores its cache; by default a temporary directory such as `/tmp/renovate/cache`.
- `redisUrl` makes Renovate use Redis instead of the local file system for its global cache of lookup results (versions, changelogs) between repositories and runs; `redisPrefix` prefixes the entry names. Use `rediss://` for TLS and `redis+cluster://` for clusters.
- `cacheTtlOverride` (experimental, advanced) maps cache namespaces to soft TTL values in minutes. `cacheHardTtlMinutes` (experimental, default 10080) is how long datasource cache entries are kept; stale data can be used if an upstream request fails until the hard TTL expires.
- `httpCacheTtlDays` is how many days HTTP cache entries are kept (default 90; 0 means no caching and removes the cached data).
- `presetCachePersistence` (default `false`) caches resolved presets in the package cache across repositories; private presets can leak between repositories, so enable it only when all repositories are trusted.

```json
{
  "cacheDir": "/path/to/renovate-cache",
  "repositoryCache": "enabled",
  "redisUrl": "redis://redis.example.com:6379"
}
```

`containerbaseDir` is where downloads are cached when `binarySource` is `docker` or `install`; if empty it is a subdirectory of `cacheDir`. If you ever need to bypass the repository cache, run once with `repositoryCache` set to `reset`.

## Checked

2026-11-09: read the cacheDir, cacheHardTtlMinutes, cacheTtlOverride, containerbaseDir, httpCacheTtlDays, presetCachePersistence, redisPrefix, redisUrl, repositoryCache, repositoryCacheForceLocal, repositoryCacheType, s3Endpoint and s3PathStyle sections of https://docs.renovatebot.com/self-hosted-configuration/. Removed the unsourced claim that persisting `cacheDir` cuts run time more than any other setting and the persistent-volume advice.

Method: documentation only; no commands were run.
