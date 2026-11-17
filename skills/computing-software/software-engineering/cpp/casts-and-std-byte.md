---
id: computing-software.software-engineering.cpp.casts-and-std-byte
name: casts-and-std-byte
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-types, cpp-ty-casts, static-cast, reinterpret-cast, const-cast, bit-cast, std-byte, narrowing, casts-std-byte]
level: practitioner
status: docs-checked
description: "Choose the right C++ cast: static_cast, dynamic_cast, const_cast, reinterpret_cast, std::bit_cast and std::byte for raw memory; avoid C-style casts and narrowing."
sources: ["https://en.cppreference.com/w/cpp/language/explicit_cast", "https://en.cppreference.com/w/cpp/numeric/bit_cast", "https://en.cppreference.com/w/cpp/types/byte"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Casts and std::byte

| Cast | Use | Danger |
|---|---|---|
| `static_cast<T>(x)` | basic conversions: numeric, base/derived pointers known statically | a wrong downcast is not checked |
| `dynamic_cast<D*>(b)` | runtime-checked cast within a class hierarchy (see its own cppreference page) | prefer virtual functions over type tests |
| `const_cast<T&>(x)` | add or remove const/volatile when calling a legacy API | only changes cv-qualifiers |
| `reinterpret_cast<T*>(p)` | general low-level conversions: pointer <-> integer | type aliasing rule: not for reinterpreting object representation |
| `std::bit_cast<To>(from)` (C++20) | reinterpret an object's representation (float <-> uint32_t) | `sizeof(To) == sizeof(From)` and both trivially copyable |
| C-style `(T)x` | avoid | tries static_cast, then static_cast plus const_cast, then reinterpret_cast, then reinterpret_cast plus const_cast, and takes the first that fits |

```cpp
float f = 1.0f;
auto bits = std::bit_cast<std::uint32_t>(f);                  // constexpr, noexcept, no aliasing issue
// auto bad = *reinterpret_cast<std::uint32_t*>(&f);           // violates the type aliasing rule

std::array<std::byte, 4> buf{};
std::byte b = std::byte{0x2A};
auto n = std::to_integer<int>(b);                             // std::byte is not arithmetic: shifts with an integer and bitwise ops with another byte only
```
`std::byte` is `enum class byte : unsigned char {}`. Like `unsigned char` it can access the raw memory of other objects, but it is not a character type and not an arithmetic type (`b *= 2` is an error). Convert to a number with `std::to_integer` or an explicit conversion.

## Gotchas
- The C-style cast picks the first interpretation that satisfies the cast rules, even if that one is ill-formed, and it can also cast through private inheritance; prefer the named casts so intent is visible.
- `reinterpret_cast` between pointer or reference types to reinterpret an object representation is generally wrong because of the type aliasing rule; use `std::bit_cast` (or `memcpy`).
- `bit_cast` of a value with indeterminate bits is undefined unless the affected object is `std::byte`, `unsigned char` or `char` (when unsigned), until C++26.

## Verify
- [ ] No C-style casts remain in the changed code (search for them; consider `-Wold-style-cast`).
- [ ] Every `bit_cast` has matching sizes (`static_assert(sizeof(To) == sizeof(From))` documents it) and trivially copyable types.

## Checked
2026-11-08. Confirmed on cppreference Explicit type conversion (C-style cast resolution order, extensions, named-cast summaries), std::bit_cast (constraints, constexpr, noexcept, aliasing note, indeterminate-bit rule) and std::byte (definition, operations, to_integer, not arithmetic). Removed: as_bytes, std::in_range/cmp_less and gsl::narrow advice, dynamic_cast failure details, const_cast-on-const-object UB, provenance and sanitiser flag claims (not on the pages read).
Method: documentation only; no commands were run.
