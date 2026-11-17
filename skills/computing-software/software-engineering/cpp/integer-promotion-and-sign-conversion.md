---
id: computing-software.software-engineering.cpp.integer-promotion-and-sign-conversion
name: integer-promotion-and-sign-conversion
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-expressions, cpp-ex-promotion, integer-promotion, sign-conversion, usual-arithmetic-conversions, signed-overflow, std-cmp-less, integer-promotion-sign-conversion]
level: practitioner
status: docs-checked
description: "Avoid C++ integer pitfalls: promotion rules, signed/unsigned comparison, overflow UB, safe comparisons with std::cmp_less, checked arithmetic and warning flags."
sources: ["https://en.cppreference.com/w/cpp/language/implicit_conversion", "https://en.cppreference.com/w/cpp/utility/intcmp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integer promotion and sign conversion

Integer types whose conversion rank is lower than `int` are promoted to `int` when `int` can represent all their values (otherwise to `unsigned int`) before arithmetic. When a signed and an unsigned operand meet in a built-in comparison, the signed value is converted to the unsigned type (usual arithmetic conversions).

```cpp
std::uint8_t a = 200, b = 100;
auto s = a + b;                      // int 300, not wrapped to 44
std::uint8_t t = a + b;              // converts back to the unsigned type modulo 2^8: 44

int i = -1; unsigned u = 1;
bool r = i < u;                      // false: i becomes 4294967295u
std::cmp_less(i, u);                 // true: C++20 <utility> compares mathematically
std::size_t n = v.size(); for (int k = n - 1; k >= 0; --k) {}   // n - 1 on empty vector wraps to huge
```

## Rules
- Conversion to an unsigned type gives the value modulo 2^n (n = bits of the destination). Conversion to a signed type that cannot represent the value is implementation-defined until C++20 and the same modulo rule since C++20. Signed integer arithmetic overflow is undefined, unlike that conversion.
- Floating-to-integer conversion: if the truncated value cannot fit the destination, the behavior is undefined, even for unsigned destinations.
- The `std::cmp_equal`, `cmp_not_equal`, `cmp_less`, `cmp_greater`, `cmp_less_equal` and `cmp_greater_equal` functions (header `<utility>`, C++20) compare integers by value: a negative signed integer always compares less than an unsigned one.
- `std::in_range<T>(x)` (C++20) checks whether an integer value is in the range of a given integer type before you narrow it.
- Prefer one type through an expression, or iterate with range-for, instead of mixing `size()` (unsigned) with signed indexes.

## Gotchas
- Indexes from `size()` are unsigned: `i < v.size() - 1` is true for an empty container because `0 - 1` wraps.
- Bit-fields promote as well: to `int` if `int` can represent all their values, otherwise to `unsigned int`.
- Treat compiler sign-comparison and conversion warnings as bugs and fix the type rather than silencing them (enable them in your compiler's warning settings).

## Verify
- [ ] Tests include edge inputs (INT_MAX, 0, empty container) and mixed signed/unsigned comparisons through `std::cmp_*`.
- [ ] The build has sign-compare and conversion warnings on with zero findings in new code.

## Checked
2026-11-08. Confirmed on cppreference Implicit conversions (integral promotion rules for small types and bit-fields, modulo 2^n conversion rules, signed overflow undefined, floating-to-integer undefined case) and std::cmp_equal ... cmp_greater_equal (header `<utility>`, mathematical comparison, example with -1 and 1U; in_range listed as related). Removed: __builtin_add_overflow/ckd_add/add_sat, ssize, shift and char signedness rules, abs(INT_MIN), compiler warning flag lists and UBSan options (not on the pages read).
Method: documentation only; no commands were run.
