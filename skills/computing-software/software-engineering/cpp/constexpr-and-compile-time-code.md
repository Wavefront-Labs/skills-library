---
id: computing-software.software-engineering.cpp.constexpr-and-compile-time-code
name: constexpr-and-compile-time-code
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, modern-cpp, constexpr, consteval, constinit, compile-time, static-assert, lookup-tables, static-initialization-order, cpp-constants]
level: advanced
status: docs-checked
description: "Move work to compile time in C++ with constexpr, consteval and constinit: lookup tables, compile-time validation, and fixing static initialization order problems."
sources: ["https://en.cppreference.com/w/cpp/language/constexpr", "https://en.cppreference.com/w/cpp/language/consteval", "https://en.cppreference.com/w/cpp/language/constinit", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#per11-move-computation-from-run-time-to-compile-time"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# constexpr, consteval and constinit

**Goal:** catch errors at compile time, precompute tables for free, and eliminate
runtime static-initialization surprises.

## The three keywords
| Keyword | Meaning |
|---|---|
| `constexpr` function | MAY run at compile time when called in a constant context; otherwise runs at runtime |
| `constexpr` variable | must be initialised at compile time; implicitly const |
| `consteval` function | MUST run at compile time (immediate function), C++20 |
| `constinit` variable | static/thread storage initialised at compile time, but mutable later (C++20) |

## Lookup tables
```cpp
constexpr auto make_crc_table() {
    std::array<uint32_t, 256> t{};
    for (uint32_t i = 0; i < 256; ++i) {
        uint32_t c = i;
        for (int k = 0; k < 8; ++k) c = (c & 1) ? 0xEDB88320u ^ (c >> 1) : c >> 1;
        t[i] = c;
    }
    return t;
}
constexpr auto kCrcTable = make_crc_table();   // computed by the compiler
```
C++20 allows `std::vector`/`std::string` inside constexpr functions as long as memory is
freed before the end of evaluation (transient allocation).

## Compile-time validation
```cpp
consteval int checked_port(int p) { if (p <= 0 || p > 65535) throw "bad port"; return p; }
constexpr int kPort = checked_port(8080);   // checked_port(70000) is a compile error
static_assert(sizeof(Header) == 16, "wire format changed");
```
`std::format` checks format strings at compile time using this technique.

## Static initialization order fiasco
Globals with dynamic initialisers in different translation units initialise in
unspecified order; one may read another before it is constructed.
```cpp
constinit Registry* g_registry = nullptr;        // guaranteed static init, no ordering problem
Config& config() { static Config c = load(); return c; }   // function-local static: lazy, thread-safe
```
`constinit` makes the compiler reject anything that would need dynamic init.

## Testing constexpr code
`static_assert(gcd(12, 18) == 6);` in the header or test file. Undefined behaviour
during constant evaluation is a compile ERROR, so constexpr tests double as UB checks.

## Limits
Compile-time evaluation increases build time, and compilers cap evaluation steps (see your compiler's
constexpr limit options). `std::is_constant_evaluated()` and `if consteval` (C++23) branch between
compile-time and runtime implementations.

## Checked
2026-10-28: Confirmed on cppreference (constexpr, consteval, constinit pages): consteval functions are immediate functions that must produce a compile-time constant, constinit is C++20, if consteval is C++23. Removed the compiler flag names and the .rodata claim (not in fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Tables are not built at startup (check the disassembly or object file).
- [ ] No non-constinit globals with dynamic initialisers that depend on other TUs.
