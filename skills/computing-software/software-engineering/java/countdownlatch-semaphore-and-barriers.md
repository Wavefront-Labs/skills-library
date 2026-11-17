---
id: computing-software.software-engineering.java.countdownlatch-semaphore-and-barriers
name: countdownlatch-semaphore-and-barriers
category: computing-software
field: software-engineering
product: java
tags: [java, countdownlatch, java-semaphore, cyclicbarrier, phaser, synchronizers, java-concurrency]
level: practitioner
status: docs-checked
description: "Coordinate threads with java.util.concurrent synchronizers: CountDownLatch for one-shot gates, Semaphore for limiting access, CyclicBarrier and Phaser for phases."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CountDownLatch.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Semaphore.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Phaser.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CyclicBarrier.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CountDownLatch, Semaphore and barriers

**Goal:** pick the right synchronizer instead of hand-rolled `wait/notify`.

## CountDownLatch: wait for N events, once
```java
CountDownLatch ready = new CountDownLatch(services.size());
for (Service s : services) pool.submit(() -> { s.start(); ready.countDown(); });
if (!ready.await(30, TimeUnit.SECONDS)) throw new IllegalStateException("startup timed out");
```
- Cannot be reset. Count down in `finally` so a failing task does not hang the waiter forever.
- Test use: a start gate (`new CountDownLatch(1)`) releases many threads simultaneously to
  provoke races.

## Semaphore: limit concurrent access
```java
Semaphore permits = new Semaphore(10, true);     // fair: ordered acquisition, lower throughput
void call() throws InterruptedException {
    if (!permits.tryAcquire(2, TimeUnit.SECONDS)) throw new RejectedExecutionException("busy");
    try { client.send(); }
    finally { permits.release(); }                // always in finally
}
```
Not owned by a thread (any thread may release) - a release without acquire silently grows the
permit count. Great for capping calls to a fragile downstream, including from virtual threads
(where pool size no longer limits concurrency).

## CyclicBarrier: N threads meet, repeatedly
```java
CyclicBarrier barrier = new CyclicBarrier(workers, () -> mergeResults());   // runs once per trip
// in each worker loop:
computeChunk(); barrier.await();     // all wait, barrier action runs, next phase starts
```
If one thread is interrupted or times out, the barrier breaks and others get
`BrokenBarrierException`.

## Phaser: dynamic parties and phases
```java
Phaser phaser = new Phaser(1);               // register self
for (Task t : tasks) {
    phaser.register();
    pool.submit(() -> { t.phaseOne(); phaser.arriveAndAwaitAdvance(); t.phaseTwo(); phaser.arriveAndDeregister(); });
}
phaser.arriveAndDeregister();
```
Use when the number of participants changes over time; otherwise CountDownLatch/CyclicBarrier
are simpler.

## Choosing
| Need | Tool |
|---|---|
| wait until N things happened | CountDownLatch |
| at most N at once | Semaphore |
| N threads in lock-step phases | CyclicBarrier / Phaser |
| wait for results of tasks | `invokeAll`, `CompletableFuture.allOf`, structured concurrency |
| one-time value handoff | `CompletableFuture` |

## Checked
2026-10-28: Confirmed in the CountDownLatch, Semaphore, Phaser and CyclicBarrier Javadoc: latch count cannot be reset, Semaphore fairness parameter, Phaser parties vary over time, BrokenBarrierException from CyclicBarrier. Added the CyclicBarrier page as a source.
Method: documentation only; no commands were run.

## Verify
- [ ] Every `await` has a timeout in production code; every `release`/`countDown` is in `finally`.
- [ ] Interrupted waits restore the interrupt flag.
