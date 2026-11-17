---
id: computing-software.software-engineering.cpp.scoped-lock-and-mutex-patterns
name: scoped-lock-and-mutex-patterns
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-concurrency, cpp-cc-locks, scoped-lock, mutex, deadlock, unique-lock, shared-mutex, scoped-lock-mutex]
level: practitioner
status: docs-checked
description: "Lock correctly in C++: std::scoped_lock for multiple mutexes, naming lock objects, condition waits with a condition, and not holding locks across callbacks."
sources: ["https://en.cppreference.com/w/cpp/thread/scoped_lock", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#cp-concurrency"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# scoped_lock and mutex patterns

```cpp
class Bank {
  struct Account { std::mutex m; long balance = 0; };
public:
  void transfer(Account& from, Account& to, long amt) {
    if (&from == &to) return;                       // do not pass the same mutex twice
    std::scoped_lock lock(from.m, to.m);            // C++17: deadlock avoidance as if by std::lock
    from.balance -= amt; to.balance += amt;
  }
};
```

## Choosing the lock type
| Need | Use |
|---|---|
| Lock one or more mutexes for a scope | `std::scoped_lock`: takes ownership on construction, releases on scope exit; with several mutexes it uses a deadlock avoidance algorithm as if by `std::lock` |
| Deferred locking, condition variables | `std::unique_lock` with `std::defer_lock` (cppreference's second equivalent of `scoped_lock`, "if unique_locks are needed, e.g. for condition variables") |

CP.21: use `std::lock()` or `std::scoped_lock` to acquire multiple mutexes; two threads taking `m1, m2` and `m2, m1` with separate `lock_guard`s "is asking for deadlock".

CP.42: do not wait without a condition, because a bare wait can miss a wakeup or wake to find no work.

## Rules
- CP.20: use RAII, never plain `lock()`/`unlock()`.
- CP.22: never call unknown code (a callback) while holding a lock; if you do not know what it does you risk deadlock.
- CP.43: minimise time spent in a critical section.
- CP.50: define a mutex together with the data it guards (a struct holding the mutex and the data, or `synchronized_value<T>` where available).

## Gotchas
- CP.44: name your `lock_guard`s and `unique_lock`s. `lock_guard<mutex> {m2};` creates an unnamed temporary that locks and immediately unlocks, and `unique_lock<mutex>(m1);` declares a default-constructed local named `m1` that shadows the global mutex and locks nothing.

## Verify
- [ ] A stress test with multiple threads and opposing lock orders does not deadlock.

## Checked
2026-11-03. Confirmed on cppreference std::scoped_lock (semantics, C++17, equivalent `lock_guard`/`unique_lock` code) and Core Guidelines CP.20-CP.22, CP.42-CP.44, CP.50. Removed: the UB claim for locking one mutex twice, `shared_mutex`/`shared_lock`/`recursive_mutex` advice, Clang thread-safety annotations, atomic and latch/barrier notes, the `shared_mutex` starvation claim, the RAII exception-safety note, ThreadSanitizer and `-Wthread-safety` checks.
Method: documentation only; no commands were run.
