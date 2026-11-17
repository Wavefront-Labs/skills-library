---
id: computing-software.cloud-infrastructure-engineering.aws.api-gateway-stage-caching
name: api-gateway-stage-caching
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-gateway, stage-cache, api-caching, cache-key, cache-invalidation, rest-api, performance]
level: practitioner
status: docs-checked
description: "Enable API Gateway REST stage caching: cache size and TTL, cache key parameters, per-method overrides, client invalidation control, encryption and hit/miss metrics."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/canary-release.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-metrics-and-dimensions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway stage caching (REST APIs)

**Goal:** serve repeated GETs from the gateway cache, with correct cache keys so users never
see each other's data. HTTP APIs have no built-in cache — put CloudFront in front instead.

## 1. Enable
```bash
aws apigateway update-stage --rest-api-id "$API" --stage-name prod --patch-operations \
  op=replace,path=/cacheClusterEnabled,value=true \
  op=replace,path=/cacheClusterSize,value=0.5
```
- Cache sizes (`cacheClusterSize`): 0.5, 1.6, 6.1, 13.5, 28.4, 58.2, 118 or 237 GB; creating the cache takes up to
  about 4 minutes, and changing capacity replaces the cache and deletes cached data.
- TTL 0–3600 s, default 300; the largest cacheable response is 1048576 bytes. Only GET methods are cached by default;
  per-method overrides use method settings (`cachingEnabled`, `cacheTtlInSeconds`, `cacheDataEncrypted`).

## 2. Cache keys (the part people get wrong)
By default the key is the resource path only. Add every parameter that changes the response:
```bash
aws apigateway update-method --rest-api-id "$API" --resource-id "$RES" --http-method GET \
  --patch-operations op=add,path=/requestParameters/method.request.querystring.page,value=false
aws apigateway update-integration --rest-api-id "$API" --resource-id "$RES" --http-method GET \
  --patch-operations op=add,path=/cacheKeyParameters/method.request.querystring.page
```
User-specific responses must include the identity (e.g. `Authorization` header or a
tenant header) in the cache key, or disable caching on that method.

## 3. Invalidation
- Whole stage: `aws apigateway flush-stage-cache --rest-api-id "$API" --stage-name prod`.
- Per request: client sends `Cache-Control: max-age=0`. Require authorisation for it
  (`requireAuthorizationForCacheControl=true`, callers need `execute-api:InvalidateCache`)
  and choose `unauthorizedCacheControlHeaderStrategy` = `FAIL_WITH_403`,
  `SUCCEED_WITH_RESPONSE_HEADER` or `SUCCEED_WITHOUT_RESPONSE_HEADER` — otherwise any client can invalidate the cache.

## 4. Metrics
`CacheHitCount` and `CacheMissCount` (enable detailed metrics on the stage for per-method).

## Gotchas
- Lambda authorizer caching is separate from response caching.
- A canary uses the stage cache only when `useStageCache` is set and caching is enabled; production and canary responses are cached separately if they use different deployments.

## Verify
- [ ] Second identical GET is faster and `CacheHitCount` increments; integration not invoked (Lambda invocations unchanged).
- [ ] Two users with different identities never receive each other's cached response.
- [ ] Unauthorised `Cache-Control: max-age=0` does not refresh the cache.

## Checked
Date: 2026-10-24. Documentation release: Amazon API Gateway Developer Guide (awsdocs source, June 2023 snapshot) plus the current botocore `apigateway` model.
Confirmed: `cacheClusterSize` values; up to 4 minutes to create the cache; capacity change deletes cached data; 1048576-byte response limit; GET-only default; TTL default 300 and maximum 3600; `Cache-Control: max-age=0` invalidation and `execute-api:InvalidateCache`; header strategy values; `CacheHitCount` and `CacheMissCount`; canary `useStageCache`.
Fixed: `SUCCEED_WITHOUT_UPDATING_CACHE` is not a valid value (valid: `FAIL_WITH_403`, `SUCCEED_WITH_RESPONSE_HEADER`, `SUCCEED_WITHOUT_RESPONSE_HEADER`). Removed unconfirmed hourly billing, method-level patch paths, the 5xx/4xx caching claim and the hit-ratio rule of thumb.

Method: documentation only; no commands were run.
