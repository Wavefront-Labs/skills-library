---
id: computing-software.software-engineering.cpp.gsl-and-bounds-safety
name: gsl-and-bounds-safety
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, gsl, bounds-safety, std-span, hardened-libcxx, glibcxx-assertions, not-null, narrow-cast, memory-safety]
level: advanced
status: docs-checked
description: "Get bounds safety in C++ with the Guidelines Support Library (span, not_null, narrow, at), std::span, hardened standard library modes and clang -Wunsafe-buffer-usage."
sources: ["https://github.com/microsoft/GSL", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-gsl", "https://libcxx.llvm.org/Hardening.html", "https://gcc.gnu.org/onlinedocs/libstdc++/manual/using_macros.html", "https://clang.llvm.org/docs/SafeBuffers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bounds safety with GSL and hardened containers

**Goal:** turn out-of-bounds reads/writes (the top memory-safety CVE class) into deterministic
traps or compile-time errors, with low runtime cost.

## 1. Stop passing (pointer, length)
```cpp
void checksum(std::span<const std::byte> data);      // instead of (const uint8_t* p, size_t n)
checksum(std::as_bytes(std::span{vec}));
```
`std::span` (C++20) carries the size; `subspan`, `first`, `last` replace pointer arithmetic.
`std::span::operator[]` has a precondition that hardened implementations check (below); `std::span::at()` appears in the C++26 working draft.

## 2. Guidelines Support Library (Microsoft GSL)
```cpp
#include <gsl/gsl>
void draw(gsl::not_null<Widget*> w);            // null rejected at construction (contract check)
int8_t b = gsl::narrow<int8_t>(i);             // throws gsl::narrowing_error if value changes
int8_t c = gsl::narrow_cast<int8_t>(i);        // documented intentional truncation, no check
auto& x = gsl::at(sp, i);                      // bounds-checked indexing (shown for a span)
gsl::owner<int*> p = new int;                  // annotation: this raw pointer owns
Expects(n > 0); Ensures(result != nullptr);    // pre/postconditions (terminate on failure)
auto _ = gsl::finally([&]{ cleanup(); });      // scope guard
```
- Get it via vcpkg (`ms-gsl`) or CMake FetchContent; target `Microsoft.GSL::GSL`.
- `Expects`/`Ensures` call `std::terminate` when the condition does not hold.
- The Core Guidelines Bounds profile (Bounds.1 no pointer arithmetic, Bounds.4 no non-bounds-checked standard
  library functions, and others) is partly checked by clang-tidy `cppcoreguidelines-pro-bounds-*`
  checks and by MSVC CppCoreCheck.

## 3. Hardened standard library (checks in operator[], front, back, span, string_view, optional)
| Library | Enable |
|---|---|
| libc++ | `-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_FAST` (recommended for production by libc++), `_EXTENSIVE`, `_DEBUG` |
| libstdc++ | `-D_GLIBCXX_ASSERTIONS` (precondition assertions; defined by default when compiling without optimisation; separate from `_GLIBCXX_DEBUG`) |
| MSVC STL | `_MSVC_STL_HARDENING=1` (macro defined in the microsoft/STL sources, default 0; check your toolset version), `_ITERATOR_DEBUG_LEVEL` in debug |
libc++'s fast mode is limited to checks that need little overhead and are intended for production; extensive and
debug modes cost more. A failed check terminates the program. The C++26 working draft standardises
"hardened implementations" with contract assertions.

## 4. Find raw buffer use at compile time
Clang `-Wunsafe-buffer-usage` (the "Safe Buffers" programming model) warns on raw pointer
arithmetic and unchecked array indexing to push code towards `std::span`. Adopt per directory with
`#pragma clang unsafe_buffer_usage begin/end` to mark audited legacy code.

## 5. Runtime detection in testing
ASan catches heap/stack/global overflows; `-fsanitize=bounds` (UBSan) catches statically sized array
indexing; `-D_FORTIFY_SOURCE=3` hardens libc buffer functions.

## Rollout
Enable `_GLIBCXX_ASSERTIONS` / libc++ fast mode in release builds, replace pointer+length APIs
with span at module boundaries, turn on `-Wunsafe-buffer-usage` for new code, and use `gsl::narrow`
wherever a conversion may lose data.

## Verify
- [ ] An out-of-bounds `vec[size()]` in a test traps in release builds (hardening active).
- [ ] `-Wunsafe-buffer-usage` clean in new/modified directories.
- [ ] No new `(T* ptr, size_t len)` public APIs.

## Checked

Date: 2026-10-25. Documentation: Microsoft GSL README and docs/headers.md (microsoft/GSL), libc++ Hardening and Clang SafeBuffers pages (llvm/llvm-project, head 2026-10-25), libstdc++ manual using.xml (gcc-mirror/gcc), microsoft/STL yvals.h, C++ Core Guidelines (isocpp/CppCoreGuidelines), C++ working draft (cplusplus/draft, head 2026-10-24), OpenSSF compiler hardening guide.

Confirmed: GSL `not_null`, `narrow` (throws `narrowing_error`), `narrow_cast`, `at`, `owner`, `finally`, `Expects`/`Ensures` (terminate), `Microsoft.GSL::GSL`, vcpkg `ms-gsl`; Bounds profile rules and the clang-tidy `cppcoreguidelines-pro-bounds-*` checks; libc++ hardening macros and modes; `_GLIBCXX_ASSERTIONS` (default at no optimisation); `_MSVC_STL_HARDENING` exists in microsoft/STL; `-Wunsafe-buffer-usage` and `#pragma clang unsafe_buffer_usage begin/end`; UBSan `-fsanitize=bounds`; `_FORTIFY_SOURCE=3`; span `at` and hardened implementations in the C++26 draft.
Removed as unconfirmed: LLVM 18 gate, the 1 percent overhead figure, `__builtin_trap`, Conan package name, "gsl::span predates std::span", and the span fix-it claim.

Method: documentation only; no commands were run.
