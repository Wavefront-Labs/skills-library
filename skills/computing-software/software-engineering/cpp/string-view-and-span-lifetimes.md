---
id: computing-software.software-engineering.cpp.string-view-and-span-lifetimes
name: string-view-and-span-lifetimes
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, modern-cpp, cpp17, string-view, std-span, non-owning-views, dangling-references, lifetime, null-termination]
level: practitioner
status: docs-checked
description: "Use std::string_view and std::span as non-owning parameters without dangling, and avoid the null-termination and temporary-lifetime traps."
sources: ["https://en.cppreference.com/w/cpp/string/basic_string_view", "https://en.cppreference.com/w/cpp/container/span", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#sl-str-strings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# string_view and span lifetimes

**Goal:** cheap, flexible parameters for read-only strings and contiguous sequences,
without returning or storing views of dead memory.

## Use as parameters
```cpp
bool starts_with_http(std::string_view s) { return s.starts_with("http"); }  // accepts std::string, char*, literals
double mean(std::span<const double> xs);         // accepts vector, array, C array, subrange
void fill(std::span<std::byte> out);             // mutable view
```
Pass by value (they're two words). Core Guidelines: prefer `string_view`/`span` over
`const std::string&`/pointer+length for read-only parameters.

## Lifetime rules
Views do not own. They are valid only while the underlying storage is alive and
unmodified (no reallocation).
```cpp
std::string_view name() { std::string s = load(); return s; }      // dangling: s destroyed
std::string_view sv = std::string("temp");                          // dangling at end of statement
std::string_view sv = get_string();                                 // dangling if get_string returns by value
std::span<int> sp = vec; vec.push_back(1);                          // may reallocate: sp dangles
auto key = map.find(sv);                                            // fine: used immediately
```
- Return `std::string` (owning) from functions that build strings; return
  `string_view` only into storage that outlives the call (members, static data).
- Avoid string_view members unless the class is explicitly a view type.
- Compiler help: GCC `-Wdangling-reference` warns when a reference is bound to a temporary whose lifetime has ended; check your compiler's documentation for further lifetime warnings.

## Null termination
`string_view::data()` is NOT guaranteed null-terminated. Passing it to C APIs
(`fopen`, `strlen`, `printf("%s")`) reads past the end. Convert:
`std::string(sv).c_str()`, or keep a `const std::string&`/`const char*` API for C calls.
Printing: `printf("%.*s", int(sv.size()), sv.data())` or `std::print("{}", sv)`.

## span specifics
- `std::span<T, N>` fixed extent vs `std::span<T>` dynamic; `subspan`, `first`, `last`
  have no bounds checks in release (C++26 adds `.at()`); enable hardened standard
  library modes (`_GLIBCXX_ASSERTIONS`, libc++ hardening) in debug/CI.
- `std::span<const T>` for read-only parameters; `span<T>` converts to it implicitly,
  but template argument deduction does not see through conversions, so templates
  taking `std::span<const T>` need an explicit `std::span(vec)` at the call site.

## Checked
2026-10-28: Confirmed on cppreference (basic_string_view, span) and the GCC C++ dialect options page (-Wdangling-reference): views do not own, span extents, subspan/first/last. Removed the muddled flag list and the clang attribute claims (not in fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] ASan and hardened-library builds run the test suite clean.
- [ ] No functions returning string_view/span to locals or temporaries (review + warnings).
