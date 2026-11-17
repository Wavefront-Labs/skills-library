---
id: computing-software.software-engineering.concurrency.immutability-and-safe-publication
name: immutability-and-safe-publication
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, locking, immutability, safe-publication, final-fields, volatile, copy-on-write, thread-confinement, java-memory-model]
level: advanced
status: draft
description: "Share data between threads without locks by making it immutable and publishing it safely (final fields, volatile/atomic references, copy-on-write snapshots)."
sources: ["Java Concurrency in Practice (Goetz et al.), ch3 Sharing Objects", "https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html#jls-17.5", "https://go.dev/ref/mem", "https://en.cppreference.com/w/cpp/atomic/memory_order"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Immutability and safe publication

**Goal:** the cheapest thread safety is no shared mutable state. Make objects immutable
and hand them to other threads in a way that guarantees they see the fully constructed
object.

## Immutable objects (JCIP definition)
- State cannot change after construction.
- All fields are final (Java) / readonly (C#) / const (C++) / never written after init.
- Properly constructed: `this` does not escape the constructor (no registering
  listeners or starting threads from the constructor).
Immutable objects are thread-safe without synchronisation, can be shared freely and
cached. Deeply immutable means nested collections are unmodifiable copies too.

## Safe publication
Even a correct object can be seen half-initialised by another thread if the REFERENCE
is published unsafely (a plain non-volatile field written by one thread and read by
another). Safe ways:
- Static initialiser / class init (`static final Config C = load();`).
- `volatile` field or `AtomicReference` (Java), `Volatile`/`Interlocked` (C#),
  `std::atomic<std::shared_ptr<T>>` with release/acquire (C++20), `atomic.Pointer[T]` (Go).
- Storing into a properly locked field, or into a concurrent collection
  (ConcurrentHashMap, BlockingQueue put/take hand-off).
- Java `final` fields have special guarantees: a properly constructed object's final
  fields are visible to any thread that obtains a reference, even via a data race.

## The snapshot pattern (copy-on-write)
Readers never lock; writers build a new immutable version and swap the reference:
```java
private final AtomicReference<Routes> routes = new AtomicReference<>(Routes.empty());
Route lookup(String path) { return routes.get().match(path); }       // lock-free read
void addRoute(Route r) { routes.updateAndGet(old -> old.with(r)); }   // copy + CAS
```
Ideal for config, routing tables, feature flags: read constantly, written rarely.
Rust: `arc-swap`; Go: `atomic.Pointer`; .NET: `ImmutableDictionary` + `Interlocked.Exchange`.

## Thread confinement (the other lock-free option)
State touched by only one thread (event loop, actor, goroutine owning a map) needs no
synchronisation; hand off ownership via queues/channels.

## Pitfalls
- "Effectively immutable" objects (never modified in practice) still need safe publication.
- Unmodifiable views (`Collections.unmodifiableList(list)`) over a list someone else still mutates are not immutable.
- Lazy caches inside "immutable" objects (`hashCode` caching) must be benign races or synchronised.

## Verify
- [ ] Shared fields are final/volatile/atomic or guarded; reviewed with the race detector / TSan / jcstress.
- [ ] Read-mostly shared structures use snapshot swapping instead of reader locks where contention showed up.
