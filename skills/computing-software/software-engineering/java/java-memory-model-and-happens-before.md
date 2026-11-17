---
id: computing-software.software-engineering.java.java-memory-model-and-happens-before
name: java-memory-model-and-happens-before
category: computing-software
field: software-engineering
product: java
tags: [java, java-concurrency-core, happens-before, java-memory-model, visibility, safe-publication, double-checked-locking, data-race]
level: advanced
status: docs-checked
description: "Reason about visibility and ordering with the Java Memory Model: happens-before edges, final field guarantees, volatile double-checked locking, and racy flags."
sources: ["https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java Memory Model and happens-before

The Java Memory Model (JLS chapter 17) defines when a read is guaranteed to see a write: the write must **happen-before** the read. Without such an edge a thread may see stale or reordered values.

## Happens-before edges that matter
1. Each action in a thread happens-before every later action of that thread in program order.
2. An unlock of a monitor (`synchronized` exit) happens-before every later lock of the same monitor.
3. A write to a `volatile` field happens-before every later read of that field.
4. A call to `Thread.start()` happens-before any action in the started thread; all actions in a thread happen-before another thread successfully returns from `join()` on it.
5. Actions before submitting a `Runnable` to an `Executor` happen-before its execution begins; actions of a computation happen-before `Future.get()` returns in another thread.
6. Actions before placing an object into a concurrent collection happen-before actions after accessing or removing it in another thread.
7. Releasing synchronizer methods (`Lock.unlock`, `Semaphore.release`, `CountDownLatch.countDown`) happen-before a later successful acquire on the same synchronizer.
8. Final fields: a thread that only sees a reference to an object after its constructor has finished is guaranteed to see the correctly initialised values of its `final` fields (JLS 17.5). Letting `this` escape from the constructor voids that.
The relation is transitive.

## Classic bug and fix
```java
class Holder { static Helper h;              // racy: no happens-before between the write and another thread's read
    static Helper get() { if (h == null) { h = new Helper(); } return h; } }
```
Double-checked locking is correct when the field is `volatile`:
```java
private static volatile Helper h;
static Helper get() { Helper r = h; if (r == null) synchronized (Holder.class) { r = h; if (r == null) h = r = new Helper(); } return r; }
```
A stop flag needs `volatile` (or `AtomicBoolean`): JLS 17.3 shows a loop on a non-volatile `done` field that may never terminate.

## Gotchas
- `volatile` gives visibility and ordering, **not atomicity** of `count++`; use `AtomicInteger`/`LongAdder`.
- A single write to a non-volatile `long` or `double` is treated as two separate 32-bit writes (JLS 17.7), so a reader can see a torn value; declare shared `long`/`double` fields `volatile`.
- Final fields let a thread-safe immutable object be seen as immutable even when its reference is passed through a data race, but only if `final` is used correctly.

## Verify
Review code for any field accessed from several threads without an edge from the list above.

## Checked
2026-11-09. Confirmed against JLS 17 (se21) and the java.util.concurrent package summary (memory consistency properties): the happens-before edges for monitors, volatile, start/join, executors, futures, concurrent collections and synchronizers; the final-field guarantee; the non-volatile long/double two-write rule; the non-volatile `done` flag example.
Removed: the initialization-on-demand holder and static-initializer idioms, the AtomicReference/lock publication list, the JIT-hoisting and x86-versus-ARM remarks and the jcstress advice (not stated by the cited pages), and the shipilev.net source (does not cover them).
Method: documentation only; no commands were run.
