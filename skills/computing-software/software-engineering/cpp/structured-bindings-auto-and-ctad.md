---
id: computing-software.software-engineering.cpp.structured-bindings-auto-and-ctad
name: structured-bindings-auto-and-ctad
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, structured-bindings, ctad, auto, type-deduction, deduction-guides, decltype-auto, c++17]
level: practitioner
status: docs-checked
description: "Use C++ type deduction well: auto and its decay rules, decltype(auto), structured bindings for pairs/tuples/structs, class template argument deduction and deduction guides."
sources: ["https://en.cppreference.com/w/cpp/language/structured_binding", "https://en.cppreference.com/w/cpp/language/class_template_argument_deduction", "https://en.cppreference.com/w/cpp/language/auto", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-auto"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structured bindings, auto and CTAD

**Goal:** less repetitive type noise without accidental copies, dangling references or surprising
deduced types.

## auto rules
- `auto x = expr;` deduces like a by-value template parameter: **drops references and top-level
  const**, decays arrays and functions. `auto x = vec[0];` copies.
- `auto& x` / `const auto& x` binds a reference; `auto&& x` is a forwarding reference (binds to
  anything, used in range-for over proxy iterators like `vector<bool>`).
- `auto x{1};` is `int` (C++17); `auto x = {1};` is `std::initializer_list<int>`.
- Range-for: `for (const auto& e : v)` for read, `for (auto& e : v)` to modify, `for (auto e : v)`
  only for cheap-to-copy elements. Iterating a map by `const std::pair<std::string, int>&` (missing
  `const` on the key) silently copies every element; `const auto&` avoids it.
- Return type `auto` deduces by value; `decltype(auto)` preserves references - use it in forwarding
  wrappers: `decltype(auto) get() { return (member_); }` returns a reference because of the
  parentheses (and can dangle if you return a local that way).
- Good uses: iterators, lambdas, `make_unique`/casts where the type is on the right, long template
  types. Spell types when the type is the documentation (`std::chrono::seconds timeout = ..`).

## Structured bindings (C++17)
```cpp
for (const auto& [name, score] : scores) { ... }           // map elements
auto [it, inserted] = m.try_emplace(key, value);
auto [q, r] = std::div(17, 5);
struct Size { int w, h; };
auto [w, h] = get_size();
```
- Works for arrays, tuple-like types (`std::tuple`, `pair`, types specialising `std::tuple_size`/`get`)
  and structs with all public non-static members.
- The qualifiers apply to a hidden object, not to each name: `auto [a, b] = s;` copies `s` once;
  `auto& [a, b] = s;` binds into `s`. `const auto& [x, y] = f();` extends the temporary's lifetime.
- Names cannot be given individual types; `[[maybe_unused]]` applies to the whole declaration.
  Name unused parts.
- Since C++20, bindings can be captured by lambdas.

## CTAD (class template argument deduction)
```cpp
std::pair p{1, 2.0};                 // pair<int, double>
std::vector v{1, 2, 3};              // vector<int>
std::lock_guard lk{mtx};             // lock_guard<std::mutex>
std::array a{1, 2, 3};               // array<int, 3>
std::optional o{42};                 // optional<int>
```
- Traps: `std::vector v{other_vector};` deduces `vector<int>` (copy), not `vector<vector<int>>`;
  `std::vector v(5, 1)` vs `v{5, 1}` still differ. String literals deduce `const char*`:
  `std::vector v{"a", "b"}` is `vector<const char*>` - write `using namespace std::literals;` and
  `"a"s` for `std::string`.
- Deduction guides teach CTAD for your templates:
```cpp
template <class T> struct Buffer { Buffer(T* p, std::size_t n); };
template <class It> Buffer(It, It) -> Buffer<typename std::iterator_traits<It>::value_type>;
```
- Aggregates get CTAD in C++20 without guides.

## Checked
2026-10-28: Confirmed on cppreference (structured binding declaration, class template argument deduction, auto/placeholder type specifiers): by-value deduction drops references and top-level const, hidden object semantics of qualifiers, CTAD deduction guides and aggregate deduction. Removed the C++26 placeholder note and clang-tidy check names.
Method: documentation only; no commands were run.

## Verify
- [ ] Static-analysis suggestions about `auto` and range-for copies reviewed (do not blindly apply).
- [ ] No `auto` hiding a copy of a large object in a loop.
- [ ] CTAD-constructed containers checked for the intended element type in reviews.
