---
id: computing-software.software-engineering.cpp.strongly-typed-interfaces
name: strongly-typed-interfaces
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-interfaces, cpp-if-strong-types, strong-types, type-safety, explicit, core-guidelines]
level: practitioner
status: docs-checked
description: "Make C++ interfaces precisely and strongly typed per Core Guidelines I.4: avoid void*, naked ints and bool lists; use chrono durations, structs and explicit."
sources: ["https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#i4-make-interfaces-precisely-and-strongly-typed", "https://en.cppreference.com/w/cpp/language/explicit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strongly typed interfaces

Core Guidelines I.4: make interfaces precisely and strongly typed. Reason given: types are the simplest and best documentation, improve legibility through well-defined meaning, and are checked at compile time; precisely typed code is also often optimised better.

## Patterns from the guideline
- **Do not pass `void*`**: callers cannot tell which types are allowed or whether the data is mutated, every pointer type converts to it, and the callee must `static_cast` to an unverified type. Use `const void*` only in designs indescribable in C++; prefer a `variant`, a pointer to base, or a template parameter (`T*`/`T&`, possibly concept-constrained).
- **Name what the numbers mean**: `draw_rect(100, 200, 100, 500)` is unclear. Use `draw_rectangle(Point top_left, Point bottom_right)` and `draw_rectangle(Point top_left, Size height_width)` overloads. The type system cannot catch everything (that the first argument is the top-left point is left to convention).
- **Replace lists of bool/int settings** (`set_settings(true, false, 42)`) with a settings struct (`alarm_settings s{}; s.enabled = true; ...`), and for a set of booleans use a flags `enum` (`lamp_option::on | lamp_option::animate_state_transitions`).
- **Make units explicit with `std::chrono::duration`**: `void blink_led(milliseconds time_to_blink)` called as `blink_led(1500ms)`. To accept any unit, take `duration<rep, period>` and `duration_cast` inside.
- Enforcement ideas: report `void*` as a parameter or return type; report more than one `bool` parameter; look for functions with too many primitive-type arguments.

## `explicit`
`explicit` on a constructor, conversion function or deduction guide means it cannot be used for implicit conversions and copy-initialisation. `explicit(constant-expression)` (C++20, feature macro `__cpp_conditional_explicit` = 201806L) makes it explicit only if the expression is `true`. A constructor that is not `explicit` and takes a single non-default parameter is a converting constructor. An explicit cast `(A)1` still works because it performs a `static_cast`.

Illustrative wrapper types (a sketch, not from the page):
```cpp
struct Meters  { double v; explicit constexpr Meters(double x) : v(x) {} };
struct Seconds { double v; explicit constexpr Seconds(double x) : v(x) {} };
constexpr double speed(Meters d, Seconds t) { return d.v / t.v; }
// speed(Meters{100}, Seconds{9.58});   ok
// speed(100, 9.58);                    error: explicit blocks the implicit conversion
```

## Verify
- Call sites have no naked literals for units, IDs or flags.

## Checked
Read Core Guidelines I.4 in full (and the start of I.5) and the cppreference explicit specifier page. Removed as unconfirmed: designated-initialiser parameter structs, `std::span` and `std::filesystem::path` substitution advice, NamedType and type_safe libraries, zero-runtime-cost claims and `static_assert` checks, operator-overload guidance.
Method: docs-checked 2026-11-09 against Core Guidelines I.4 and the cppreference explicit page.
