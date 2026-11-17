---
id: computing-software.software-engineering.java.forkjoinpool-and-recursivetask
name: forkjoinpool-and-recursivetask
category: computing-software
field: software-engineering
product: java
tags: [java, java-concurrency-core, forkjoinpool, recursivetask, work-stealing, common-pool, divide-and-conquer, managedblocker]
level: advanced
status: docs-checked
description: "Write divide-and-conquer tasks with RecursiveTask, use fork/compute/join correctly, size thresholds, and avoid blocking in the shared common pool."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ForkJoinPool.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/RecursiveTask.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ForkJoinPool and RecursiveTask

## Pattern
```java
class SumTask extends RecursiveTask<Long> {
    private static final int THRESHOLD = 10_000;   // tune by measurement
    private final long[] a; private final int lo, hi;
    SumTask(long[] a, int lo, int hi) { this.a = a; this.lo = lo; this.hi = hi; }
    @Override protected Long compute() {
        if (hi - lo <= THRESHOLD) { long s = 0; for (int i = lo; i < hi; i++) s += a[i]; return s; }
        int mid = (lo + hi) >>> 1;
        SumTask left = new SumTask(a, lo, mid), right = new SumTask(a, mid, hi);
        left.fork();                       // run asynchronously
        long r = right.compute();          // reuse this thread for the second half
        return left.join() + r;
    }
}
long total = ForkJoinPool.commonPool().invoke(new SumTask(data, 0, data.length));
```
`RecursiveTask<V>` is a recursive result-bearing `ForkJoinTask`; its `compute()` returns the result. The RecursiveTask Javadoc example does the same shape: a base case, a "too small to parallelize" case, then fork the left half, compute the right half locally ("perform about half the work locally") and join the left. Use `RecursiveAction` when there is no result; `ForkJoinTask.invokeAll(...)` also exists.

## Rules
1. Fork one half, compute the other directly, then join, as in the Javadoc example.
2. Pick a threshold below which you stop splitting; measure with JMH rather than trusting a rule of thumb.
3. Per the ForkJoinPool Javadoc, tasks should not normally entail blocking operations; keep them CPU-bound and free of shared mutable state.
4. `ForkJoinPool.commonPool()` is "appropriate for most applications" and is used by any `ForkJoinTask` not explicitly submitted to a specified pool. For isolated work create a dedicated pool (`new ForkJoinPool(parallelism)`; the no-arg constructor uses `Runtime.availableProcessors()`). If a task must block, wrap it in a `ForkJoinPool.ManagedBlocker` and call `ForkJoinPool.managedBlock(...)` so the pool can add compensating threads.

## Gotchas
- Common pool tuning system properties: `java.util.concurrent.ForkJoinPool.common.parallelism` (a non-negative integer) and `java.util.concurrent.ForkJoinPool.common.maximumSpares` (extra threads to maintain target parallelism, default 256).
- If a thread about to block on a join or ManagedBlocker cannot be replaced because the maximum pool size would be exceeded, the default is a `RejectedExecutionException` (unless a `saturate` predicate was given, in which case the pool runs with fewer runnable threads, which "might not ensure progress").
- Use balanced splits; a skewed split recurses deeply.

## Verify
Compare against a sequential loop for correctness on random arrays and with `-Djava.util.concurrent.ForkJoinPool.common.parallelism=1`; benchmark with JMH at several thresholds.

## Checked
Read the ForkJoinPool and RecursiveTask Javadoc (Java 21). Confirmed: common pool description, system properties and the maximumSpares default, constructors, ManagedBlocker/managedBlock, saturate behaviour, blocking advisory, RecursiveTask example shape. Removed (not on the cited pages): the "100-10,000 operations" threshold, "parallelism = CPUs - 1" default, parallel streams and CompletableFuture sharing the common pool, exception wrapping details, the virtual-threads advice, and the dev.java source (404).
Method: docs-only read of cited pages, 2026-11-08
