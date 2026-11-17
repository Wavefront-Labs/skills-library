---
id: computing-software.messaging-and-integration.apache-camel.thread-pool-profiles
name: thread-pool-profiles
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, threading, thread-pool, rejected-policy, virtual-threads]
level: advanced
status: docs-checked
description: "Camel threading model: default thread pool profile (10 core, 20 max, queue 1000, CallerRuns), custom profiles via executorService, thread names, shutdown and virtual threads."
sources:
  - https://camel.apache.org/manual/threading-model.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread pools and profiles

Camel uses JDK thread pools in Multicast/Split parallel processing, SEDA, the Threads EIP, and components like JMS, Kafka, Netty and Jetty.

Default profile: `poolSize` 10, `maxPoolSize` 20, `keepAliveTime` 60 seconds, `maxQueueSize` 1000 (`-1` unbounded), `allowCoreThreadTimeOut` true, `rejectedPolicy` CallerRuns (others: Abort, Block).

Profiles are recipes; a pool is a concrete `ExecutorService`. Only one default profile exists and custom profiles inherit unset options from it.
- Default: `getDefaultThreadPoolProfile()`, Spring XML `threadPoolProfile` with `defaultProfile="true"`, or `camel.threadpool.pool-size`.
- Custom: `ThreadPoolProfileBuilder` plus `registerThreadPoolProfile`, or `camel.threadpool.config[profileId]`.
- A route references one via `executorService`; Camel first looks for an `ExecutorService` with that id in the registry, then for a profile.

Thread names default to `Camel (#camelId#) thread ##counter# - #name#`; set `camel.main.thread-name-pattern`.

Shutdown: `shutdownGraceful` waits then turns aggressive; default timeout 10000 ms. Pools appear in JMX under `threadpools` (needs camel-management).

Virtual threads (Java 21+): set system property `camel.threads.virtual.enabled=true`. With a positive `maxQueueSize` a semaphore caps concurrent tasks and pool sizes are ignored.

Verify: log lines show thread names matching the configured pattern, and a Multicast with `parallelProcessing=true` creates its pool from the default profile unless `executorService` names another profile.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel threading model page: default profile values (poolSize 10, maxPoolSize 20, keepAliveTime 60, maxQueueSize 1000 with -1 unbounded, allowCoreThreadTimeOut true, rejectedPolicy CallerRuns with Abort and Block), single default profile and inheritance, the Java, XML and application property ways to configure profiles, registry-then-profile lookup, default thread name pattern, 10000 ms shutdownGraceful timeout, JMX threadpools and the virtual thread behaviour (Java 21, camel.threads.virtual.enabled, semaphore cap from a positive maxQueueSize) match. The old verify line about a 21st task was removed because the page does not describe when a thread is added versus a task queued. No commands were run.
