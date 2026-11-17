---
id: computing-software.software-engineering.spring-boot.caching-redis-caffeine-and-couchbase
name: caching-redis-caffeine-and-couchbase
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, caching, redis, caffeine, couchbase, cache2k, spring-cache-redis, cacheloader]
level: practitioner
status: docs-checked
description: "Configure Redis, Caffeine, Couchbase and Cache2k cache managers in Boot: spring.cache.* properties, specs, TTL, key prefix, cache loader and async mode."
sources:
  - https://docs.spring.io/spring-boot/reference/io/caching.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Redis: auto-configures a `RedisCacheManager` when Redis is available. `spring.cache.cache-names` creates caches; defaults come from `spring.cache.redis.*`:
```yaml
spring:
  cache:
    cache-names: "cache1,cache2"
    redis:
      time-to-live: "10m"
```
A key prefix is added by default so separate caches with the same key do not overlap; keep it enabled if you create your own `RedisCacheManager`. Replace the default configuration with your own `RedisCacheConfiguration` bean (for example to change serialization), or register a `RedisCacheManagerBuilderCustomizer` bean for per-cache settings.

Caffeine: a `CaffeineCacheManager` (from `spring-boot-starter-cache`) is auto-configured when Caffeine is present. Customization, in order: `spring.cache.caffeine.spec`, a `CaffeineSpec` bean, a `Caffeine` bean.
```yaml
spring:
  cache:
    cache-names: "cache1,cache2"
    caffeine:
      spec: "maximumSize=500,expireAfterAccess=600s"
```
A `CacheLoader` bean is associated with all caches, so it must be `CacheLoader<Object, Object>`; other generic types are ignored. For `Cache#retrieve` an `AsyncCache` is needed: register via a `CacheManagerCustomizer` calling `CaffeineCacheManager#registerCustomCache`, or set `spring.cache.caffeine.cache-mode` to `async` for named and on-demand caches.

Couchbase: with Spring Data Couchbase configured a `CouchbaseCacheManager` is auto-configured. `spring.cache.cache-names: "cache1,cache2"` plus `spring.cache.couchbase.expiration: "10m"` sets entry expiration; use a `CouchbaseCacheManagerBuilderCustomizer` for more control.

Cache2k: with the Cache2k Spring integration present a `SpringCache2kCacheManager` is auto-configured; `spring.cache.cache-names` creates caches and a `Cache2kBuilderCustomizer` bean sets defaults.

## Checked

2026-11-07

Read caching.adoc in full (cited Caching page), using the Couchbase, Redis, Caffeine and Cache2k sections. The MyCouchbaseCacheManagerConfiguration, MyRedisCacheManagerConfiguration and MyCache2kDefaultsConfiguration include examples were not opened.
Confirmed: RedisCacheManager with spring.cache.redis.* and time-to-live "10m", default key prefix and the keep-it-enabled advice, RedisCacheConfiguration bean, RedisCacheManagerBuilderCustomizer; CaffeineCacheManager from spring-boot-starter-cache, the three-step customization order (spec property, CaffeineSpec bean, Caffeine bean), the spec "maximumSize=500,expireAfterAccess=600s", CacheLoader<Object, Object> rule, AsyncCache / registerCustomCache / spring.cache.caffeine.cache-mode async; Couchbase auto-configuration conditions, spring.cache.couchbase.expiration "10m" and CouchbaseCacheManagerBuilderCustomizer; Cache2k SpringCache2kCacheManager and Cache2kBuilderCustomizer.
Nothing trimmed.

Method: documentation only; no commands were run.
