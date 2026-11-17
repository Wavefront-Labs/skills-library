---
id: computing-software.software-engineering.cpp.three-way-comparison-and-spaceship
name: three-way-comparison-and-spaceship
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-operators, cpp-op-spaceship, spaceship-operator, defaulted-comparison, strong-ordering, rewritten-candidates, three-way-comparison]
level: practitioner
status: docs-checked
description: "Define C++20 comparisons with a defaulted operator<=> and operator==, pick the right ordering category, and handle floats, custom ordering and rewritten candidate pitfalls."
sources: ["https://en.cppreference.com/w/cpp/language/default_comparisons", "https://en.cppreference.com/w/cpp/utility/compare/strong_ordering", "https://en.cppreference.com/w/cpp/utility/compare/partial_ordering", "https://en.cppreference.com/w/cpp/utility/compare/compare_three_way"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Three-way comparison (<=>)

```cpp
#include <compare>
struct Version {
  int major = 0, minor = 0, patch = 0;
  auto operator<=>(const Version&) const = default;   // lexicographic over members in declaration order
  bool operator==(const Version&) const = default;    // implicit when <=> is defaulted, shown for clarity
};
Version a{1,2,3}, b{1,3,0};
a < b; a != b; a >= b;           // all synthesised from <=> and ==
std::set<Version> s;              // works with std::less
```

## Ordering categories (return type of `<=>`)
| Type | Meaning |
|---|---|
| `std::strong_ordering` | equal values are indistinguishable (ints, strings) |
| `std::weak_ordering` | equivalent but distinguishable (case-insensitive strings) |
| `std::partial_ordering` | some pairs unordered (floating point NaN) |
A defaulted `<=>` declared with `auto` deduces `std::common_comparison_category_t` of the members' `<=>` result types, so one member with a `partial_ordering` result makes the whole result `partial_ordering`. Members are compared in order (base classes, then data members in declaration order) and the first non-equal result is returned.

## Custom ordering
```cpp
std::strong_ordering operator<=>(const Person& a, const Person& b) {
  if (auto c = a.last <=> b.last; c != 0) return c;
  return a.first <=> b.first;
}
bool operator==(const Person& a, const Person& b) { return a.last == b.last && a.first == b.first; }   // == is NOT generated from a user-provided <=>
```
`std::compare_three_way` is the function object that applies `<=>` to two arguments.

## Gotchas
- An `operator==` is declared implicitly only for a defaulted `<=>` and only when the class declares no `operator==` of its own; a user-provided `<=>` does not declare `==`, so define it separately.
- The defaulted `<=>` is defined as deleted if some member has no usable `<=>` or its result is not a comparison category type.
- Default `<=>` compares every base and member in order, including ones you may not want (caches, pointers); order members deliberately or write it by hand.
- The `!=`, `<`, `>`, `<=`, `>=` operators are selected through rewritten candidates from `<=>` and `==`; you do not define them.
- A `partial_ordering` result can be `unordered`, in which case `<`, `<=`, `>`, `>=` are all false; sorting with it needs a policy.

## Verify
- [ ] Sorting and equality tests with equal, lesser, greater values on each field.
- [ ] A `std::set<Version>` insert compiles (it needs `<`).

## Checked
2026-11-08. Confirmed on cppreference Default comparisons (member order, common_comparison_category_t deduction, deleted conditions, implicit operator== rule, rewritten secondary operators), the strong_ordering and partial_ordering pages (category meanings, unordered) and the compare_three_way page. Removed: compiler version support line, ranges::less projection advice, the asymmetric operator== ambiguity claim and the three_way_comparable/totally_ordered concept checks (not on the pages read).
Method: documentation only; no commands were run.
