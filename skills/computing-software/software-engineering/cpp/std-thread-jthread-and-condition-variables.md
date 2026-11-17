---
id: computing-software.software-engineering.cpp.std-thread-jthread-and-condition-variables
name: std-thread-jthread-and-condition-variables
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-concurrency, std-thread, jthread, condition-variable, stop-token, mutex, data-race, cpp-threads]
level: practitioner
status: gated
description: "Use C++ threads safely: std::jthread with stop_token, mutex and scoped_lock, condition variables without lost wakeups, futures/async, and thread sanitizer checks."
sources:
  - https://en.cppreference.com/w/cpp/thread
  - https://en.cppreference.com/w/cpp/thread/jthread
  - https://en.cppreference.com/w/cpp/thread/condition_variable
  - https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-concurrency
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# std::thread, jthread and condition variables

**Goal:** correct multi-threaded C++ with RAII-managed threads, deadlock-free locking and reliable signalling.

## 1. Prefer std::jthread (C++20)
```cpp
std::jthread worker([](std::stop_token st) {
    while (!st.stop_requested()) {
        process_next();
    }
});
// destructor: request_stop() then join() automatically
```
A `std::thread` that is still joinable when destroyed calls `std::terminate`. jthread removes that footgun and adds cooperative cancellation.

## 2. Mutexes with RAII
```cpp
class Inventory {
    mutable std::mutex mu_;
    std::unordered_map<std::string, int> stock_;   // guarded by mu_
public:
    void add(const std::string& sku, int n) {
        std::scoped_lock lock(mu_);
        stock_[sku] += n;
    }
    int get(const std::string& sku) const {
        std::scoped_lock lock(mu_);
        auto it = stock_.find(sku);
        return it == stock_.end() ? 0 : it->second;
    }
};
void transfer(Account& a, Account& b, int amt) {
    std::scoped_lock lock(a.mu, b.mu);             // C++17; several mutexes are locked as if by std::lock (deadlock avoidance)
    ...
}
```
- Never call `lock()`/`unlock()` manually; never call unknown code (callbacks, virtuals) while holding a lock.
- `std::shared_mutex` + `std::shared_lock` for read-mostly data with significant read sections (gated: unconfirmed, source is paywalled or blocked).
- Clang's thread-safety analysis (`-Wthread-safety`, `GUARDED_BY` annotations) checks lock discipline at compile time (see the Clang docs) (gated: unconfirmed, source is paywalled or blocked).

## 3. Condition variables
```cpp
std::mutex m;
std::condition_variable_any cv;
std::deque<Job> q;

void push(Job j) {
    { std::scoped_lock lk(m); q.push_back(std::move(j)); }
    cv.notify_one();
}
std::optional<Job> pop(std::stop_token st) {
    std::unique_lock lk(m);
    if (!cv.wait(lk, st, [&]{ return !q.empty(); }))   // predicate form handles spurious wakeups; returns the last predicate result, so false after a stop
        return std::nullopt;
    Job j = std::move(q.front()); q.pop_front();
    return j;
}
```
- Always wait with a **predicate**; the state change must happen under the mutex, or a notify can be lost.
- `condition_variable_any` integrates with `stop_token` (C++20) so blocked waiters wake on stop.

## 4. Results across threads
`std::async(std::launch::async, f)` returns a `std::future`; if that future is not moved from or bound to a variable, its destructor blocks at the end of the full expression until the task completes, making fire-and-forget calls synchronous. Futures obtained other than from `std::async` never block in their destructors. With the default policy it is implementation-defined whether the task runs concurrently or deferred. `std::promise`/`std::packaged_task` for manual plumbing. C++20 `std::latch`, `std::barrier`, `std::counting_semaphore` for coordination.

## 5. Atomics
`std::atomic<int>` for counters and flags; the sequentially consistent default order is the safe choice (check the memory_order docs) (gated: unconfirmed, source is paywalled or blocked). Weaker orders (acquire/release) only with a documented reason and review.

## Gotchas
- Data races on non-atomic variables are undefined behaviour, not "just stale values".
- Capturing locals by reference in a thread lambda that outlives the scope is use-after-free; jthread joining at scope exit helps.
- Exceptions escaping a thread function call `std::terminate` (gated: unconfirmed, source is paywalled or blocked); catch inside and transfer via promise/future.
- Oversubscription: creating a thread per task; use a pool sized to the hardware (`std::thread::hardware_concurrency()` is a hint).

## Verify
- Tests built with `-fsanitize=thread` (TSan) run clean under stress loops, and shutdown via `request_stop()` completes promptly with no hangs.

## Checked

2026-11-02. Checked against cppreference pages for std::jthread, std::thread destructor, std::scoped_lock, std::async and condition_variable_any::wait. Confirmed: jthread (C++20) destructor requests stop then joins, passes a stop_token as first argument, joinable std::thread destructor calls std::terminate, scoped_lock (C++17) multi-mutex deadlock avoidance as if by std::lock, async future-destructor blocking note, cv_any stop_token wait return value. Fixed: the async future blocking claim made precise. Gated: shared_mutex, Clang thread-safety, memory-order default, exceptions escaping threads, hardware_concurrency, not fetched.

Method: documentation only; no commands were run.
