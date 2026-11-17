---
id: computing-software.software-engineering.java.scheduledexecutorservice-and-delayqueue
name: scheduledexecutorservice-and-delayqueue
category: computing-software
field: software-engineering
product: java
tags: [java, java-concurrent-utils, scheduledexecutorservice, delayqueue, scheduleatfixedrate, scheduled-tasks]
level: practitioner
status: docs-checked
description: "Schedule periodic Java tasks with ScheduledExecutorService (fixed rate vs fixed delay), survive task exceptions, control shutdown policy, and use DelayQueue for expiry."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ScheduledExecutorService.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ScheduledThreadPoolExecutor.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/DelayQueue.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ScheduledExecutorService and DelayQueue

## Scheduling
```java
ScheduledExecutorService ses = Executors.newScheduledThreadPool(2);
ses.schedule(this::once, 10, TimeUnit.SECONDS);
ses.scheduleAtFixedRate(this::poll, 0, 5, TimeUnit.SECONDS);       // starts at 0, 5, 10, ...
ses.scheduleWithFixedDelay(this::sync, 0, 5, TimeUnit.SECONDS);     // 5 s from the end of one run to the start of the next
```
- Fixed rate: executions commence after `initialDelay`, then `initialDelay + period`, and so on. If one run takes longer than the period, later runs may start late but never run concurrently.
- Fixed delay: the delay is between the termination of one execution and the commencement of the next, so runs of varying length cannot bunch up.
- `period` / `delay` must be greater than zero (`IllegalArgumentException`). Zero or negative delays in `schedule` mean immediate execution.
- Arguments are relative delays, not dates; the Javadoc warns that a relative delay need not coincide with the wall-clock time because of network time synchronisation, clock drift or other factors.

## The silent-death rule
If any execution of a periodic task throws, subsequent executions are suppressed; the exception is only visible by calling `get` on the returned future (it throws `ExecutionException` with the exception as cause). Wrap the body if the task must keep running:
```java
Runnable safe = () -> { try { poll(); } catch (Throwable t) { log.error("poll failed", t); } };
```
(`log` is a placeholder for your logger.) A periodic task also ends when it is cancelled via its future or the executor terminates.

## Shutdown policies (ScheduledThreadPoolExecutor)
```java
ses.shutdown();
if (!ses.awaitTermination(10, TimeUnit.SECONDS)) ses.shutdownNow();
```
- By default `shutdown()` cancels future executions of existing periodic tasks (`setContinueExistingPeriodicTasksAfterShutdownPolicy`, default false) but existing delayed one-shot tasks still run (`setExecuteExistingDelayedTasksAfterShutdownPolicy`, default true).
- To drop pending one-shots on shutdown, cast to `ScheduledThreadPoolExecutor` and call `setExecuteExistingDelayedTasksAfterShutdownPolicy(false)`.
- A cancelled task is not removed from the work queue until its delay elapses unless `setRemoveOnCancelPolicy(true)` is set; the default can retain cancelled tasks without bound.

## DelayQueue for expiring items
`DelayQueue<E extends Delayed>` is an unbounded blocking queue. An element is expired when `getDelay(TimeUnit.NANOSECONDS)` returns zero or less. It rejects `null`.
```java
DelayQueue<Lease> q = new DelayQueue<>();   // Lease implements Delayed
Lease expired = q.take();                    // blocks until the head has expired
```
- `take()`, `poll()` and `remove()` only ever remove the **expired** head; `peek()` may return the head even when `take()` would still block; `size()` and the iterator count unexpired elements too.
- Implement `getDelay` from a monotonic deadline you control; `Delayed` elements must also define their ordering.

## Verify
Make a task throw on its second run and check that your wrapper logs and the schedule continues; use a short period and assert the run count after a bounded wait.

## Checked
2026-11-03. Confirmed against the Java SE 21 pages for ScheduledExecutorService, ScheduledThreadPoolExecutor and DelayQueue: fixed rate vs fixed delay semantics, non-overlap of late runs, exception suppresses later runs and surfaces through `get`, argument checks, shutdown policy defaults, setRemoveOnCancelPolicy, DelayQueue expiry semantics, null rejection and peek/size behaviour.
Removed (not in the pages read): the `java.util.Timer` comparison, the `Thread.ofPlatform()` factory line, "catch up" wording for late runs, claims about nanoTime and clock changes, Quartz and Spring `@Scheduled`, pool-sizing and lock gotchas, and the `compareTo` example body.
Method: documentation only; no commands were run.
