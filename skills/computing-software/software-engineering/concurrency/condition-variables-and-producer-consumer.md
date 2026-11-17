---
id: computing-software.software-engineering.concurrency.condition-variables-and-producer-consumer
name: condition-variables-and-producer-consumer
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, locking, producer-consumer, condition-variables, spurious-wakeup, lost-wakeup, bounded-buffer, blocking-queue, monitors]
level: advanced
status: docs-checked
description: "Coordinate threads with condition variables correctly (predicate loops, spurious and lost wakeups, notify vs notify_all) or replace them with blocking queues."
sources: ["https://en.cppreference.com/w/cpp/thread/condition_variable", "https://docs.python.org/3/library/threading.html#condition-objects", "https://pkg.go.dev/sync#Cond"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Condition variables and producer-consumer

**Goal:** make threads wait for a state change without busy-waiting, and without the
classic lost-wakeup and spurious-wakeup bugs.

## Prefer a ready-made queue
Most producer-consumer needs are met by a bounded blocking queue from your language's
standard library. Bounded capacity gives backpressure. Write condition-variable code only
for custom synchronisers.

## The correct pattern (C++)
```cpp
std::mutex m; std::condition_variable not_empty, not_full;
std::deque<Job> q; const size_t cap = 100;

void put(Job j) {
    std::unique_lock lk(m);
    not_full.wait(lk, [&] { return q.size() < cap; });   // predicate form loops internally
    q.push_back(std::move(j));
    lk.unlock();
    not_empty.notify_one();
}
Job take() {
    std::unique_lock lk(m);
    not_empty.wait(lk, [&] { return !q.empty(); });
    Job j = std::move(q.front()); q.pop_front();
    lk.unlock();
    not_full.notify_one();
    return j;
}
```

## Rules
1. **Always wait in a loop on a predicate** (`while (!cond) cv.wait(lk);`). A wait can end by
   notification, timeout or spurious wakeup (cppreference), and the condition that prompted
   a notify may no longer hold when you run (Python threading docs; Go `sync.Cond` docs say
   to Wait in a loop).
2. **Change the predicate state while holding the same mutex** the waiter uses, even if
   the variable is atomic (cppreference); notifying may happen after releasing the lock.
3. **notify_one vs notify_all**: decide whether one state change interests one waiter or
   several. Adding one item to a buffer needs to wake only one consumer (Python docs); use
   `notify_all` when several waiters may be able to proceed.
4. Use timed waits (`wait_for`) where liveness matters, and recheck the predicate after
   a timeout.
5. Shutdown: a `closed` flag in the predicate, set under the lock, followed by
   `notify_all`, so waiters exit.

## Verify
- [ ] Every wait is inside a predicate loop or uses the predicate overload.
- [ ] Stress test with many producers/consumers and a shutdown in the middle completes without hangs.

## Checked
2026-11-01. Confirmed against the cppreference `std::condition_variable` page (mutex-protected modification, notify after unlock allowed, spurious wakeup, predicated overloads), the Python `threading` Condition docs (loop on condition, `wait_for`, notify vs notify_all) and the Go `sync` docs (Wait in a loop). Removed: the per-language queue list, Java wait/notify and `java.util.concurrent` notes, the lost-wakeup explanation and the book citation.
Method: documentation only; no commands were run.
