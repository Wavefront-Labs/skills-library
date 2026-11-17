---
id: computing-software.software-engineering.cpp.floating-point-random-engines-and-numeric-algorithms
name: floating-point-random-engines-and-numeric-algorithms
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-numerics, cpp-nu-random, cpp-nu-numeric, std-random, mt19937, std-reduce, std-accumulate, random-number-engines]
level: practitioner
status: docs-checked
description: "Numerics in C++: choosing std::random engines and seeding with random_device and seed_seq, and std::reduce versus std::accumulate for floating-point sums."
sources: ["https://en.cppreference.com/w/cpp/numeric/random", "https://en.cppreference.com/w/cpp/algorithm/reduce"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Random engines and numeric algorithms

## Random numbers
Three pieces: a uniform random bit generator (URBG), engines that are pseudo-random URBGs seeded from data, and distributions that post-process URBG output into a defined probability distribution.

```cpp
#include <random>
std::random_device r;                                   // seed source
std::default_random_engine e1(r());
std::uniform_int_distribution<int> uniform_dist(1, 6);
int roll = uniform_dist(e1);
```
- Engine trade-offs per the reference: linear congruential is moderately fast with very small state; Mersenne twister is slower with larger state but has the longest non-repeating sequence with desirable spectral characteristics; subtract-with-carry is very fast but needs more state and sometimes has less desirable spectral characteristics. `philox_engine` (C++26) is counter-based, for massively parallel Monte-Carlo work.
- Predefined engines include `minstd_rand0`, `minstd_rand`, `mt19937`, `mt19937_64`, `ranlux24`, `ranlux48`, `knuth_b`. `default_random_engine` is an implementation-defined type.
- `std::random_device` is non-deterministic, but implementations may use a pseudo-random engine if non-deterministic generation is not supported.
- `std::seed_seq` is a general-purpose bias-eliminating scrambled seed sequence generator; the reference example fills one from several `random_device` calls.
- None of the standard engines is cryptographically secure; use a crypto library (the page cites OpenSSL `RAND_bytes`).
- The C `rand`/`srand`/`RAND_MAX` functions are available but "not recommended".
- Engine adaptors (`discard_block_engine`, `independent_bits_engine`, `shuffle_order_engine`) change the spectral characteristics of an underlying engine.

## std::reduce versus std::accumulate (C++17, `<numeric>`)
```cpp
std::accumulate(v.begin(), v.end(), 0.0);                // left fold in order; init type is the result type
std::reduce(v.begin(), v.end(), 0.0);                    // same as reduce(first, last, init, std::plus<>())
std::reduce(std::execution::par, v.begin(), v.end(), 0.0);
```
- `reduce` reduces the range "possibly permuted and aggregated in unspecified manner": it behaves like `accumulate` except elements may be grouped and rearranged in arbitrary order.
- If the operation is not associative or not commutative (such as floating-point addition), the result is non-deterministic.
- `op` is applied in unspecified order to dereferenced elements, results of other `op` calls and `init`. Complexity is O(N) applications of `op`.
- Undefined behaviour if `T` is not MoveConstructible or `op` modifies an element or invalidates iterators in the range.
- Execution-policy overloads (feature macro `__cpp_lib_parallel_algorithm` = 201603L) throw `std::bad_alloc` if temporary memory for parallelisation is unavailable; an uncaught exception from the algorithm arguments calls `std::terminate` for standard policies.
- Pass an `init` of the right type: `0` versus `0.0` decides the accumulator type.

## Checked
Read the cppreference random library and std::reduce pages. The numeric/math page was not read and was dropped from sources, along with every floating-point claim: tolerance comparison, epsilon, fast-math flags, FMA contraction, Kahan summation, money advice. Removed as unconfirmed: thread-safety of engines, distribution portability across libraries, the old MinGW random_device remark, `rand() % n` bias, TBB linking, `abs` overload ambiguity.
Method: docs-checked 2026-11-09 against the cppreference random and reduce pages.
