---
id: computing-software.messaging-and-integration.apache-activemq-artemis.optional-jvm-and-executor-metrics
name: optional-jvm-and-executor-metrics
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,metrics,jvm-memory,jvm-gc,jvm-threads,netty-pool,executor-services,security-caches,activemq-artemis]
level: advanced
status: docs-checked
description: "Switch on the optional Micrometer metric groups in the broker.xml metrics element: jvm-gc, threads, file descriptors, processor, logging, security caches, executors."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/metrics.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optional metric groups

Besides broker metrics, Micrometer-provided groups (not prefixed `artemis.`) are switched on in the `metrics` element. Defaults are shown:
```xml
<metrics>
   <jvm-memory>true</jvm-memory>          <!-- default true -->
   <jvm-gc>true</jvm-gc>                  <!-- default false -->
   <jvm-threads>true</jvm-threads>        <!-- default false -->
   <netty-pool>true</netty-pool>          <!-- default false -->
   <file-descriptors>true</file-descriptors>
   <processor>true</processor>
   <uptime>true</uptime>
   <logging>true</logging>
   <security-caches>true</security-caches>
   <executor-services>true</executor-services>
</metrics>
```
All except `jvm-memory` default to `false`.
- JVM memory: buffer and memory pool utilization. JVM GC: live/max data size, promotion and allocation rates, pause counts. JVM thread: peak, daemon and live threads.
- Netty allocator, file descriptors (current and max), processor (CPU count, usage, 1-minute load), uptime.
- Logging: counts events per level. **Works only with Log4j2**; when embedding with another logger (Log4j 1.x, JUL, Logback) enabling it makes the broker fail to start with `NoClassDefFoundError`.
- Security caches: `cache.size`, `cache.puts`, `cache.gets` (tag `result` = `hit` or `miss`), `cache.evictions`, `cache.eviction.weight`, tagged by `cache` (`authentication` or `authorization`).
- Executor services: per-pool `executor.*` metrics (`executor.active`, `executor.queued`, `executor.pool.size` and others) tagged with the pool role (general, io, paging, scheduled), and `netty.eventexecutor.tasks.pending`.

## Checked

Method: docs-checked 2026-11-09 against metrics.adoc (read in full). Removed the Verify step.
