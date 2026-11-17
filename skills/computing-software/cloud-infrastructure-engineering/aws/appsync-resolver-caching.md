---
id: computing-software.cloud-infrastructure-engineering.aws.appsync-resolver-caching
name: appsync-resolver-caching
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, appsync, graphql, appsync-caching, resolver-cache, per-resolver-caching, full-request-caching, caching-keys, cache-eviction, evictfromapicache, flush-api-cache, cache-ttl]
level: practitioner
status: docs-checked
description: "Cache AppSync GraphQL resolvers: full-request vs per-resolver caching, identity-safe caching keys, TTLs, eviction on mutations, encryption and hit-rate metrics."
sources: ["https://docs.aws.amazon.com/appsync/latest/devguide/enabling-caching.html", "https://docs.aws.amazon.com/appsync/latest/devguide/extensions.html", "https://docs.aws.amazon.com/appsync/latest/devguide/monitoring.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AppSync resolver caching

**Goal:** hot, read-mostly fields (product catalogue, config, profile lookups) are served
from AppSync's managed cache in single-digit ms, without leaking one user's data to another
and without stale data after a mutation.

## 1. Create the cache
```bash
aws appsync create-api-cache --api-id <API_ID> --ttl 300 \
  --api-caching-behavior PER_RESOLVER_CACHING --type LARGE
aws appsync get-api-cache --api-id <API_ID>          # status AVAILABLE
```
- `FULL_REQUEST_CACHING`: every resolver invoked in a request is cached separately, keyed by
  the contents of `context.arguments` and `context.identity`, with one TTL for all.
- `PER_RESOLVER_CACHING`: each resolver opts in with its own TTL (mandatory) and optional
  caching keys. Default to this. With a TTL and no keys it behaves like full request caching.
- `OPERATION_LEVEL_CACHING`: whole successful query responses are cached (maximum cacheable
  response 15 MB); the key combines the query string, operation name, variables, identity and
  request headers (some reserved headers excluded), so it varies per caller.
- The maximum TTL is 3,600 seconds. The cache is hosted ElastiCache (Redis OSS) in your account and
  Region; instance types are `SMALL` through `LARGE_12X` (the older `T2_*` and `R4_*` names are
  deprecated).
- Encryption at rest and in transit is always on for new caches and cannot be disabled; to
  turn it on for an existing cache, delete and recreate the cache.

## 2. Configure a resolver
```bash
aws appsync update-resolver --api-id <API_ID> --type-name Query --field-name getProduct \
  --data-source-name ProductsTable --runtime name=APPSYNC_JS,runtimeVersion=1.0.0 --code file://getProduct.js \
  --caching-config '{"ttl":600,"cachingKeys":["$context.arguments.id"]}'
```
Caching keys rules:
- Public data: key on arguments only (`$context.arguments.id`).
- Per-user data: **include identity** (`$context.identity.sub`, or
  `$context.identity.claims.custom:tenant_id` for tenant-shared data). Missing identity in
  the key = user A receives user B's cached profile.
- Keys may be the top-level maps `$context.arguments`, `$context.source` and `$context.identity`
  or string fields inside them. Without keys, the defaults are the contents of all three maps.

## 3. Evict on mutation
In the mutation resolver's request or response handler (JS runtime; it works only in mutations):
```js
import { extensions } from '@aws-appsync/utils';
export function response(ctx) {
  extensions.evictFromApiCache('Query', 'getProduct', { 'ctx.args.id': ctx.args.input.id });
  return ctx.result;
}
```
The key map must name the same caching keys as the cached resolver, in the same order. When an
entry is removed the response `extensions` carries `apiCacheEntriesDeleted`. Evicting needs a known key, so
use per-resolver caching with explicit keys. Full flush (deploys, bulk loads):
`aws appsync flush-api-cache --api-id <API_ID>`.

## 4. Measure
Enhanced metrics (per-resolver behaviour) emit `CacheHit` and `CacheMiss`; the cache health metrics
include `CacheNetworkBandwidthOutAllowanceExceeded` and `CacheEngineCPUUtilization`. A low hit ratio
on a cached resolver means the key is too specific or the TTL too short.

## Gotchas
- Caching a resolver whose data source applies authorisation (e.g. row-level checks in
  Lambda) without identity in the key skips that authorisation for cache hits.
- After changing caching keys, flush the cache so entries built with the old keys do not linger.

## Verify
- [ ] Two identical queries: second shows `CacheHit` increment and lower latency in the X-Ray/AppSync logs.
- [ ] User A and user B querying `me` get their own data (identity in key).
- [ ] Update mutation then query: fresh value returned immediately (eviction works).
- [ ] `get-api-cache` shows the intended behaviour, type and TTL.

## Checked

2026-10-27, AWS documentation (current release as read on that date). AWS AppSync Developer Guide caching, resolver extensions and monitoring pages; botocore appsync 2017-07-25 model (ApiCachingBehavior, ApiCacheType). Fixed: full request caching caches each resolver separately (not the whole response); an OPERATION_LEVEL_CACHING behaviour exists (15 MB maximum, key includes query, variables, identity and headers); encryption at rest and in transit is always on for new caches and cannot be disabled, so the create-api-cache encryption flags were removed; maximum TTL 3,600 seconds; eviction works only in mutations and the key map must follow the cachingKeys order; the hit-rate rule of thumb and the CacheCurrItems, CacheEvictions and CacheReplicationLag metric names are not in the docs and were removed. Confirmed: per-resolver TTL mandatory and keys optional, default keys, flush-api-cache, apiCacheEntriesDeleted, CacheHit and CacheMiss.
Method: documentation only; no commands were run.
