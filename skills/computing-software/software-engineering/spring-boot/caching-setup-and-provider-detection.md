---
id: computing-software.software-engineering.spring-boot.caching-setup-and-provider-detection
name: caching-setup-and-provider-detection
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, caching, enablecaching, cachemanager, spring-cache-type, cachemanagercustomizer, simple-cache]
level: practitioner
status: docs-checked
description: "Enable Spring caching in Boot, how the cache provider is detected in order, forcing spring.cache.type, the simple provider, cache-names and no-op caching."
sources:
  - https://docs.spring.io/spring-boot/reference/io/caching.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Boot auto-configures cache infrastructure when caching is enabled with `@EnableCaching`. Avoid putting `@EnableCaching` on the main application class: it makes caching mandatory, including in test suites. Add caching annotations to service methods; before invoking, the abstraction looks for an entry in the named cache matching the arguments, returns it if found, else invokes the method and updates the cache. Standard JSR-107 annotations (such as `@CacheResult`) work transparently, but do not mix Spring Cache and JCache annotations. Cache update and evict annotations are also available.

Providers: the abstraction needs a `Cache`/`CacheManager`. If you have not defined a `CacheManager` bean or a `CacheResolver` named `cacheResolver`, Boot detects, in order: Generic, JCache (EhCache 3, Hazelcast, Infinispan and others), Hazelcast, Infinispan, Couchbase, Redis, Caffeine, Cache2k, Simple. If Boot auto-configures the manager you can force a provider with `spring.cache.type`. The `spring-boot-starter-cache` starter brings `spring-context-support`, which you must include manually to use JCache or Caffeine.

Customizing: expose `CacheManagerCustomizer` beans (any number, ordered with `@Order`/`Ordered`) to tune an auto-configured manager before initialization; the customizer is not invoked if the manager is of a different type (for example you provided your own).

Generic: used if the context defines at least one `Cache` bean; a `CacheManager` wrapping all such beans is created.

Simple (default when no library is present): `ConcurrentHashMap` store, not recommended for production. Caches are created as needed; restrict with:
```yaml
spring:
  cache:
    cache-names: "cache1,cache2"
```
Using an unlisted cache then fails at runtime when needed, not at startup. Nearly all real providers require each cache to be configured explicitly; some customise default caches via `spring.cache.cache-names`.

None: a no-op cache with `spring.cache.type: "none"`.

## Checked

2026-11-07

Read caching.adoc (docs-repo source of the cited Caching page) in full. The include-code examples (MyMathService, MyCacheManagerConfiguration, MyIntegrationTests) were not opened; claims rest on page prose.
Confirmed: auto-configuration when @EnableCaching is present and the tip against putting it on the main application class; lookup-by-argument behaviour described for piDecimals; JSR-107 annotations usable but "strongly advise" not mixing; update/evict tip; provider detection conditions (no CacheManager bean, no CacheResolver named cacheResolver) and the nine-provider order Generic, JCache, Hazelcast, Infinispan, Couchbase, Redis, Caffeine, Cache2k, Simple; spring.cache.type forcing; spring-boot-starter-cache bringing spring-context-support (needed manually for JCache or Caffeine); CacheManagerCustomizer with @Order/Ordered and the not-invoked NOTE; Generic (at least one Cache bean); Simple (ConcurrentHashMap, not recommended for production, cache-names restriction, runtime failure for unlisted caches); None via spring.cache.type "none".
Nothing trimmed.

Method: documentation only; no commands were run.
