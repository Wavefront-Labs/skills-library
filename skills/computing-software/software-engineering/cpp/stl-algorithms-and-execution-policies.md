---
id: computing-software.software-engineering.cpp.stl-algorithms-and-execution-policies
name: stl-algorithms-and-execution-policies
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, stl-algorithms, execution-policies, parallel-algorithms, ranges-algorithms, tbb, std-sort]
level: practitioner
status: docs-checked
description: "Replace raw loops with STL and std::ranges algorithms, know the key ones by task, and parallelise with execution policies (par, par_unseq) including TBB setup and pitfalls."
sources: ["https://en.cppreference.com/w/cpp/algorithm", "https://en.cppreference.com/w/cpp/algorithm/execution_policy_tag_t", "https://en.cppreference.com/w/cpp/algorithm/ranges", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-loop"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STL algorithms and execution policies

**Goal:** express intent with named algorithms (fewer off-by-one bugs, easier review) and get
multicore speed-ups on large data with one argument.

## Algorithms by task
| Task | Algorithm |
|---|---|
| find element / condition | `find`, `find_if`, `ranges::find(v, x, &T::id)` (projection) |
| any/all/none | `any_of`, `all_of`, `none_of` |
| count | `count`, `count_if` |
| transform into output | `transform` |
| sum / reduce | `std::accumulate`, `std::reduce`, `transform_reduce` |
| sort | `sort`, `stable_sort`, `partial_sort` (top-k), `nth_element` (k-th element) |
| sorted lookups | `lower_bound`, `upper_bound`, `equal_range`, `binary_search` |
| remove by condition | `remove_if` (then erase the tail) |
| unique | `sort` then `unique` then erase (or `ranges::unique`) |
| min/max | `min_element`, `max_element`, `minmax_element`, `std::clamp` |
| partition | `partition`, `stable_partition`, `partition_point` |
| set ops on sorted ranges | `set_union`, `set_intersection`, `set_difference`, `includes` |
| copy | `copy`, `copy_if`, `copy_n` |
| fill/generate | `fill`, `iota`, `generate` |
| compare | `equal`, `mismatch`, `lexicographical_compare` |

## Ranges versions (C++20)
```cpp
std::ranges::sort(people, {}, &Person::age);               // projection instead of lambda
auto it = std::ranges::find(people, "bob", &Person::name);
auto adults = people | std::views::filter([](auto& p){ return p.age >= 18; });
```
Ranges algorithms take the whole container, support projections, and return richer results
(`ranges::copy` returns both iterators). `std::ranges::fold_left` (C++23) is the ranges accumulate.

## Execution policies (C++17, `<execution>`)
```cpp
#include <execution>
std::sort(std::execution::par, v.begin(), v.end());
double total = std::transform_reduce(std::execution::par_unseq, xs.begin(), xs.end(), 0.0,
                                     std::plus<>{}, [](double x){ return x * x; });
```
| Policy | Meaning |
|---|---|
| `seq` | sequential |
| `par` | may run on multiple threads; element functions must not race |
| `par_unseq` | threads + vectorisation; no locks, no allocation, no blocking inside the function |
| `unseq` (C++20) | vectorised, single thread |

Rules:
- Element access functions must be free of data races; see the execution policy page for what `par_unseq` additionally forbids.
- Only worth it for large inputs or expensive per-element work; measure.

## Toolchain setup
- Support for parallel execution policies varies by standard library; check your toolchain's documentation.

## Verify
- [ ] Raw index loops replaced where an algorithm states intent.
- [ ] Parallel versions benchmarked against `seq` on production-size data.
- [ ] TSan clean for par element functions; parallel backend verified in your toolchain.

## Checked

- Date: 2026-10-28
- Confirmed on cppreference (algorithm, execution_policy_tag_t, algorithm/ranges pages): the algorithm names listed, ranges::fold_left (C++23), execution policies seq/par/par_unseq/unseq (C++20), Core Guidelines page.
- Removed: TBB/libstdc++ toolchain claims, element-count threshold, std::terminate and reduce-associativity claims (not on the fetched pages), clang-tidy check names, erase_if row, back_inserter, complexity note.
Method: documentation only; no commands were run.
