---
id: computing-software.software-engineering.java.spring-caching-and-scheduled-tasks
name: spring-caching-and-scheduled-tasks
category: computing-software
field: software-engineering
product: java
tags: [java, spring-cache, scheduled-tasks, cacheable, caffeine, shedlock, spring-boot]
level: practitioner
status: docs-checked
description: "Use Spring's cache abstraction (Cacheable, CacheEvict, Caffeine/Redis) and @Scheduled tasks correctly: proxy pitfalls, TTLs, thread pools and single-run locking across instances."
sources: ["https://docs.spring.io/spring-framework/reference/integration/cache.html", "https://docs.spring.io/spring-boot/reference/io/caching.html", "https://docs.spring.io/spring-framework/reference/integration/scheduling.html", "https://github.com/lukas-krecan/ShedLock"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spring caching and scheduled tasks

**Goal:** cache expensive reads and run periodic jobs without the classic proxy,
staleness and multi-instance bugs.

## Caching
```java
@EnableCaching @Configuration class CacheConfig {}

@Service class RatesService {
    @Cacheable(cacheNames = "fx-rates", key = "#base + ':' + #quote", unless = "#result == null")
    public BigDecimal rate(String base, String quote) { return client.fetch(base, quote); }

    @CacheEvict(cacheNames = "fx-rates", allEntries = true)
    public void refreshAll() {}
}
```
```properties
spring.cache.cache-names=fx-rates
spring.cache.caffeine.spec=maximumSize=10000,expireAfterWrite=5m
# or spring.cache.type=redis with spring.cache.redis.time-to-live=5m
```
Without a cache library Boot auto-configures a simple provider that keeps entries in concurrent maps in memory; the Boot docs say it is not recommended for production.

### Proxy pitfalls (same for @Transactional, @Async)
- Self-invocation bypasses the proxy: `this.rate(...)` from another method in the same class
  is not cached. Call through another bean.
- Cached return values are shared objects: return immutable types.
- `sync = true` on `@Cacheable` asks the underlying cache to lock the entry while the value is computed, so concurrent misses for the same key do not all call the method.

## Scheduling
```java
@EnableScheduling @Configuration class SchedConfig {}

@Component class Jobs {
    @Scheduled(fixedDelayString = "PT1M", initialDelayString = "PT30S")   // 1 min after previous run ends
    void syncInventory() { ... }

    @Scheduled(cron = "0 0 3 * * *", zone = "Europe/London")             // sec min hour dom mon dow
    void nightlyReport() { ... }
}
```
- `fixedRate` is a fixed period between invocations; `fixedDelay` is a fixed period between the end of the last invocation and the start of the next.
- Boot's default `ThreadPoolTaskScheduler` uses **one thread**: a slow job delays all others. Set
  `spring.task.scheduling.pool.size=4`, or use virtual threads (Java 21+, `spring.threads.virtual.enabled=true`); with virtual threads prefer fixed rates and cron over fixed delays, because fixed-delay tasks run on a single scheduler thread.
- Exceptions are logged and the schedule continues; add metrics/alerts yourself.

## Multiple instances
Every replica runs every `@Scheduled` method. For run-once jobs use ShedLock (third-party; needs `@EnableSchedulerLock(defaultLockAtMostFor = ...)` and a lock provider bean):
```java
@Scheduled(cron = "0 0 3 * * *")
@SchedulerLock(name = "nightlyReport", lockAtMostFor = "PT30M", lockAtLeastFor = "PT1M")
void nightlyReport() { ... }
```
(JDBC, Redis, Mongo and others are supported as lock stores; durations accept `1s`/`5m`, plain milliseconds or ISO-8601 `PT15M`), or move the job to a Kubernetes CronJob / external scheduler.

## Verify
- [ ] Every cache has a size bound and TTL; cache metrics (prefixed `cache`) visible in Micrometer.
- [ ] Scheduled jobs are idempotent and either locked or safe to run on every replica.

## Checked

Date: 2026-10-25. Documentation release: Spring Boot 4.1.2 and Spring Framework 7.0.10 (GitHub main documentation sources; releases of 2026-10-22); ShedLock README (GitHub master); Caffeine CaffeineSpec source.

Confirmed: `spring.cache.caffeine.spec` with `maximumSize` and `expireAfterWrite`; `spring.cache.redis.time-to-live`; `spring.cache.cache-names`; simple provider default; `@Cacheable(sync = true)`; `unless` with `#result`; `@Scheduled` `fixedDelayString` accepting ISO-8601 durations, `zone`, `initialDelayString`, `fixedRate` semantics; six-field cron; Boot default scheduler uses one thread, `spring.task.scheduling.pool.size`, `spring.threads.virtual.enabled`; fixed-delay caveat with virtual threads; Boot cache metrics prefix; ShedLock `@SchedulerLock` attributes, `@EnableSchedulerLock` and duration formats.

Removed as unconfirmed: the claim that only public methods are intercepted for caching, the "no expiry and no size limit" and "per instance only" remarks, the "overlap queued" remark, the Boot 3.2 version note and the `cache.gets` metric name.

Method: documentation only; no commands were run.
