---
id: computing-software.software-engineering.java.concurrency-with-executors-and-virtual-threads
name: concurrency-with-executors-and-virtual-threads
category: computing-software
field: software-engineering
product: java
tags: [java, concurrency, executors, virtual-threads, pinning, jep-444, executorservice, project-loom]
level: advanced
status: docs-checked
description: "Choose between fixed thread pools and Java 21 virtual threads, and avoid virtual-thread pinning and pooling mistakes."
sources: ["https://openjdk.org/jeps/444", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Executors.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java concurrency — executors and virtual threads

**Goal:** pick the right executor for CPU-bound versus blocking work, and know the
documented sharp edges of virtual threads (JEP 444, final in Java 21).

## 1. Choosing an ExecutorService
```java
Executors.newFixedThreadPool(n)               // fixed number of threads, shared unbounded queue
Executors.newVirtualThreadPerTaskExecutor()   // one new virtual thread per submitted task
```
`newFixedThreadPool` reuses a fixed number of threads fed from a shared unbounded queue
(Executors API docs). For CPU-bound work, more threads than processor cores cannot
improve throughput, so keep a bounded platform-thread pool.

## 2. Virtual threads for blocking work
JEP 444 says virtual threads pay off when the workload is not CPU-bound and there are
many concurrent tasks that spend their time waiting. A virtual thread normally
unmounts from its carrier (a platform thread) when it blocks on I/O or on a JDK blocking
operation such as `BlockingQueue.take()`, freeing the carrier for another virtual thread.
Use `Executors.newVirtualThreadPerTaskExecutor()` and create a virtual thread per task.
JEP 444 has a section "Do not pool virtual threads": they are cheap, so create one per
task rather than sharing a pool. Virtual threads do not remove the need for
synchronisation of shared mutable state.

## 3. Pinning
A virtual thread cannot unmount while blocking when it is pinned to its carrier, in two
documented cases: it is executing inside a `synchronized` block or method, or it is
executing a native method or foreign function. Pinning does not make an application
incorrect but can hurt scalability, because the carrier and OS thread stay blocked for
the duration of the blocking operation. Diagnostics from JEP 444: a JDK Flight Recorder
event is emitted when a thread blocks while pinned, and the system property
`jdk.tracePinnedThreads` (`full` or `short`) prints a stack trace when a thread blocks
while pinned. JEP 444 suggests assessing replacing a `synchronized` use with a
`java.util.concurrent` lock in code that blocks while holding it. Check the JEP and your
JDK's release notes, since the JEP says the `synchronized` limitation may be removed in
a future release.

## Verify
- [ ] CPU-bound work runs on a bounded platform-thread pool, not one thread per task.
- [ ] Blocking, I/O-bound work uses one virtual thread per task and is not pooled.
- [ ] Code that blocks inside `synchronized` was checked for pinning with the JFR event or
      `jdk.tracePinnedThreads` on the JDK actually deployed.

## Checked
2026-11-01. Confirmed: JEP 444 (virtual-thread use cases, not CPU-bound guidance,
`newVirtualThreadPerTaskExecutor`, "Do not pool virtual threads", mount/unmount on
blocking I/O, two pinning scenarios, JFR event, `jdk.tracePinnedThreads=full|short`,
note that the synchronized limitation may be lifted later); Executors API docs for Java 21
(`newFixedThreadPool` and its shared unbounded queue). Removed unconfirmed claims:
thread-pool starvation walkthrough, `newCachedThreadPool` advice, sizing from
`availableProcessors()`, CompletableFuture composition and exception advice, ScopedValue and
ThreadLocal guidance, the Java 24 pinning statement, and `shutdown()`/`shutdownNow()`
semantics.
Method: documentation only; no commands were run.

Related: computing-software.software-engineering.concurrency.deadlock-and-race-detection,
computing-software.software-engineering.java.spring-boot-services
