---
id: computing-software.game-programming.game-engine-architecture.mutexes-spinlocks-and-condition-variables
name: mutexes-spinlocks-and-condition-variables
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, spinlock, mutex, condition-variable, game-programming]
level: practitioner
status: draft
description: "Choose engine locking primitives: OS mutex vs spinlock vs hybrid, correct spin loops with pause and backoff, condition variable usage and priority inversion."
sources: ["https://en.cppreference.com/w/cpp/thread/condition_variable", "https://rigtorp.se/spinlock/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mutexes, spinlocks and condition variables

**Goal:** pick and implement locks that don't burn cores, deadlock, or stall the frame.

## Choosing
- **OS mutex** (`std::mutex`, Windows `SRWLOCK`, futex-based on Linux): sleeps when contended. Default
  choice. SRWLOCK and futexes spin briefly before sleeping already.
- **Spinlock:** only for very short critical sections (a few instructions) with threads on separate
  cores, and never on systems that can oversubscribe (PC with other apps, many threads > cores).
  A preempted lock holder makes every spinner waste its time slice. Linus Torvalds and the
  rigtorp article both detail why user-space spinlocks often lose.
- **Lock-free/atomics:** for counters and single-producer queues; harder to get right.

## Correct spinlock (if you must)
```cpp
struct Spin { std::atomic<bool> f{false};
  void lock() {
    for (;;) {
      if (!f.exchange(true, std::memory_order_acquire)) return;
      while (f.load(std::memory_order_relaxed)) _mm_pause();   // test-and-test-and-set, spin on read
    }
  }
  void unlock() { f.store(false, std::memory_order_release); } };
```
Add exponential backoff and fall back to yield/sleep after N spins. ARM uses `__yield()` / `wfe`.
Note Intel Skylake+ made `pause` ~140 cycles; calibrate spin counts in time, not iterations.

## Condition variables
```cpp
std::unique_lock lk(m);
cv.wait(lk, [&]{ return !queue.empty() || quit; });   // predicate handles spurious wakeups
```
Modify the predicate state under the mutex, then `notify_one/all`. Missing the predicate or
notifying without changing state under the lock causes lost wakeups.

## Pitfalls
- Priority inversion: low-priority loader holds a lock the render thread needs.
- Lock ordering: acquire multiple locks in a global order; use `std::scoped_lock(a, b)`.
- Holding locks while calling callbacks or doing I/O.

## Verify
- Contention profiling (Tracy lockables `TracyLockable`, VTune Threading) shows wait time per lock;
  ThreadSanitizer for races and lock-order inversion reports.
