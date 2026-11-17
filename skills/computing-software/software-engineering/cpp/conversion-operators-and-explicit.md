---
id: computing-software.software-engineering.cpp.conversion-operators-and-explicit
name: conversion-operators-and-explicit
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-operators, cpp-op-conv, conversion-operator, explicit-operator-bool, implicit-conversion, converting-constructor, conversion-operators-explicit]
level: practitioner
status: docs-checked
description: "Control C++ implicit conversions with explicit constructors and conversion operators, explicit operator bool and C++20 conditional explicit(bool)."
sources: ["https://en.cppreference.com/w/cpp/language/cast_operator", "https://en.cppreference.com/w/cpp/language/explicit", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c46-by-default-declare-single-argument-constructors-explicit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conversion operators and explicit

Implicit conversions silently pick overloads and hide bugs. Make them `explicit` unless the type is truly interchangeable (C.46).

```cpp
class Handle {
  int fd_ = -1;
public:
  explicit Handle(int fd) : fd_(fd) {}                    // int -> Handle must be spelled out
  explicit operator bool() const { return fd_ >= 0; }     // usable in if/while/&&/||/! but not in arithmetic
  explicit operator int() const { return fd_; }
};
Handle h{3};
if (h) { /* contextual conversion to bool: ok */ }
// int n = h + 1;          // error: no implicit conversion
int n = static_cast<int>(h) + 1;

template <class T> struct Wrapper {
  template <class U> explicit(!std::is_convertible_v<U, T>) Wrapper(U&& u);   // C++20 conditional explicit
};
```

## Rules
- Single-argument constructors: `explicit` by default (C.46).
- `explicit` on a constructor or conversion function stops implicit conversion and copy-initialization (`B b = 1;` and `bool nb = b;` fail); direct-initialization, `static_cast` and `if (b)` still work.
- `explicit(expression)` (since C++20) makes the function explicit if and only if the constant expression is true.
- Conversion to a reference or pointer to internal storage dangles when the object dies.
- Prefer named functions (`to_string()`) to conversion operators for lossy or costly conversions.

## Gotchas
- A non-explicit `operator bool` makes `bool b = h;` compile (copy-initialization considers it).
- An implicit conversion sequence contains zero or one converting constructor or user-defined conversion function, so chains of user-defined conversions fail to compile.
- With both a converting constructor and a conversion function, copy-initialization can be ambiguous while direct-initialization uses the constructor.

## Verify
- [ ] Negative compile tests: `static_assert(!std::is_convertible_v<int, Handle>)`, `!std::is_convertible_v<Handle, int>`, `std::is_constructible_v<bool, Handle>`.
- [ ] The clang-tidy check `google-explicit-constructor` (an alias of `misc-explicit-constructor`) runs clean.

## Checked
2026-11-03. Confirmed on cppreference (user-defined conversion function: `explicit operator`, `explicit(expression)` since C++20, one conversion function or constructor per implicit sequence, direct versus copy-initialization; explicit specifier: example of `B b1 = 1;` and `bool nb1 = b2;` errors), Core Guidelines C.46 and the clang-tidy check list. Removed: the contextual-conversion list, the multi-argument-constructor advice, `as_span()`, the `h1 == h2` and `h << 1` claims, the string_view dangling claim, the overload-ambiguity claim and the std::optional/unique_ptr/istream claim.
Method: documentation only; no commands were run.
