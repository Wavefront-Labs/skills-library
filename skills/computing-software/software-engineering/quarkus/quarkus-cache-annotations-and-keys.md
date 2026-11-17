---
id: computing-software.software-engineering.quarkus.quarkus-cache-annotations-and-keys
name: quarkus-cache-annotations-and-keys
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, cache, caffeine, cacheresult, cachekey, cdi, invalidation]
level: practitioner
status: docs-checked
description: "Cache CDI bean method results in Quarkus with @CacheResult, @CacheInvalidate, @CacheKey and CacheKeyGenerator, and know exactly how cache keys are built."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/cache.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus cache annotations and key building

Add the `quarkus-cache` extension (default backend: Caffeine; Infinispan and Redis are alternatives). Annotations work on CDI bean methods with any access modifier except `private`.

## Annotations
- `@CacheResult(cacheName = "weather-cache")`: returns the cached value without running the method when the key exists; otherwise runs it and stores the result. Concurrent calls on a missing key invoke the method once (lock on miss); `lockTimeout` can interrupt the lock (disabled by default). Not allowed on `void` methods. `null` values are cached too. Works on Kotlin `suspend` functions with `quarkus-kotlin`.
- `@CacheInvalidate(cacheName = ...)`: removes the entry for the computed key; no-op if absent.
- `@CacheInvalidateAll(cacheName = ...)`: clears the cache. Invalidation happens after the method completes successfully; if it throws, nothing is invalidated.
- `@CacheKey`: marks a parameter as part of the key; use only when some arguments should not be.
- Several can be stacked on one method, e.g. `@CacheInvalidate` plus `@CacheResult` on the same name to force a refresh, or `@CacheInvalidateAll` for `foo` and `bar`.

## Key building order
1. If `keyGenerator` is set on the annotation, it is used and `@CacheKey` is ignored.
2. No arguments: `DefaultCacheKey` from the cache name.
3. One argument: that argument.
4. Several arguments, exactly one `@CacheKey`: that argument.
5. Several `@CacheKey` arguments: `CompositeCacheKey` of them.
6. Several arguments, none annotated: `CompositeCacheKey` of all.

Key order matters, argument names do not: `invalidate(String a, Integer b)` matches `load(String, Integer)`, but `invalidate(Integer, String)` does not. Non-primitive key arguments must implement `equals()` and `hashCode()`. Normal-scoped injected beans (e.g. `JsonWebToken`, `Principal`, `SecurityIdentity`) are CDI client proxies and are rejected with a `CacheException` as keys; pass a derived value like `principal.getName()`.

## Custom `CacheKeyGenerator`
```java
@ApplicationScoped
public class ApplicationScopedKeyGen implements CacheKeyGenerator {
    @Override
    public Object generate(Method method, Object... methodParams) {
        return new CompositeCacheKey(method.getName(), methodParams[0]);
    }
}
// usage: @CacheResult(cacheName = "foo", keyGenerator = ApplicationScopedKeyGen.class)
```
It must be a CDI bean (exactly one bean with that type, or the build fails; its scope must be active) or have a public no-args constructor (then no injection). Check argument count before indexing to avoid `IndexOutOfBoundsException`; avoid expensive `Method` calls.

## Config
`quarkus.cache.caffeine."foo".maximum-size=20`, `.initial-capacity=10`, `.expire-after-write=60S`. By default caches never evict. Metrics: `quarkus.cache.caffeine."foo".metrics-enabled=true` (needs a `quarkus-micrometer-registry-*` extension). Mixed backends: `quarkus.cache.type=caffeine` plus `quarkus.cache.weather-cache.type=redis`.

## Gotcha
Do not swallow exceptions and return `null` from a `@CacheResult` method to signal failure: the `null` gets cached. Let the exception propagate; failed calls are not cached.

## Checked

2026-11-07. Read in full: cache.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
