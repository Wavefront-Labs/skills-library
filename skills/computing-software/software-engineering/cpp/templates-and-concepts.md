---
id: computing-software.software-engineering.cpp.templates-and-concepts
name: templates-and-concepts
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, modern-cpp, cpp20, cpp-concepts, cpp-templates, requires-clause, constraints, sfinae, abbreviated-templates, template-errors]
level: advanced
status: docs-checked
description: "Constrain C++ templates with C++20 concepts and requires-clauses instead of SFINAE, write custom concepts, and keep template code readable and debuggable."
sources: ["https://en.cppreference.com/w/cpp/language/constraints", "https://en.cppreference.com/w/cpp/concepts", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#t-templates-and-generic-programming"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Templates and concepts

**Goal:** generic C++ whose requirements are stated in the signature, so misuse gives a
one-line error instead of 300 lines of instantiation backtrace.

## Using standard concepts
```cpp
#include <concepts>
template <std::integral T>
T gcd(T a, T b) { while (b) { a %= b; std::swap(a, b); } return a; }

auto clamp01(std::floating_point auto x) { return std::clamp(x, decltype(x){0}, decltype(x){1}); }  // abbreviated template

template <std::ranges::input_range R>
  requires std::totally_ordered<std::ranges::range_value_t<R>>
auto max_of(R&& r) { return *std::ranges::max_element(r); }
```
Useful library concepts: `same_as`, `convertible_to`, `derived_from`, `integral`,
`floating_point`, `invocable<F, Args...>`, `predicate`, `regular`, `totally_ordered`,
`ranges::range`/`random_access_range`/`sized_range`.

## Writing a concept
```cpp
template <typename T>
concept Shape = requires(const T& s, double k) {
    { s.area() } -> std::convertible_to<double>;
    { s.scaled(k) } -> std::same_as<T>;
    typename T::id_type;
};
void draw(const Shape auto& s);
```
Guidelines (Core Guidelines T.20-T.26): express meaningful semantic concepts
(`Sortable`, `Number`), not single-syntax checks; prefer standard ones.

## Replacing SFINAE
```cpp
// old
template <typename T, typename = std::enable_if_t<std::is_integral_v<T>>> void f(T);
// new
template <std::integral T> void f(T);
// or inside: if constexpr (std::integral<T>) { ... } else { ... }
```
Overloads constrained by concepts are ordered by subsumption: the more constrained
overload wins, no `enable_if` tricks needed.

## Keeping templates sane
- `static_assert(Shape<Circle>);` next to each type intended to model a concept.
- Prefer `if constexpr` over tag dispatch and specialization for small branches.
- Avoid deep template metaprogramming; `constexpr` functions usually replace it.

## Verify
- [ ] Calling a constrained function with a wrong type produces "constraints not satisfied" naming the concept.
- [ ] `static_assert`s document which types satisfy each concept.

## Checked

- Date: 2026-10-28
- Confirmed on cppreference (constraints, concepts pages) and the Core Guidelines (T.20-T.26): standard concepts used, requires-expressions, subsumption ordering, SFINAE replacement.
- Removed: explicit-instantiation compile-time advice (not on the fetched pages).
Method: documentation only; no commands were run.
