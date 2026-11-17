---
id: computing-software.software-engineering.cpp.small-string-optimization-and-string-costs
name: small-string-optimization-and-string-costs
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-performance, cpp-pf-sso, std-string, allocation, string-view, reserve]
level: advanced
status: docs-checked
description: "Cut std::string allocation cost: reserve semantics, capacity growth, invalidation rules, resize_and_overwrite, pmr strings, and measuring SSO capacity."
sources: ["https://en.cppreference.com/w/cpp/string/basic_string", "https://en.cppreference.com/w/cpp/string/basic_string/reserve"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Small string optimisation and string costs

Many standard libraries keep short strings inside the `std::string` object so no heap allocation is needed. The standard does not mandate this or any threshold, so measure it rather than assume it:

```cpp
std::string s;
std::cout << s.capacity() << "\n";   // the reference's sample output shows 15 for an empty string on one implementation
```

## Reduce allocations
```cpp
std::string out;
out.reserve(estimated);              // one allocation for the final size
out += a; out += ','; out += b;      // append, not out = out + a + ...
```
- `reserve(new_cap)`: if `new_cap` is greater than the current capacity, new storage is allocated and capacity becomes at least `new_cap`. Since C++20, a `new_cap` less than or equal to the capacity has no effect; before C++20 a smaller value was a non-binding shrink request.
- If a capacity change takes place, all iterators and references (including past-the-end) are invalidated. It throws `std::length_error` if `new_cap` exceeds `max_size()`, and has strong exception safety (no effect if it throws).
- The no-argument `reserve()` is deprecated in C++20 and removed in C++26; use `shrink_to_fit()` instead. `shrink_to_fit` is a non-binding request; after it, capacity is unspecified but at least `size()`.
- Growth when appending is geometric: the reference's sample shows capacity going 101, 202, 404, 808, 1616 (a factor of 2 on that implementation; not guaranteed by the standard).
- `resize_and_overwrite` (C++23, feature macro `__cpp_lib_string_resize_and_overwrite` = 202110L) changes the size and lets a user-provided operation overwrite indeterminate contents, which avoids zero-filling before writing from a C API.
- `std::pmr::string` is `basic_string` with `std::pmr::polymorphic_allocator<char>` (C++17); use it with a memory resource to control allocation.
- A `std::basic_string` converts to a non-modifiable `std::basic_string_view` over the whole string, so take `string_view` parameters when you only read.

## Invalidation
- References, pointers and iterators to a string's elements may be invalidated by any library function taking a non-const `basic_string&` (such as `std::getline`, `std::swap`, `operator>>`) and by calling non-const member functions, except `operator[]`, `at`, `data`, `front`, `back`, `begin`, `rbegin`, `end` and `rend`.
- Practical rule: do not keep a `string_view`, pointer or iterator into a string that may be modified, swapped or reallocated, including strings held in a growing container.

## Verify
- Count allocations in a before/after test (for example with a counting `operator new`) and benchmark strings below and above the capacity your library reports for an empty string.

## Checked
Read the cppreference basic_string and basic_string::reserve pages. Removed as unconfirmed: the per-library SSO sizes (15/22/15) and `sizeof(std::string)` values, that moving an SSO string copies bytes, std::format_to buffer patterns, heterogeneous lookup advice, the dual ABI remark, and `c_str` stability wording.
Method: docs-checked 2026-11-09 against the cppreference basic_string and basic_string::reserve pages.
