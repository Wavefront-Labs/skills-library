---
id: computing-software.software-engineering.cpp.std-async-futures-and-promises
name: std-async-futures-and-promises
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, std-async, std-future, std-promise, packaged-task, shared-future, concurrency, thread-pool]
level: practitioner
status: docs-checked
description: "Use std::async, futures, promises and packaged_task correctly: launch policies, blocking future destructors, exception propagation, wait_for timeouts and thread pools."
sources: ["https://en.cppreference.com/w/cpp/thread/async", "https://en.cppreference.com/w/cpp/thread/future", "https://en.cppreference.com/w/cpp/thread/promise", "https://en.cppreference.com/w/cpp/thread/packaged_task"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std::async, futures and promises

**Goal:** get a result (or exception) back from concurrent work safely, knowing the traps that
make std::async surprisingly synchronous.

## std::async
```cpp
#include <future>
auto f = std::async(std::launch::async, [](std::string path) { return load(path); }, "data.bin");
// ... other work ...
Data d = f.get();          // blocks until ready; rethrows any exception from the task
```
- **Always pass `std::launch::async`.** The default policy (`async | deferred`) lets the
  implementation run the task lazily on the thread that calls `get()` - possibly never in parallel,
  and `wait_for` then returns `future_status::deferred` forever in polling loops.
- **The future returned by std::async blocks in its destructor** until the task finishes. This
  line runs sequentially:
```cpp
std::async(std::launch::async, work1);   // temporary future destroyed here -> waits
std::async(std::launch::async, work2);
```
  Keep the futures in variables or a vector.
- Arguments are copied (decay-copied) into the task; use `std::ref` deliberately and make sure the
  referenced object outlives the task.

## future API
| Call | Behaviour |
|---|---|
| `get()` | wait, return value or rethrow; callable **once** (future becomes invalid) |
| `wait()` | wait without consuming |
| `wait_for(d)` / `wait_until(t)` | returns `ready`, `timeout`, or `deferred` |
| `valid()` | false after get() or for default-constructed |
| `share()` | `std::shared_future`: copyable, `get()` many times from many threads |
There is no cancellation and no continuation (`.then`) in std::future; use an atomic flag
for cancellation.

## promise: set a result from anywhere
```cpp
std::promise<int> p;
std::future<int> f = p.get_future();
std::jthread t([pr = std::move(p)]() mutable {
    try { pr.set_value(compute()); }
    catch (...) { pr.set_exception(std::current_exception()); }
});
int v = f.get();
```
- If a promise is destroyed without setting a value, `get()` throws `std::future_error` with
  `broken_promise`.
- `std::promise<void>` + `shared_future<void>` makes a one-shot "start" signal for many threads.
- Setting a value twice throws `std::future_error` (`future_errc::promise_already_satisfied`).

## packaged_task: wrap a callable for a queue
```cpp
std::packaged_task<int(int)> task([](int x) { return x * 2; });
std::future<int> f = task.get_future();
queue.push(std::move(task));     // a worker later calls task(21)
```
The usual building block for a hand-written thread pool returning futures. Its futures do **not**
block on destruction.

## Better options for real workloads
- A thread pool from a library you already use, or `std::packaged_task` plus a hand-written pool.
- Parallel STL algorithms for data parallelism.

## Verify
- [ ] Every `std::async` call specifies `std::launch::async` and stores its future.
- [ ] Exceptions from tasks are observed (`get()` called) on every path.
- [ ] TSan clean; shared state accessed by tasks is synchronised.

## Checked

- Date: 2026-10-28
- Confirmed on cppreference (async, future, promise, packaged_task, future_status, future_errc pages): launch policy behaviour, blocking destructor of the future returned by std::async, wait_for/future_status::deferred, broken_promise, promise_already_satisfied.
- Removed: per-implementation thread claims (MSVC), named thread-pool libraries, std::stop_token and std::execution/stdexec mentions.
Method: documentation only; no commands were run.
