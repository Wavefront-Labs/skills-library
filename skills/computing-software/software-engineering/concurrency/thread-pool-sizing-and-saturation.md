---
id: computing-software.software-engineering.concurrency.thread-pool-sizing-and-saturation
name: thread-pool-sizing-and-saturation
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, concurrency-models, thread-pool-sizing, saturation-policy, backpressure, executor-service, littles-law]
level: practitioner
status: gated
description: "Size thread pools for CPU-bound and I/O-bound work, choose bounded queues and rejection policies, and detect pool saturation before it becomes an outage."
sources:
  - https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ThreadPoolExecutor.html
  - https://jcip.net/
  - https://learn.microsoft.com/en-us/dotnet/standard/threading/the-managed-thread-pool
  - https://brooker.co.za/blog/2018/06/20/littles-law.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread pool sizing and saturation policies

## Sizing formulas (starting points, then measure)
- **CPU-bound:** threads ≈ number of cores (`Runtime.getRuntime().availableProcessors()`, `os.cpu_count()`), maybe +1. More threads only add context switching.
- **I/O-bound (Goetz, JCIP):** threads ≈ cores x target utilisation x (1 + wait time / compute time). A task waiting 90 ms on I/O per 10 ms CPU on 8 cores -> 8 x 1 x (1 + 9) = 80. (arithmetic computed)
- **Little's law:** concurrency needed = arrival rate x latency. 200 req/s x 0.25 s = 50 in flight. If the pool is smaller, requests queue.
- In containers, the visible CPU count follows cgroup limits on modern runtimes (JDK 10+ and .NET Core 3+ (gated: unconfirmed, source is paywalled or blocked); Go 1.25+ `GOMAXPROCS` per the Go 1.25 release notes, which also say the runtime updates it periodically; earlier Go needs `automaxprocs`). Check what your runtime sees.
- Downstream limits cap useful concurrency: a pool of 200 threads sharing a DB pool of 20 connections gives 180 threads waiting.

## Bounded queues and rejection
Unbounded queues hide overload until memory runs out and latency is minutes. Bound both threads and queue:
```java
// Java, not compiled here (gated: unconfirmed, source is paywalled or blocked)
var pool = new ThreadPoolExecutor(
    16, 16,                                   // core = max for predictable behaviour
    0L, TimeUnit.MILLISECONDS,
    new ArrayBlockingQueue<>(500),            // bounded
    new ThreadFactoryBuilder().setNameFormat("orders-io-%d").build(),   // named threads help thread dumps
    new ThreadPoolExecutor.CallerRunsPolicy());   // saturation policy
```
Note: `ThreadPoolExecutor` only grows past core size when the queue is full - with an unbounded queue, max size is never used. (gated: unconfirmed, source is paywalled or blocked)

Saturation policies:
| Policy | Effect | Use |
|---|---|---|
| Abort (throw `RejectedExecutionException`) | fail fast; caller returns 503/429 | request handling with load shedding |
| CallerRuns | submitting thread runs the task: natural backpressure | producers that can slow down (batch ingestion) |
| Discard / DiscardOldest | silently drop | only for lossy work (metrics samples) |
| Block on submit (semaphore) | producer waits | pipelines with bounded memory |

## Separate pools (bulkheads)
CPU work, blocking I/O, and each critical downstream get their own pools so one slow dependency cannot starve everything. Never run blocking calls on an event-loop or `ForkJoinPool.commonPool()` (Java parallel streams and `CompletableFuture` defaults use it). Java 21 virtual threads remove pool sizing for blocking I/O, but you still need semaphores to bound concurrency to downstream resources.

## Saturation signals to monitor
Active threads vs max, queue depth, task wait time in queue (time from submit to start), rejection count, CPU utilisation. Micrometer `ExecutorServiceMetrics`, .NET `ThreadPool.PendingWorkItemCount` and `dotnet-counters` (thread pool queue length, starvation warnings), Go goroutine count.

## Verify
- [ ] Load test at 2x expected traffic: rejections happen fast and cleanly (429/503), latency of accepted requests stays bounded.
- [ ] Alert on queue wait time and rejection rate.
