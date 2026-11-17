---
id: computing-software.software-engineering.cpp.array-tuple-pair-and-structured-bindings
name: array-tuple-pair-and-structured-bindings
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-stl, cpp-st-tuple, array-tuple-pair, std-array, std-tuple, std-pair, tuple-size]
level: practitioner
status: docs-checked
description: "Use std::array, std::pair and std::tuple well: fixed-size arrays over C arrays, tuple access and tie, apply, make_from_tuple, and when a named struct is better."
sources: ["https://en.cppreference.com/w/cpp/container/array", "https://en.cppreference.com/w/cpp/utility/tuple", "https://en.cppreference.com/w/cpp/utility/apply"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# array, tuple and pair

```cpp
std::array<int, 4> a{1, 2, 3, 4};          // aggregate; does not decay to T*
auto b = std::to_array({1, 2, 3});          // C++20: deduce the size from an initializer

std::pair<std::string, int> p{"x", 1};      // p.first, p.second
std::tuple<int, double, std::string> t{1, 2.5, "z"};
std::get<0>(t); std::get<std::string>(t);   // by index, or by type
auto [i, d, s] = t;                         // structured bindings (C++17)
std::tie(i, d, s) = t;                      // unpack into existing variables; std::ignore skips an element
auto t2 = std::make_tuple(1, 2);
std::apply([](auto... xs) { return (xs + ...); }, t2);     // call f with the tuple elements as arguments
auto w = std::make_from_tuple<Widget>(std::tuple{1, "a"}); // construct an object from a tuple of arguments
std::tuple_size_v<decltype(t)>;  std::tuple_element_t<0, decltype(t)>;
```
`std::array<T, N>` is an aggregate with the same semantics as a struct holding a C array `T[N]`, so `std::array<int, 3> a = {1, 2, 3};` works. Tuples compare lexicographically; `std::tuple_cat` concatenates tuples; `std::forward_as_tuple` creates a tuple of forwarding references and `std::tie` a tuple of lvalue references.

## When not to use
Return types with several meaningful fields are clearer as a named struct (`struct Result { int code; std::string msg; };`). Use tuples for generic code (argument packs, zip-like algorithms).

## Gotchas
- Zero-length `std::array` (N == 0): `begin() == end()`, and calling `front()` or `back()` is undefined.
- Default-initializing a `std::array` of a non-class type can leave indeterminate values (the implicit constructor follows aggregate initialization).
- `std::tie` and `std::forward_as_tuple` hold references: they dangle if the referent dies.
- `std::apply` accepts anything supporting `std::get` and `std::tuple_size` (before C++23 the page names `std::array` and `std::pair` as examples).

## Verify
- [ ] `static_assert(std::tuple_size_v<decltype(t)> == 3)` and a `tie`/`apply` round trip test.

## Checked
2026-11-08. Confirmed on cppreference std::array (aggregate semantics, no decay, N == 0 rule, indeterminate values on default initialization, to_array, lexicographic comparison), std::tuple (get by index and type, tie, ignore, forward_as_tuple, tuple_cat, tuple_size/tuple_element, lexicographic comparison) and std::apply (call with tuple elements, make_from_tuple listed alongside). Removed: at() exception type and operator[] UB wording, stack-size, missing-braces warning, structured-binding copy rules, tuple-as-map-key, std::span and sanitiser macro advice (not on the pages read).
Method: documentation only; no commands were run.
