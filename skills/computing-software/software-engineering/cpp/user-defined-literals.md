---
id: computing-software.software-engineering.cpp.user-defined-literals
name: user-defined-literals
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-operators, cpp-op-udl, user-defined-literals, operator-literal, chrono-literals, units, inline-namespace]
level: practitioner
status: docs-checked
description: "Define and use C++ user-defined literals: operator\"\" suffixes, the allowed parameter lists, raw and template forms, standard literal namespaces and the underscore rule."
sources: ["https://en.cppreference.com/w/cpp/language/user_literal", "https://en.cppreference.com/w/cpp/symbol_index/literals"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User-defined literals

A user-defined literal turns an integer, floating-point, character or string literal into an object of a user-defined type through a ud-suffix such as `12_km`, `0.5_Pa`, `'c'_X` or `"abd"_L`.

```cpp
#include <chrono>
#include <string>
#include <string_view>
using namespace std::literals;             // chrono_literals, string_literals, string_view_literals (the std::literals namespace)

auto timeout = 250ms;                       // chrono literal
auto name = "alice"s;                       // std::string
constexpr auto key = "id"sv;                // std::string_view (since C++17)

namespace units {
  struct Meters { long double v; };
  constexpr Meters operator""_m(long double x) { return {x}; }
  constexpr Meters operator""_km(long double x) { return {x * 1000}; }
}
using namespace units;
constexpr auto d = 1.5_km;
```

`std::literals` contains `chrono_literals` and `complex_literals` (since C++14), `string_literals` (since C++14) and `string_view_literals` (since C++17).

## Literal operator parameter lists
Only these are allowed (cppreference):

| Literal kind | Parameter list |
|---|---|
| Integer, first choice | `unsigned long long` |
| Floating, first choice | `long double` |
| Raw fallback for integer and floating | `const char*` |
| Character | `char`, `wchar_t`, `char8_t` (C++20), `char16_t`, `char32_t` |
| String | `(const char*, std::size_t)` and the `wchar_t`, `char8_t` (C++20), `char16_t`, `char32_t` equivalents |

- If an integer literal has no `unsigned long long` operator, the overload set must contain either a raw literal operator or a numeric literal operator template (`template<char...> double operator""_x();`), not both. The same fallback applies to floating-point literals.
- Since C++20 a string literal operator template takes a non-type template parameter of class type.
- Default arguments are not allowed and C language linkage is not allowed. Otherwise a literal operator is a normal function: it can be `inline` or `constexpr`.
- If the lookup of `operator""X` finds nothing the program is ill-formed. A token that matches both a user-defined and a regular literal syntax is a regular literal (you cannot overload `LL` in `123LL`).

## Rules
- A ud-suffix must begin with `_`; suffixes without it are reserved for the standard library, and suffixes containing a double underscore are reserved too.
- The `operator "" _km` spelling with a space is deprecated; write `operator""_km`.
- Adjacent string literals concatenate, and only one distinct ud-suffix may appear among them.
- Optional digit separators `'` are allowed in the digit sequences since C++14.

## Gotchas
- Declare literal operators in a namespace users opt into with `using namespace`, as the standard library does with `std::literals`; a `using namespace` in a header leaks into every includer.

## Verify
- [ ] A compile-time test of your literals passes, such as `static_assert` on the stored value.

## Checked
2026-11-03. Confirmed on cppreference User-defined literals (syntax forms, lookup and fallback rules, allowed parameter lists, underscore and double-underscore reservation, deprecated spaced form, concatenation) and the `std::literals` symbol index. Removed: the standard suffix list (d, y, i), "cooked" naming, the `inline namespace literals` pattern, claims about `-5_x`, `1.5_x` and integer overflow, the allocation claims for `s` and `sv`, and the `-Wuser-defined-literals` check.
Method: documentation only; no commands were run.
