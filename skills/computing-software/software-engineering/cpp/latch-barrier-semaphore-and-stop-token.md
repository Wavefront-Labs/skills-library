---
id: computing-software.software-engineering.cpp.latch-barrier-semaphore-and-stop-token
name: latch-barrier-semaphore-and-stop-token
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, std-latch, std-barrier, std-counting-semaphore, stop-token, jthread, c++20, concurrency]
level: advanced
status: gated
description: "Coordinate C++20 threads with std::latch, std::barrier, counting/binary semaphores, and cooperative cancellation via jthread, stop_token, stop_callback and condition_variable_any."
sources: ["https://en.cppreference.com/w/cpp/thread/latch", "https://en.cppreference.com/w/cpp/thread/barrier", "https://en.cppreference.com/w/cpp/thread/counting_semaphore", "https://en.cppreference.com/w/cpp/thread/stop_token", "https://en.cppreference.com/w/cpp/thread/condition_variable_any/wait"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C++20 latch, barrier, semaphore and stop_token

**Goal:** replace hand-rolled mutex+condition-variable coordination with the C++20 primitives,
and make threads stoppable without ad-hoc atomic flags.

## std::latch: one-shot countdown
```cpp
#include <latch>
std::latch ready{n_workers};
for (int i = 0; i < n_workers; ++i)
    workers.emplace_back([&] { init_thread_local(); ready.count_down(); do_work(); });
ready.wait();              // main continues once every worker initialised
```
- `count_down(n)` (non-blocking decrement), `wait()`, `try_wait()` (tests whether the counter is zero), `arrive_and_wait()` (count down then block until zero - a start gate for N threads). Added in C++20.
- Single use; cannot be reset.

## std::barrier: reusable phase synchronisation
```cpp
#include <barrier>
std::barrier sync(n_threads, []() noexcept { swap_buffers(); });   // completion runs once per phase
auto worker = [&](int id) {
    for (int step = 0; step < steps; ++step) {
        compute_slice(id);
        sync.arrive_and_wait();      // all threads finish step before any starts the next
    }
};
```
- The completion function must be nothrow-invocable (`std::is_nothrow_invocable_v<CompletionFunction&>`); it runs exactly once per phase, in the thread whose `arrive`, `arrive_and_drop` or `wait` call brings the expected count to zero.
- `arrive_and_drop()` lets a thread leave permanently: it reduces the expected count for the current phase and for all later phases.

## Semaphores
```cpp
#include <semaphore>
std::counting_semaphore<16> slots{4};    // at most 4 concurrent holders
void use_db() {
    slots.acquire();
    auto release = gsl::finally([&]{ slots.release(); });   // or a small RAII guard
    query();
}
std::binary_semaphore signal{0};          // = counting_semaphore<1>
// producer: signal.release();  consumer: signal.acquire();
```
- `try_acquire()` (can spuriously fail), `try_acquire_for(d)`, `try_acquire_until(t)`.
- No thread ownership: unlike `std::mutex`, acquiring and releasing may happen on different threads, which makes it suitable for signalling between threads. `acquire`/`release` are explicit calls; write your own RAII guard.
- The template parameter `LeastMaxValue` is the minimum guaranteed max, not the actual max (`max()` may be larger) and not the initial count; the initial count is the constructor argument. `binary_semaphore` is `counting_semaphore<1>` and may be implemented more efficiently.

## Cooperative cancellation: jthread + stop_token
```cpp
std::jthread poller([](std::stop_token st) {
    while (!st.stop_requested()) { poll_once(); std::this_thread::sleep_for(100ms); }
});
// destructor: request_stop() then join(); or call poller.request_stop() explicitly
```
- `std::jthread` passes its own token if the callable's first parameter is `std::stop_token` (jthread semantics: gated: unconfirmed, source is paywalled or blocked).
- Interruptible waits with `std::condition_variable_any`:
```cpp
std::unique_lock lk(m);
if (!cv.wait(lk, st, [&] { return !queue.empty(); })) return;   // returns the last result of the predicate; false means a stop was requested first
```
  (The `stop_token` overloads are documented on `std::condition_variable_any`; for plain `std::condition_variable` confirm in the standard library docs) (gated: unconfirmed, source is paywalled or blocked)
- `std::stop_callback cb(st, [&]{ socket.close(); });` runs when stop is requested - unblocks
  blocking I/O that does not know about tokens. It runs on the thread that successfully calls `request_stop()`, or immediately on the constructing thread if stop was already requested; if the callback throws, `std::terminate` is called.
- `std::stop_source` creates tokens for your own task systems; pass tokens down call chains.

## Choosing
| Need | Primitive |
|---|---|
| wait for N events once | latch |
| repeated lockstep phases | barrier |
| limit concurrency / signal | counting/binary semaphore |
| stop a thread | jthread + stop_token |
| complex state predicates | mutex + condition_variable(_any) |

## Verify
- [ ] Every thread loop observes a stop_token or other shutdown signal.
- [ ] Semaphore releases are RAII-guarded on all paths.
- [ ] TSan clean; stress test with many iterations of the barrier/latch paths.

## Checked

2026-11-02. Checked against cppreference pages for std::latch, std::barrier, std::counting_semaphore, std::condition_variable_any::wait and std::stop_callback. Confirmed: latch member functions and single-use nature, barrier completion function requirements and once-per-phase execution, `arrive_and_drop` effect, semaphore LeastMaxValue meaning, thread-independent acquire/release, binary_semaphore alias, spurious `try_acquire` failure, cv_any stop_token overload and return value, stop_callback invocation thread rules. Fixed: noexcept wording, LeastMaxValue described as the max, return-value comment. Gated: plain condition_variable having no stop_token overload and jthread behaviour, which were not fetched.

Method: documentation only; no commands were run.
