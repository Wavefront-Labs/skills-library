---
id: computing-software.software-engineering.cpp.bit-flags-with-enum-class-and-bitset
name: bit-flags-with-enum-class-and-bitset
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-types, cpp-ty-bitflags, bit-flags, std-bitset, bitmask, enum-class-operators, std-popcount, bit-flags-bitset]
level: practitioner
status: docs-checked
description: "Model C++ bit flags with enum class operator overloads, std::bitset, and <bit> helpers; avoid signed shifts and overflow."
sources: ["https://en.cppreference.com/w/cpp/utility/bitset", "https://en.cppreference.com/w/cpp/header/bit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bit flags with enum class and bitset

```cpp
enum class Perm : std::uint8_t { None = 0, Read = 1 << 0, Write = 1 << 1, Exec = 1 << 2 };

using U = std::underlying_type_t<Perm>;
constexpr Perm operator|(Perm a, Perm b) { return Perm(static_cast<U>(a) | static_cast<U>(b)); }
constexpr Perm operator&(Perm a, Perm b) { return Perm(static_cast<U>(a) & static_cast<U>(b)); }
constexpr Perm operator~(Perm a)         { return Perm(~static_cast<U>(a) & 0x07); }   // mask to defined bits
constexpr Perm& operator|=(Perm& a, Perm b) { return a = a | b; }
constexpr bool has(Perm set, Perm f) { return (set & f) == f; }

Perm p = Perm::Read | Perm::Write;
p |= Perm::Exec;
p = p & ~Perm::Write;
```
The bitwise operators on the underlying `unsigned char` promote to `int`, so convert the result back to `Perm` (the `Perm(...)` above).

## std::bitset for fixed-size sets
```cpp
std::bitset<64> mask;  mask.set(3); mask[5] = true;
mask.test(3); mask.count(); mask.any(); mask.to_ulong();
std::bitset<8>("10110000").to_string();
```
`std::bitset<N>` has a size fixed by the template argument `N`. Query with `test`, `count`, `any`, `all`, `none`; convert with `to_string`, `to_ulong`, `to_ullong`. `operator[]` on a non-const bitset returns the proxy class `bitset::reference`, so `auto b = mask[3];` captures the proxy, not a `bool`.

## <bit> (C++20)
`std::popcount(x)` (counts 1 bits in an unsigned integer), `std::countl_zero` and `std::countr_zero` (consecutive 0 bits from the most or least significant end), `std::has_single_bit` (is a power of 2), `std::bit_ceil` (smallest power of 2 not less than the value), `std::rotl` (left rotation) and `std::bit_cast<To>(from)`. The integer helpers are templates for unsigned integer types.

## Gotchas
- Test flags through a helper such as `has()` rather than relying on a conversion of the result to `bool`.
- `~` on a small unsigned type promotes to `int`; mask the result as `operator~` above does.
- Keep every flag value a distinct single bit so `|` and `&` behave as set operations.

## Verify
- [ ] `static_assert` truth table for `|`, `&`, `~` and `has`.

## Checked
2026-11-08. Confirmed on cppreference std::bitset (fixed template size, member list, to_string/to_ulong/to_ullong, reference proxy class) and the `<bit>` header (popcount, countl_zero, countr_zero, has_single_bit, bit_ceil, rotl, bit_cast and their signatures). Removed: std::to_underlying use, to_ulong overflow_error claim, vector<bool> remark, shift-UB and ADL claims, UBSan flags (not on the pages read).
Method: documentation only; no commands were run.
