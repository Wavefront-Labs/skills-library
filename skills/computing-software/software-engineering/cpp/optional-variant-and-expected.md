---
id: computing-software.software-engineering.cpp.optional-variant-and-expected
name: optional-variant-and-expected
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, modern-cpp, cpp17, std-optional, std-variant, std-expected, std-visit, sum-types, error-handling, monadic-operations]
level: practitioner
status: docs-checked
description: "Model maybe-values, alternatives and errors in C++ with std::optional, std::variant + std::visit and C++23 std::expected, including monadic chaining and pitfalls."
sources: ["https://en.cppreference.com/w/cpp/utility/optional", "https://en.cppreference.com/w/cpp/utility/variant", "https://en.cppreference.com/w/cpp/utility/expected"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std::optional, std::variant and std::expected

**Goal:** replace sentinel values, nullable pointers, out-parameters and unions with
vocabulary types the compiler understands.

## optional: maybe a value
```cpp
std::optional<User> find(Id id);
if (auto u = find(id)) use(*u);
auto name = find(id).transform(&User::name).value_or("guest");   // C++23 monadic ops
```
- `*opt` on empty is UB; `.value()` throws `bad_optional_access`. Check first.
- `std::optional` of a reference type is ill-formed in C++17/20/23; use `T*` for an optional reference.
- Don't use for error reporting where the caller needs to know WHY: use expected.

## variant: one of several types
```cpp
using Shape = std::variant<Circle, Rect, Polygon>;
template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

double area(const Shape& s) {
    return std::visit(overloaded{
        [](const Circle& c) { return std::numbers::pi * c.r * c.r; },
        [](const Rect& r)   { return r.w * r.h; },
        [](const Polygon& p){ return p.area(); },
    }, s);
}
```
- `std::visit` with an overload set fails to compile if a case is missing: exhaustive by construction.
- `std::get<Rect>(s)` throws `bad_variant_access` if wrong; `std::get_if<Rect>(&s)` returns pointer or null.
- `valueless_by_exception()` can happen if assignment throws mid-way; rare but real.
- Variant size = largest alternative + index; big alternatives bloat every instance (box them).

## expected: value or error (C++23)
```cpp
std::expected<Config, ParseError> parse(std::string_view text);

auto cfg = read_file(path)
    .and_then(parse)                         // propagate errors
    .transform(apply_defaults)
    .or_else([](const ParseError& e) -> std::expected<Config, ParseError> { log(e); return std::unexpected(e); });
if (!cfg) return std::unexpected(cfg.error());
```
- Mark functions returning expected `[[nodiscard]]` so ignored errors warn.
- Exceptions vs expected: expected for anticipated, local failures (parsing, validation);
  exceptions for truly exceptional failures crossing many layers.

## Checked
2026-10-28: Confirmed on cppreference (optional, variant, expected pages): value() and bad_optional_access, visit, get_if, valueless_by_exception, expected as a C++23 type with and_then/transform/or_else. Removed the tl::expected claim and the clang-tidy check name, and reworded the optional reference note to match the standard text.
Method: documentation only; no commands were run.

## Verify
- [ ] No `.value()`/`*` on optional/expected without a preceding check (static analysis can flag these).
- [ ] Adding a variant alternative breaks compilation of every visitor that must handle it.
