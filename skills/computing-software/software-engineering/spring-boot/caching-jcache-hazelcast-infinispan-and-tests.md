---
id: computing-software.software-engineering.spring-boot.caching-jcache-hazelcast-infinispan-and-tests
name: caching-jcache-hazelcast-infinispan-and-tests
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, caching, jcache, jsr-107, hazelcast, infinispan, autoconfigurecache, test]
level: practitioner
status: docs-checked
description: "Use JCache, Hazelcast or Infinispan with Boot caching, choose the JCache provider and config file, and disable caching in tests with @AutoConfigureCache or spring.cache.type=none."
sources:
  - https://docs.spring.io/spring-boot/reference/io/caching.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
JCache (JSR-107): bootstrapped when a `CachingProvider` is on the classpath; `JCacheCacheManager` comes from `spring-boot-starter-cache`. Boot has dependency management for Ehcache 3, Hazelcast and Infinispan; others work too. If more than one provider is present, name it:
```yaml
spring:
  cache:
    jcache:
      provider: "com.example.MyCachingProvider"
      config: "classpath:example.xml"
```
When a library has both a native implementation and JSR-107 support, Boot prefers JSR-107. A single `HazelcastInstance` is reused for the JCache `CacheManager` unless `spring.cache.jcache.config` is set. Customize the underlying `javax.cache.CacheManager` with `spring.cache.cache-names` (plus a custom `Configuration` bean) or `CacheManagerCustomizer` beans. A standard `javax.cache.CacheManager` bean you define is wrapped automatically with no further customization.

Hazelcast: with an auto-configured `HazelcastInstance` and `com.hazelcast:hazelcast-spring` on the classpath, it is wrapped in a Spring `CacheManager`. `spring.cache.type=hazelcast` uses that implementation; `spring.cache.type=jcache` uses Hazelcast as JCache. With several JCache providers, set the JCache provider explicitly to force Hazelcast.

Infinispan: no default config location, so set it, else the default bootstrap is used:
```yaml
spring:
  cache:
    infinispan:
      config: "infinispan.xml"
```
`spring.cache.cache-names` creates caches; a custom `ConfigurationBuilder` bean customizes them.

Tests: if you define a custom `CacheManager`, keep caching configuration in an isolated `@Configuration` class so slice tests do not require it; `@SpringBootTest` with a full context needs an explicit overriding configuration. If caching is auto-configured, annotate tests with `@AutoConfigureCache` to swap in a no-op `CacheManager`, or set `spring.cache.type: "none"`.

## Checked

2026-11-07

Read caching.adoc in full (cited Caching page), using the JCache, Hazelcast, Infinispan and Testing sections. The MyIntegrationTests include example was not opened.
Confirmed: CachingProvider bootstrap and JCacheCacheManager from spring-boot-starter-cache; dependency management for Ehcache 3, Hazelcast and Infinispan; explicit provider needed when several are present, with the spring.cache.jcache.provider / config YAML; Boot prefers JSR-107 over a native implementation; HazelcastInstance reuse unless spring.cache.jcache.config is set; the two customization routes (cache-names plus Configuration bean, CacheManagerCustomizer); wrapping of a standard javax.cache.CacheManager bean; Hazelcast needing com.hazelcast:hazelcast-spring and the spring.cache.type hazelcast vs jcache NOTE; Infinispan config location and ConfigurationBuilder bean; test advice (isolated @Configuration, @SpringBootTest overriding configuration, @AutoConfigureCache, spring.cache.type none).
Nothing trimmed.

Method: documentation only; no commands were run.
