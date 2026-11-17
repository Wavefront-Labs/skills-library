---
id: computing-software.software-engineering.java.blockingqueue-producer-consumer
name: blockingqueue-producer-consumer
category: computing-software
field: software-engineering
product: java
tags: [java, blockingqueue, producer-consumer, arrayblockingqueue, poison-pill, backpressure, java-concurrency]
level: practitioner
status: docs-checked
description: "Build producer-consumer pipelines with BlockingQueue: choosing Array/Linked/Synchronous/Priority queues, put/offer/take/poll semantics, poison pills and bounded backpressure."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/BlockingQueue.html", "https://jcip.net/", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BlockingQueue producer-consumer

**Goal:** hand work between threads safely with bounded memory and a clean shutdown.

## Choosing the queue
| Queue | Use |
|---|---|
| `ArrayBlockingQueue(n)` | bounded, fixed capacity; default choice |
| `LinkedBlockingQueue(n)` | bounded if you pass n (capacity defaults to `Integer.MAX_VALUE` otherwise!) |
| `SynchronousQueue` | no capacity: direct handoff |
| `PriorityBlockingQueue` | unbounded, ordered by comparator |
| `DelayQueue` | elements available after a delay (scheduling, retries) |
| `LinkedTransferQueue` | producers can wait until consumed (`transfer`) |

## Method semantics
| | throws | special value | blocks | times out |
|---|---|---|---|---|
| insert | `add` | `offer` -> false | `put` | `offer(e, t, unit)` |
| remove | `remove` | `poll` -> null | `take` | `poll(t, unit)` |
Null elements are rejected (null is the "empty" signal of `poll`).

## Pattern
```java
BlockingQueue<Job> q = new ArrayBlockingQueue<>(1_000);
static final Job POISON = new Job(null);

Runnable consumer = () -> {
    try {
        while (true) {
            Job j = q.take();
            if (j == POISON) { q.put(POISON); return; }   // re-insert so other consumers stop too
            process(j);
        }
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();              // restore flag and exit
    }
};

ExecutorService pool = Executors.newFixedThreadPool(4);
for (int i = 0; i < 4; i++) pool.submit(consumer);
for (Job j : jobs) q.put(j);       // blocks when full: backpressure on the producer
q.put(POISON);
pool.shutdown();
pool.awaitTermination(1, TimeUnit.MINUTES);
```
Alternatives to poison pills: interrupt consumers via `shutdownNow()`, or `poll(timeout)` with a
volatile `running` flag.

## Backpressure decisions
When the queue is full, pick deliberately: block the producer (`put`), drop (`offer` returns
false - count and log drops), or fail fast to the caller (HTTP 503). Unbounded queues turn a
slow consumer into an `OutOfMemoryError` later.

## Batch draining
```java
List<Job> batch = new ArrayList<>(100);
batch.add(q.take());                // wait for at least one
q.drainTo(batch, 99);               // then grab what's available, no blocking
writeAll(batch);
```

## Gotchas
- `size()` on concurrent queues is a snapshot; don't base control flow on it.
- Exceptions inside `process` kill the consumer loop if uncaught - catch per item.
- `ThreadPoolExecutor` already contains a queue; often a pool plus `submit` is enough.

## Verify
- [ ] Every queue has an explicit capacity.
- [ ] Shutdown test: all consumers exit and no items are lost or processed twice.

## Checked

- Date: 2026-10-28
- Confirmed in the Java SE 21 Javadoc (BlockingQueue, LinkedBlockingQueue, SynchronousQueue, LinkedTransferQueue pages, Executors page): method semantics table, null rejection, drainTo, default capacity of Integer.MAX_VALUE, SynchronousQueue has no capacity.
- Removed: lock-count and throughput remarks, newCachedThreadPool link.
Method: documentation only; no commands were run.
