---
id: computing-software.software-engineering.java.locks-atomics-and-concurrent-collections
name: locks-atomics-and-concurrent-collections
category: computing-software
field: software-engineering
product: java
tags: [java, java-concurrency, reentrantlock, concurrenthashmap, java-atomics, longadder, readwritelock, stampedlock, synchronized, volatile, computeifabsent]
level: advanced
status: docs-checked
description: "Choose between synchronized, ReentrantLock, ReadWriteLock, atomics/LongAdder and concurrent collections in Java, with the compound-action traps each one has."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/package-summary.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locks, atomics and concurrent collections

**Goal:** protect shared state with the lightest correct tool and avoid the
check-then-act bugs that "thread-safe" collections do not prevent.

## Decision guide
| Situation | Tool |
|---|---|
| Single counter / flag updated by many threads | `AtomicLong`, `AtomicBoolean`; hot counters: `LongAdder` |
| Publish an immutable snapshot, readers never block | `volatile` reference or `AtomicReference` to immutable object |
| Map shared across threads | `ConcurrentHashMap` with atomic methods |
| Several fields must change together | `synchronized` block or `ReentrantLock` |
| Need tryLock/timeout/interruptible lock/fairness | `ReentrantLock` |
| Read-mostly data, long reads | `ReentrantReadWriteLock` or `StampedLock` optimistic reads |
| Producer/consumer hand-off | `BlockingQueue` (`ArrayBlockingQueue` bounded) |
| Listener lists, rarely modified | `CopyOnWriteArrayList` |

## ConcurrentHashMap: use the atomic operations
```java
// WRONG: race between get and put
if (!cache.containsKey(k)) cache.put(k, load(k));
// RIGHT
cache.computeIfAbsent(k, this::load);
counts.merge(word, 1L, Long::sum);
```
- The mapping function in `computeIfAbsent` runs while the update is in progress: keep it short,
  never update other mappings of the same map inside it, and avoid slow I/O.
- Size and iteration are weakly consistent; no `ConcurrentModificationException`, but no
  snapshot either.
- Nulls are not allowed as keys or values.

## ReentrantLock idiom
```java
lock.lock();
try { balance -= amt; ledger.add(entry); }
finally { lock.unlock(); }
```
Always unlock in `finally`. `Condition` objects (`lock.newCondition()`) replace
`wait/notify` and allow several wait sets.

## Virtual threads note
JEP 491 (delivered in JDK 24) removes most pinning of virtual threads when blocking inside `synchronized`; on older JDKs prefer `ReentrantLock` in code running on virtual threads.

## Atomics details
- Prefer the atomic classes' function-based update methods over hand-written `compareAndSet` loops; check their docs for retry behaviour.

## Verify
- [ ] No check-then-act sequences on concurrent collections (grep `containsKey` followed by `put`).
- [ ] jcstress or a stress test with many threads gives stable totals.
- [ ] Thread dumps under load show no long BLOCKED queues on a single lock.

## Checked

- Date: 2026-10-28
- Confirmed in the Java SE 21 API docs (concurrent, concurrent.atomic, ConcurrentHashMap, locks pages) and JEP 491: atomic classes and LongAdder, CHM null rule, weakly consistent iterators, compute functions must be short and must not update other mappings, JEP 491 delivered in JDK 24.
- Removed: bin-lock and deadlock wording, updateAndGet retry and LongAdder sum remarks.
Method: documentation only; no commands were run.
