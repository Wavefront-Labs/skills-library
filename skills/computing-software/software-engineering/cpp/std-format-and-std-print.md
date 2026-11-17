---
id: computing-software.software-engineering.cpp.std-format-and-std-print
name: std-format-and-std-print
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, std-format, std-print, fmtlib, string-formatting, formatter-specialization, c++20, c++23, cpp-text-io]
level: practitioner
status: docs-checked
description: "Format text in modern C++ with std::format and std::print: format spec mini-language, compile-time checks, formatting custom types, format_to buffers and the {fmt} fallback."
sources: ["https://en.cppreference.com/w/cpp/utility/format/format", "https://en.cppreference.com/w/cpp/utility/format/spec", "https://en.cppreference.com/w/cpp/io/print", "https://fmt.dev/latest/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# std::format and std::print

**Goal:** type-safe, fast, readable formatting that replaces printf and iostream manipulators.

## Basics
```cpp
#include <format>
#include <print>      // C++23
std::string s = std::format("{} has {} items", name, n);
std::println("{:>8.2f} | {:<10} | {:#06x}", price, sku, flags);
std::print(stderr, "error: {}\n", msg);
```
- Format strings are **checked at compile time** (C++20 via consteval `format_string`): a wrong
  argument count or an invalid spec for the type is a compile error. For runtime format strings
  use `std::vformat(fmt, std::make_format_args(args...))` (and validate them).

## Spec mini-language `{arg-id:fill align sign # 0 width .precision L type}`
| Example | Output |
|---|---|
| `{:>10}` / `{:<10}` / `{:^10}` | right/left/centre in width 10 |
| `{:*^10}` | fill with `*` |
| `{:+d}` | always show sign |
| `{:08.3f}` | zero-pad, 3 decimals |
| `{:x}` `{:#x}` `{:b}` `{:o}` | hex, 0x-prefixed, binary, octal |
| `{:e}` `{:g}` | scientific, general |
| `{:L}` | locale-aware (thousands separators) - otherwise formatting is locale-independent |
| `{0} {1} {0}` | positional reuse |
| `{:{}}` | width from an argument |
| `{:?}` | debug/escaped strings and chars (C++23) |
Default float output is the shortest round-trippable representation.

## Ranges, chrono, pointers
C++23 formats ranges and tuples: `std::println("{}", std::vector{1, 2, 3})` prints `[1, 2, 3]`;
`{:n}` drops brackets. Chrono: `std::format("{:%F %T}", std::chrono::system_clock::now())`. Pointers
need `static_cast<const void*>(p)` (prints hex).

## Formatting your own types
```cpp
struct Point { double x, y; };

template <>
struct std::formatter<Point> : std::formatter<double> {   // reuse double's spec parsing
    auto format(const Point& p, std::format_context& ctx) const {
        auto out = std::format_to(ctx.out(), "(");
        ctx.advance_to(out);
        out = std::formatter<double>::format(p.x, ctx);
        out = std::format_to(out, ", ");
        ctx.advance_to(out);
        out = std::formatter<double>::format(p.y, ctx);
        return std::format_to(out, ")");
    }
};
std::println("{:.1f}", Point{1.25, 2.5});   // (1.2, 2.5)
```
Simplest version: inherit `std::formatter<std::string_view>` and format a temporary string. Make the
`format` member `const`.

## Performance
- `std::format_to(std::back_inserter(buf), ...)` appends to an existing buffer;
  `std::format_to_n` writes into fixed storage with truncation; `std::formatted_size` computes length.

## Toolchain support and {fmt}
Check the compiler support table on cppreference for the first release of each compiler that ships
`<format>` and `<print>`. On older toolchains use **{fmt}** (`fmt::format`, `fmt::print`, `FMT_COMPILE`, `fmt::join`), which
std::format was based on; it also offers features ahead of the standard. spdlog uses {fmt} or
std::format internally.

## Gotchas
- Literal braces are `{{` and `}}`.
- `char8_t` / `u8"..."` strings do not format into `std::string` directly.
- Custom formatter specialisations must be visible wherever the type is formatted (put them in the
  type's header).

## Checked
2026-10-28: Confirmed on cppreference (std::format, format specification, std::print, std::formatted_size): format specifier grammar including the L option, ? escaped presentation (C++23), print/println and the vprint_unicode functions. Fixed the custom formatter example (output iterator was not advanced before delegating to formatter<double>). Removed compiler version numbers, performance claims and the Windows console claim.
Method: documentation only; no commands were run.

## Verify
- [ ] No printf-family calls with user-controlled format strings remain.
- [ ] Custom types format via `std::formatter` specialisations with tests.
- [ ] Build passes on the oldest supported compiler (or uses {fmt}).
