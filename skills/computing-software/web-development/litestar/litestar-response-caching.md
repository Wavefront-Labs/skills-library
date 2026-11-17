---
id: computing-software.web-development.litestar.litestar-response-caching
name: litestar-response-caching
category: computing-software
field: web-development
product: litestar
tags: [litestar, caching, cache, cache-key, response-cache, key-builder, redis, cache-response-filter]
level: practitioner
status: docs-checked
description: "Cache Litestar route handler responses with cache=True, seconds or CACHE_FOREVER, and customise the store, cache key builder and cache_response_filter."
sources: [https://docs.litestar.dev/latest/usage/caching.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar response caching

Goal: cache expensive or frequently polled handler responses.

## Method

1. Per handler, set `cache`:
   - `@get("/cached", cache=True)` uses `ResponseCacheConfig.default_expiration`. If that default is `None`, the response is cached indefinitely.
   - `@get("/cached-seconds", cache=120)` caches for 120 seconds.
   - `@get("/cached-forever", cache=CACHE_FOREVER)` (from `litestar.config.response_cache`) caches indefinitely.
2. App-level config: pass `ResponseCacheConfig(...)` as `response_cache_config=` to `Litestar`.
3. Store: the default is `MemoryStore`. Use another store by registering it and naming it:

```python
redis_store = RedisStore.with_client(url="redis://localhost/", port=6379, db=0)
cache_config = ResponseCacheConfig(store="redis_backed_store")
app = Litestar([something], stores={"redis_backed_store": redis_store}, response_cache_config=cache_config)
```

4. Cache key: by default the request path plus sorted query parameters. Override with a key builder taking the request, either app-wide (`ResponseCacheConfig(key_builder=key_builder)`) or per handler (`@get("/cached-path", cache=True, cache_key_builder=key_builder)`):

```python
def key_builder(request: Request) -> str:
    return request.url.path + request.headers.get("my-header", "")
```

5. Filter what is cached with `ResponseCacheConfig(cache_response_filter=fn)` where `fn(scope: HTTPScope, status_code: int) -> bool`. Example: `return 200 <= status_code < 300` caches only 2xx responses.

## Verify

The page's Redis example has a handler that sleeps one second and uses `cache=10`; time a repeat request yourself; the page does not state expected timings.

## Checked

2026-11-07. Read the full cited page(s) (usage/caching.html) and the example files they include, and confirmed the claims in this skill against that text. Removed a verify claim the page does not state; the verify step now says timings are not documented.

Method: documentation only; no commands were run.
