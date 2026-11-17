---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.instrumenting-thread-pools-and-caches
name: instrumenting-thread-pools-and-caches
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [thread-pool-metrics, cache-instrumentation, instrumentation, micrometer-binders, prometheus-best-practices]
level: practitioner
status: docs-checked
description: "Which metrics to export for thread pools and caches per Prometheus guidance, and how Micrometer binds executors and Caffeine, Guava, Ehcache, Hazelcast and JCache caches."
sources: ["https://prometheus.io/docs/practices/instrumentation/", "https://docs.micrometer.io/micrometer/reference/cache.html", "https://docs.micrometer.io/micrometer/reference/jvm.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instrumenting thread pools and caches

## What to track (Prometheus instrumentation page)
- Thread pools: queued requests, threads in use, total threads, tasks processed, how long they took, and time spent waiting
  in the queue.
- Caches: total queries, hits, overall latency, and the query count, errors and latency of the system the cache fronts.
- Do not label by unbounded values such as cache keys; every labelset is another time series.

## Micrometer executor binder (JVM page)
```java
new ExecutorServiceMetrics(executorService, executorServiceName, tags).bindTo(registry);
Executor monitored = ExecutorServiceMetrics.monitor(registry, executor, executorName, tags);
```
For a `ThreadPoolExecutor` the page lists: `executor` (Timer, task execution duration), `executor.idle` (Timer, time tasks spend
queued before execution), `executor.completed` (FunctionCounter), `executor.active` and `executor.queued` (Gauges),
`executor.queue.remaining`, `executor.pool.size`, `executor.pool.core`, `executor.pool.max` (Gauges). A `ForkJoinPool` gets a
different set (for example `executor.steals`, `executor.running`, `executor.parallelism`). Exported Prometheus names depend on
your registry's naming conversion; check the scrape output rather than assuming them.

## Micrometer cache binders (cache page)
Supported: Caffeine, Ehcache, Guava, Hazelcast, JCache. Each exposes basic features such as hits versus misses, tracked with a
function-tracking counter. Caffeine and Guava caches must be built with `recordStats()`.
```java
Cache<String, String> cache = Caffeine.newBuilder().recordStats().build();
CaffeineCacheMetrics.monitor(meterRegistry, cache, "testCache", tags);
```
The page's hit-ratio query, over its example Guava metric, is `sum(rate(book_guava_requests_total{result="hit"}[1m])) / sum(rate(book_guava_requests_total[1m]))`.
It suggests alerting on an upper bound for the miss ratio rather than a lower bound on the hit ratio, because with no activity the
ratio drops to 0.

## Verify
- [ ] The scrape output shows queue and active-thread series for each pool, named per your registry's conversion.
- [ ] No metric is labelled by cache key.

## Checked
Checked 2026-11-07. Read in full: the Prometheus instrumentation practices page, the Micrometer cache page, and the Micrometer JVM page
down to the ForkJoinPool metric list (about the first 60 lines; later binders were not read). Removed as not on these pages: the invented
`pool_*` and `cache_*` metric tables, the rejected-tasks and eviction metrics, `executor_*` Prometheus names, the Python lru_cache advice,
the Go goroutine advice, the saturation and p99 queries, and the client_java source (not read).
Method: documentation only; no commands were run.
