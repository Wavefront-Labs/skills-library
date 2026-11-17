---
id: computing-software.web-development.micronaut.micronaut-cache-advice
name: micronaut-cache-advice
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, cache-advice, cacheable, cache-put, cache-invalidate, caffeine, dynamic-cache]
level: intro
status: docs-checked
description: "Use Micronaut cache annotations (@Cacheable, @CachePut, @CacheInvalidate), configure Caffeine caches under micronaut.caches, and register a DynamicCacheManager."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/aop/caching.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: cache method results with annotations from the `io.micronaut.cache` package (Micronaut Cache project).

## Annotations

- `@Cacheable`: method result is cached in the named cache.
- `@CachePut`: caches the return value; unlike `@Cacheable` the original operation is never skipped.
- `@CacheInvalidate`: invocation invalidates one or more caches.

Using any of them activates `CacheInterceptor`. If the method returns a non-blocking type (`CompletableFuture` or a `Publisher`), the emitted result is cached; if the cache implementation supports non-blocking operations, reads are non-blocking too.

`CacheManager` plugs in implementations; `SyncCache` is the synchronous API, `AsyncCache` the non-blocking one.

## Configure caches

Caffeine is the default:

```yaml
micronaut:
  caches:
    my-cache:
      maximum-size: 20
```

This defines "my-cache" with maximum size 20. Define names in kebab case; camel case names are normalized (`myCache` becomes `my-cache`), and `@Cacheable` must reference the kebab-case name.

For `maximumWeight`, create a bean implementing `io.micronaut.caffeine.cache.Weigher`. Annotate it `@Named(<cache name>)` to bind it to one cache; unnamed weighers apply to all caches without a named weigher; with no beans a default is used. All options: the Micronaut Cache configuration reference (`DefaultCacheConfiguration`).

## Dynamic caches

Register a `DynamicCacheManager` bean when caches cannot be configured ahead of time: when an undefined cache is requested, it creates and returns one. With none defined, the framework registers `DefaultDynamicCacheManager`, which creates Caffeine caches with default values.

Other implementations: see the Micronaut Cache project guide.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.
