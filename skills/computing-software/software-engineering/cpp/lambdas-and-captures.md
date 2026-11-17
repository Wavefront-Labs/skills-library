---
id: computing-software.software-engineering.cpp.lambdas-and-captures
name: lambdas-and-captures
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, modern-cpp, cpp-lambdas, captures, dangling-references, std-function, generic-lambdas, init-capture, this-capture]
level: practitioner
status: docs-checked
description: "Write C++ lambdas safely: capture modes, dangling-reference bugs with async callbacks, init-captures and move-only state, this capture, and std::function costs."
sources: ["https://en.cppreference.com/w/cpp/language/lambda", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#f52-prefer-capturing-by-reference-in-lambdas-that-will-be-used-locally-including-passed-to-algorithms", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#f53-avoid-capturing-by-reference-in-lambdas-that-will-be-used-non-locally-including-returned-stored-on-the-heap-or-passed-to-another-thread"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambdas and captures

**Goal:** use lambdas freely for algorithms and callbacks without dangling references,
which are the main lambda bug.

## Capture rules (Core Guidelines F.52 / F.53)
- Lambda used **locally** (passed to `std::sort`, `std::ranges::for_each`): capture by
  reference `[&]` is fine and cheap.
- Lambda **stored, returned, queued, or run on another thread**: capture by value or
  move. Never `[&]`.
```cpp
void schedule(Executor& ex, const Request& req) {
    ex.post([&req] { handle(req); });           // BUG: req dies when schedule returns
    ex.post([req] { handle(req); });            // copy
    ex.post([r = std::move(owned)] { handle(r); });   // init-capture: move-only types (unique_ptr)
}
```

## `this` capture
- `[=]` capturing `this` implicitly is deprecated in C++20; be explicit.
- `[this]` captures the pointer: dangling if the object dies before the callback runs.
- `[*this]` (C++17) copies the object.
- For async callbacks on objects owned by shared_ptr: capture `weak_from_this()` and lock:
```cpp
ex.post([w = weak_from_this()] { if (auto self = w.lock()) self->onTimer(); });
```

## Other features
```cpp
auto add = [](auto a, auto b) { return a + b; };          // generic lambda (C++14)
auto f = []<typename T>(std::vector<T> const& v) {...};    // template lambda (C++20)
auto counter = [n = 0]() mutable { return ++n; };          // mutable state in the closure
constexpr auto sq = [](int x) { return x * x; };           // constexpr-capable since C++17
```
Immediately invoked lambda for complex const initialisation:
`const auto cfg = [&] { Config c; ...; return c; }();`

## std::function vs templates
`std::function<void(int)>` type-erases: possible heap allocation, indirect call, and it
requires copyable callables (C++23 `std::move_only_function` lifts that). For hot paths
or algorithm parameters take a template / `auto` parameter instead. Use std::function
for storing heterogeneous callbacks.

## Gotchas
- Structured bindings could not be captured before C++20.
- Capturing a loop variable by reference in callbacks that run later captures the last value or a dead variable.
- Large captures by value copy on every copy of the lambda (std::function copies).

## Checked
2026-10-28: Confirmed on cppreference (lambda expression) and the C++ Core Guidelines F.52 and F.53 entries: capture-by-reference for local use, by value for non-local use, init-capture, explicit this capture. Removed the clang-tidy check family name.
Method: documentation only; no commands were run.

## Verify
- [ ] No `[&]` in lambdas passed to executors, threads, signals or stored members (and review).
- [ ] ASan run of async tests is clean (catches dangling captures as use-after-return/scope).
