---
id: computing-software.software-engineering.cpp.coroutines-co-await-and-generator
name: coroutines-co-await-and-generator
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, cpp-coroutines, co-await, std-generator, promise-type, asio, cppcoro, async]
level: advanced
status: docs-checked
description: "Use C++20 coroutines: std::generator (C++23) for lazy sequences, co_await with library task types (Asio, cppcoro), promise_type basics, and lifetime traps."
sources: ["https://en.cppreference.com/w/cpp/language/coroutines", "https://en.cppreference.com/w/cpp/coroutine/generator", "https://think-async.com/Asio/asio-1.30.2/doc/asio/overview/composition/cpp20_coroutines.html", "https://lewissbaker.github.io/2017/11/17/understanding-operator-co-await"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coroutines (co_await / std::generator)

**Goal:** write lazy generators and asynchronous code in straight-line style, using library
coroutine types rather than hand-rolled machinery wherever possible.

## What the language gives you
A function is a coroutine if it uses `co_await`, `co_yield` or `co_return`. Its return type must
have a `promise_type` that controls behaviour. C++23 adds `std::generator`; for async tasks use a library,
for example Asio (`asio::awaitable`).

## Generators (C++23)
```cpp
#include <generator>
std::generator<std::uint64_t> fibonacci() {
    std::uint64_t a = 0, b = 1;
    while (true) { co_yield a; a = std::exchange(b, a + b); }
}
for (auto x : fibonacci() | std::views::take(10)) std::println("{}", x);
```
- Lazy: body runs only as the range is iterated. Works with ranges adaptors.
- `std::generator<const Node&>` yields references; `co_yield std::ranges::elements_of(child())`
  recursively yields a nested generator.

## Async with Asio
```cpp
asio::awaitable<void> session(asio::ip::tcp::socket sock) {
    std::array<char, 4096> buf;
    for (;;) {
        auto n = co_await sock.async_read_some(asio::buffer(buf), asio::use_awaitable);
        co_await asio::async_write(sock, asio::buffer(buf, n), asio::use_awaitable);
    }
}
asio::co_spawn(io_ctx, session(std::move(sock)), asio::detached);
```
Errors arrive as exceptions (`asio::system_error`) or, with `asio::as_tuple(asio::use_awaitable)`,
as returned error codes. Timeouts and cancellation: `asio::experimental::awaitable_operators`
(`co_await (read() || timer.async_wait())`) or cancellation slots.

## Mechanics in brief (for reading library code)
- `promise_type` provides `get_return_object`, `initial_suspend` (lazy tasks return
  `std::suspend_always`), `final_suspend` (must be `noexcept`), `return_value`/`return_void`,
  `yield_value`, `unhandled_exception`.
- An awaiter implements `await_ready`, `await_suspend(std::coroutine_handle<>)`, `await_resume`.
- The coroutine frame is heap-allocated unless the compiler elides it; custom `operator new`
  in the promise controls allocation.

## Lifetime traps (the real source of bugs)
- **Reference parameters dangle**: a coroutine taking `const std::string&` keeps the reference in
  its frame; if the caller's temporary dies before the coroutine resumes, it is use-after-free. Take
  parameters **by value** in coroutines that suspend.
- Lambdas that are coroutines: captures live in the lambda object, not the frame. If the lambda
  temporary is destroyed after the first suspension, captures dangle. Pass state as parameters
or keep the lambda alive.
- `this` in member coroutines: the object must outlive the coroutine; use `shared_from_this` in
  async servers.
- Destroying a suspended coroutine runs destructors of locals but not code after the suspension
  point - design cancellation accordingly.

## Verify
- [ ] Coroutine parameters are by value or have documented lifetime guarantees.
- [ ] ASan clean under tests that suspend and resume across caller scope exit.
- [ ] A library task type is used; no ad-hoc promise types without tests.

## Checked

- Date: 2026-10-28
- Confirmed on cppreference (coroutines, generator, enable_shared_from_this pages): promise_type members, final_suspend noexcept, std::generator (C++23), shared_from_this; Asio awaitable page.
- Removed: clang-tidy check names, library support matrix, list of third-party task libraries, symmetric-transfer and HALO claims, deducing-this suggestion.
Method: documentation only; no commands were run.
