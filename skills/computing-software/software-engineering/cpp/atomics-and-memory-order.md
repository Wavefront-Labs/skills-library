---
id: computing-software.software-engineering.cpp.atomics-and-memory-order
name: atomics-and-memory-order
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-concurrency, cpp-cc-atomics, std-atomic, memory-order, acquire-release, compare-exchange, lock-free, atomics-memory-order]
level: advanced
status: docs-checked
description: "Use std::atomic correctly: seq_cst default, acquire/release publication, relaxed counters, compare_exchange loops, lock-free checks and volatile."
sources: ["https://en.cppreference.com/w/cpp/atomic/memory_order", "https://en.cppreference.com/w/cpp/atomic/atomic"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atomics and memory order

If one thread writes to an atomic object while another reads it, the behaviour is well-defined; a concurrent read and write of a non-atomic object is a data race. `memory_order` controls ordering of *other* memory around atomic operations.

```cpp
std::atomic<int> hits{0};
hits.fetch_add(1, std::memory_order_relaxed);        // counter: only atomicity needed

// Publish data with release/acquire
int payload; std::atomic<bool> ready{false};
// producer
payload = 42;
ready.store(true, std::memory_order_release);        // all writes before this are visible to an acquirer that sees true
// consumer
while (!ready.load(std::memory_order_acquire)) {}
assert(payload == 42);

// CAS loop
int old = a.load();
while (!a.compare_exchange_weak(old, std::max(old, x))) {}   // compares with the expected value, exchanges if equal, loads the current value into old if not
```

## Choosing orders
- **`seq_cst`** (the strongest): loads acquire, stores release, read-modify-writes do both, plus a single total order in which all threads observe all modifications. cppreference notes it may be necessary for multiple-producer multiple-consumer cases where all consumers must see the producers' actions in the same order, and that once non-`seq_cst` operations enter the picture the sequential-consistency guarantee for the program is lost.
- **`relaxed`**: only atomicity, no ordering or synchronisation. cppreference's typical use is incrementing counters such as the `std::shared_ptr` reference counters; decrementing them needs acquire-release synchronisation with the destructor.
- **`acquire`/`release`**: a release store makes all writes before it visible to a thread that acquires the same atomic.
- `memory_order_consume` use is temporarily discouraged (C++17 until C++26) because its specification is being revised; since C++26 it has the same effect as acquire and is deprecated. Prefer acquire.
- `std::atomic_thread_fence` imposes stronger synchronisation than a consume operation; prefer the orders on the operations.

## Facilities
`is_lock_free()` and `is_always_lock_free` (C++17); `std::atomic_flag`, the lock-free boolean atomic type; C++20 `wait`, `notify_one` and `notify_all`, which block until notified and the value changes; C++20 `std::atomic<std::shared_ptr<U>>`; C++20 `std::atomic_ref`.

## Gotchas
- Compound operations on two atomics are not atomic together; use a mutex.
- `volatile` accesses are not atomic (a concurrent read and write is a data race) and do not order memory; they establish no inter-thread synchronisation.
- `std::atomic<T>` may be instantiated with any TriviallyCopyable type that is CopyConstructible and CopyAssignable; check `is_lock_free()` for the type you use.

## Verify
- [ ] `std::atomic<T>::is_always_lock_free` or `is_lock_free()` checked for each atomic type on the hot path.

## Checked
2026-11-03. Confirmed on cppreference std::memory_order (orderings, relaxed refcount note, consume discouraged, volatile section) and std::atomic (TriviallyCopyable requirement, `compare_exchange_*`, `wait`/`notify_*`, `is_always_lock_free`, `atomic<shared_ptr>`, `atomic_flag`, `atomic_ref`). Removed: the fetch_sub acq_rel plus acquire-fence recipe, the claim that consume is promoted to acquire, the ABA advice, spinning and yield advice, the x86-hides-bugs claim, the ThreadSanitizer, ARM and herd7/CDSChecker verification, and the claim that large T uses an internal lock.
Method: documentation only; no commands were run.
