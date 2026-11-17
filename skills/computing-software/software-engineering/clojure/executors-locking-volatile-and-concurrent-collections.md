---
id: computing-software.software-engineering.clojure.executors-locking-volatile-and-concurrent-collections
name: executors-locking-volatile-and-concurrent-collections
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, executors, thread-pool, locking, volatile, concurrent-hash-map, countdownlatch, semaphore, virtual-threads, java-util-concurrent, executors-locking-volatile, clojure-concurrency-jvm]
level: advanced
status: draft
description: "Use java.util.concurrent from Clojure: executors, locking, volatile!, ConcurrentHashMap, latches and semaphores, bound-fn conveyance, and virtual threads on newer JDKs."
sources: ["https://clojure.org/reference/vars", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JVM concurrency from Clojure

**Goal:** use the JDK's primitives where atoms and agents are not enough.

```clojure
(import '(java.util.concurrent Executors TimeUnit ConcurrentHashMap CountDownLatch Semaphore))
(def pool (Executors/newFixedThreadPool 8))
(def f (.submit pool ^Callable (fn [] (work))))        ; Clojure fns implement Callable and Runnable
(.get f 5 TimeUnit/SECONDS)
(.shutdown pool) (.awaitTermination pool 30 TimeUnit/SECONDS)

(def lock (Object.))
(locking lock (swap-state!))                            ; synchronized block
(def v (volatile! 0)) (vswap! v inc) @v                 ; single-thread-ish mutable cell, visible across threads
(def m (ConcurrentHashMap.)) (.computeIfAbsent m k (reify java.util.function.Function (apply [_ k] (make k))))
(def latch (CountDownLatch. 3)) (.countDown latch) (.await latch)
(def vthreads (Executors/newVirtualThreadPerTaskExecutor))   ; JDK 21+
```
- Use `bound-fn` / `bound-fn*` so dynamic bindings reach pool threads (`future` does this automatically).
- `locking` holds a monitor; do not block on I/O inside it; avoid nested locks.
- `volatile!` gives visibility but no atomicity (`vswap!` is not a CAS); use an atom for shared updates.
- Prefer immutable data plus atoms; reserve locks for interop with mutable Java objects.
- Always shut down executors you create; non-daemon threads keep the JVM alive.
- Thread names: set a `ThreadFactory` for debuggable pools.

## Failure modes
- Deadlock from nested `locking` in different orders.
- Pool exhaustion from blocking tasks in a small fixed pool.

## Self-check
Run 1000 tasks that increment an atom through a fixed pool and verify the exact total.
