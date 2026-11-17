---
id: computing-software.software-engineering.cpp.enum-class-and-scoped-enumerations
name: enum-class-and-scoped-enumerations
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-types, cpp-ty-enumclass, enum-class, scoped-enum, underlying-type, std-to-underlying, switch-exhaustiveness, enum-class-scoped]
level: practitioner
status: docs-checked
description: "Use enum class in C++: scoping, underlying types, std::to_underlying, using enum, switch over enumerators, and out-of-range values from casts."
sources: ["https://en.cppreference.com/w/cpp/language/enum", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#enum3-prefer-class-enums-over-plain-enums"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# enum class

```cpp
enum class Color : std::uint8_t { Red, Green, Blue };      // scoped, no implicit int conversion, fixed size
Color c = Color::Green;
// int i = c;                                // error
auto i = static_cast<int>(c);                // explicit
auto u = std::to_underlying(c);              // C++23

std::string_view name(Color c) {
  switch (c) {
    case Color::Red:   return "red";
    case Color::Green: return "green";
    case Color::Blue:  return "blue";
  }
  return "?";                                // reached only for a value outside the enumerators
}

void paint(Color c) {
  using enum Color;                          // C++20: bring enumerators into scope locally
  if (c == Red) { /* ... */ }
}
```

## Why not plain enum
Plain `enum` leaks enumerator names into the enclosing scope (Core Guidelines Enum.3: two plain enums both declaring `red` collide) and converts to int too readily. A scoped enumeration has underlying type `int` unless you name one, and has no implicit conversion to integral types.

## Rules
- Specify the underlying type when the value is stored or serialised: `enum class Color : std::uint8_t`. An enumeration has the same size, value representation and alignment as its underlying type. The same syntax with a trailing `;` is an opaque declaration.
- `using enum` (C++20) introduces the enumerator names as if by a using-declaration; two `using enum` declarations that introduce the same name conflict.
- Bit flags need operator overloads (see the bit-flags skill).

## Gotchas
- `static_cast` can convert any integer to an enumeration and the result need not equal a named enumerator, so a `switch` may see values outside the list; validate untrusted input before casting. For an enumeration without a fixed underlying type, casting a value outside its range is undefined behaviour (since CWG 1766; previously unspecified). Scoped enumerations always have a fixed underlying type.
- Adding an enumerator changes `switch`-based serialisation; keep stable numeric values explicit (`Red = 1`).

## Verify
- [ ] Round-trip test of every enumerator through your string conversion functions.

## Checked
2026-11-03. Confirmed on cppreference Enumeration declaration (scoped enum default `int`, no implicit conversion, `static_cast`, `using enum` since C++20, out-of-range cast UB per CWG 1766, `to_underlying` C++23) and Core Guidelines Enum.3. Removed: compiler warning flags (`-Wswitch`, `-Wswitch-enum`) and the advice not to add `default`, `std::unreachable`, the claim that plain enums have an implementation-chosen underlying type, the `operator<<`/reflection note, the comparison and array-index notes.
Method: documentation only; no commands were run.
