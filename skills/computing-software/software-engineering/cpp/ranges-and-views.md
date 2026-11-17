---
id: computing-software.software-engineering.cpp.ranges-and-views
name: ranges-and-views
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, modern-cpp, cpp20, cpp-ranges, views, range-adaptors, projections, dangling, lazy-evaluation, ranges-to]
level: practitioner
status: docs-checked
description: "Use C++20 ranges: range algorithms with projections, lazy views pipelines, ranges::to (C++23), and the dangling/caching pitfalls of views."
sources: ["https://en.cppreference.com/w/cpp/ranges", "https://en.cppreference.com/w/cpp/algorithm/ranges", "https://en.cppreference.com/w/cpp/ranges/to"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ranges and views

**Goal:** shorter, safer algorithm calls and lazy pipelines, without the lifetime traps
views introduce.

## Range algorithms
```cpp
std::ranges::sort(users, {}, &User::age);                    // projection: sort by age
auto it = std::ranges::find(users, "bob", &User::name);
bool ok = std::ranges::all_of(xs, [](int x) { return x > 0; });
```
Pass the container, not begin/end; projections remove most comparator lambdas.

## Views pipelines (lazy)
```cpp
namespace v = std::views;
auto names = users
    | v::filter([](const User& u) { return u.active; })
    | v::transform(&User::name)
    | v::take(10);
for (const auto& n : names) print(n);                       // computed on iteration
auto vec = names | std::ranges::to<std::vector>();           // C++23 materialise
```
Useful views: `filter, transform, take, drop, take_while, reverse, keys, values,
iota, split, join, enumerate (C++23), zip (C++23), chunk (C++23), slide (C++23)`.

## Pitfalls
- **Dangling**: `auto v = get_vector() | v::filter(p);` is OK since C++20 (the
  temporary vector is moved into an `owning_view`), but views over `std::string_view` of a temporary string,
  or storing views beyond the life of their source, dangle. Algorithms returning
  iterators into rvalues give `std::ranges::dangling` (compile error on use), which is
  a feature.
- Do not modify elements in a way that changes a `filter` predicate result while iterating the view.
- `filter` views are not const-iterable; pass them by forwarding reference
  (`auto&&`) or by value, not `const&`.
- `transform` computes its element on every dereference; materialise if the work is expensive.
- Compile errors are long; build pipelines incrementally.

## Checked
2026-10-28: Confirmed on cppreference (ranges library, std::ranges::to, ranges algorithms): owning_view, ranges::to as C++23, view adaptor list including C++23 additions. Removed two behavioural claims about filter caching and double evaluation that no fetched page states.
Method: documentation only; no commands were run.

## Verify
- [ ] ASan clean on tests exercising pipelines (catches dangling).
- [ ] No views stored in members unless their source's lifetime is guaranteed longer.
