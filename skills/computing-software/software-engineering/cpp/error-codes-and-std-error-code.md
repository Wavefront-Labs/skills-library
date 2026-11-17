---
id: computing-software.software-engineering.cpp.error-codes-and-std-error-code
name: error-codes-and-std-error-code
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-errors, cpp-er-codes, std-error-code, system-error, error-category, error-condition, filesystem-errors, error-code-system-error]
level: practitioner
status: docs-checked
description: "Report C++ errors without exceptions using std::error_code, custom error categories and portable error_condition comparison."
sources: ["https://en.cppreference.com/w/cpp/error/error_code", "https://en.cppreference.com/w/cpp/error/error_category"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error codes and std::error_code

`std::error_code` holds an error code value originating from the operating system or some low-level interface plus a pointer to a `std::error_category` for that interface. Values are not required to be unique across categories, so interpret a value only together with its category.

```cpp
#include <system_error>
namespace app {
enum class Errc { ok = 0, bad_header = 1, truncated = 2 };
struct Category : std::error_category {
  const char* name() const noexcept override { return "app"; }
  std::string message(int c) const override {
    switch (static_cast<Errc>(c)) { case Errc::bad_header: return "bad header"; case Errc::truncated: return "truncated"; default: return "ok"; }
  }
};
inline const std::error_category& category() { static const Category c; return c; }
inline std::error_code make_error_code(Errc e) { return {static_cast<int>(e), category()}; }
}
template <> struct std::is_error_code_enum<app::Errc> : std::true_type {};   // marks the enum as an error_code enumeration

std::error_code parse(std::span<const std::byte> b) {
  if (b.size() < 4) return app::Errc::truncated;
  return {};                                       // value 0 = success
}
if (auto ec = parse(buf)) { log(ec.message()); }   // operator bool: true when the value is non-zero
```

## Members worth knowing
- `value()`, `category()`, `message()` observe the code; `clear()` sets it to value 0 in `system_category`.
- `std::error_category` is the base for categories such as `system_category` and `iostream_category`; the category objects are treated as singletons passed by reference. `generic_category()`, `system_category()`, `iostream_category()` and `future_category()` are the library's own.
- `std::error_condition` holds a portable error code. `error_code::default_error_condition()` maps a code to its condition and `error_category::equivalent` compares a code with a condition, which is how a platform code is matched against a portable one.
- `make_error_code(std::errc)` creates an error code from the `errc` enumeration.

## Gotchas
- Check `ec` after every call; unlike exceptions, ignored errors vanish.
- Define `name()` and `message()` once per category; the category is looked up through a function returning a static object.

## Verify
- [ ] Unit test each code: `message()`, comparison and conversion from your enum.

## Checked
2026-11-03. Confirmed on cppreference std::error_code (member list, `operator bool`, `clear`, `is_error_code_enum`, `make_error_code(errc)`) and std::error_category (virtual `name`, `message`, `equivalent`, `default_error_condition`; singleton treatment; specific categories). Removed: the ENOENT/Win32 portability claim, the filesystem non-throwing overload section and `std::system_error` example, the `std::expected`, asio and `-fno-exceptions` style guidance, `[[nodiscard]]` and clang-tidy advice, the errno thread-local note, the claim that filesystem overloads clear `ec`, and "compare by address".
Method: documentation only; no commands were run.
