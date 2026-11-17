---
id: computing-software.devops-ci-cd.rundeck.api-rate-limiting
name: api-rate-limiting
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, api-rate-limiting, auth-token-limiter, client-ip-limiter, cache-size]
level: advanced
status: docs-checked
description: "Throttle Rundeck REST API calls (Enterprise) with rundeck.apiRateLimiting settings and choose session, auth token or client IP limiters."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/security/ratelimiting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
API Endpoints Rate Limiting (Enterprise, off by default) applies to requests to `<rundeck context path>/api/**`.

Example in `rundeck-config.properties` (or Configuration Management):

```properties
rundeck.apiRateLimiting.enabled = true
rundeck.apiRateLimiting.rate = 20
rundeck.apiRateLimiting.refillWindowInSeconds = 10
rundeck.apiRateLimiting.cacheSize = 100
rundeck.apiRateLimiting.include = rundeckpro.security.rateLimit.SessionApiRateLimiter;rundeckpro.security.rateLimit.ClientIPApiRateLimiter
```

Parameters and defaults:
- `enabled`: default false.
- `rate`: requests per time frame, default 100.
- `refillWindowInSeconds`: window size, default 10.
- `cacheSize`: size of the in-memory cache of per-token buckets for the auth-token limiter (tokens have no session). Default 100; size it to your token count. Cache overflows are exposed as JMX metric `rundeckpro.security.rateLimit.GuavaLoadingCacheBucketHolder.rateLimitCacheOverflowCount`.
- `include`: semicolon-separated limiters: `rundeckpro.security.rateLimit.AuthTokenApiRateLimiter` (per token), `SessionApiRateLimiter` (per authenticated session), `ClientIPApiRateLimiter` (per client IP; same package).

Verify by exceeding the rate with a loop of API calls and watching for rejected requests.

## Checked

2026-11-04. Confirmed against the Rundeck 4.0.x docs page Rate Limiting (Commercial): API rate limiting is off by default and applies to <context path>/api/**; defaults enabled=false, rate=100, refillWindowInSeconds=10, cacheSize=100; the three limiter class names and semicolon-separated include; the JMX overflow metric name. Nothing removed.

Method: documentation only; no commands were run.
