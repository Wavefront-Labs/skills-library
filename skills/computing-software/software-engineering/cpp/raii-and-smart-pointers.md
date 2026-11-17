---
id: computing-software.software-engineering.cpp.raii-and-smart-pointers
name: raii-and-smart-pointers
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, raii, smart-pointers, unique-ptr, shared-ptr, weak-ptr, make-unique, make-shared, rule-of-zero, rule-of-five, move-semantics, destructors, memory-safety, sanitizers, asan, ubsan, addresssanitizer, lsan, tsan, cmake, clang-tidy, valgrind, cpp-core-guidelines, cpp-resource]
level: practitioner
status: docs-checked
description: "Manage every resource with RAII in modern C++: choosing unique_ptr/shared_ptr/weak_ptr, the rule of zero vs five, and catching leaks and UB with ASan/UBSan wired into CMake."
sources: ["https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines", "https://clang.llvm.org/docs/AddressSanitizer.html", "https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html", "https://github.com/cplusplus/draft"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# RAII and smart pointers — no naked new/delete, no leaks, sanitizers on

**Goal:** every resource (memory, file, socket, lock, GPU handle) is owned by an object
whose destructor releases it; ownership is visible in types; ASan/UBSan catch what
slips through.

## 1. RAII in one sentence
Acquire in a constructor (or factory), release in the destructor, and let scope do the
rest — this is what makes code exception-safe and early-return-safe. Standard RAII
types already exist: `std::vector`, `std::string`, `std::fstream`,
`std::lock_guard`/`std::scoped_lock`, `std::unique_lock`, `std::jthread` (joins on
destruction). Wrap C APIs with a custom deleter rather than writing a class:
```cpp
struct FileCloser { void operator()(FILE* f) const noexcept { if (f) std::fclose(f); } };
using FilePtr = std::unique_ptr<FILE, FileCloser>;
FilePtr f{std::fopen(path, "rb")};
if (!f) throw std::system_error(errno, std::generic_category(), path);
```

## 2. Choosing a pointer
| Type | Meaning |
|---|---|
| `std::unique_ptr<T>` | sole owner; move-only |
| `std::shared_ptr<T>` | shared ownership, reference counted |
| `std::weak_ptr<T>` | non-owning observer of a shared_ptr; `lock()` to use |
| `T*` / `T&` | non-owning, must not outlive owner |
Prefer `unique_ptr` unless you need to share ownership (Core Guidelines R.21).
Create with `std::make_unique` / `std::make_shared`; the standard says `make_shared` should perform no more than one allocation.

Parameter conventions (Core Guidelines R.32-R.36): `std::unique_ptr<T>` by value to take ownership;
`std::shared_ptr<T>` by value to express shared ownership; `std::shared_ptr<T>&` if the function might reseat it;
`const std::shared_ptr<T>&` if it might retain a reference count. Otherwise take `T&`/`T*`.

## 3. Rule of zero, rule of five
- **Rule of zero** (the goal): members are RAII types, so you declare no destructor,
  copy or move operations — the compiler-generated ones are correct.
- **Rule of five** (C.21): if you define or `= delete` any copy, move or destructor function, define or
  `= delete` them all.
- Make move operations `noexcept` (C.66).
- Polymorphic base: the destructor should be public and virtual, or protected and non-virtual (C.35).

## 4. Sanitizers and CMake
```cmake
cmake_minimum_required(VERSION 3.25)
project(app CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)        # for clang-tidy / clangd
option(ENABLE_SANITIZERS "ASan+UBSan" OFF)
if(ENABLE_SANITIZERS)
  add_compile_options(-fsanitize=address,undefined -fno-sanitize-recover=undefined -fno-omit-frame-pointer -g -O1)
  add_link_options(-fsanitize=address,undefined)
endif()
add_compile_options(-Wall -Wextra -Wpedantic -Werror=return-type)
```
Run CI with `-DENABLE_SANITIZERS=ON` and:
```
ASAN_OPTIONS=detect_leaks=1 \
UBSAN_OPTIONS=print_stacktrace=1 ctest --output-on-failure
```
- ASan: use-after-free, buffer overflows, double free, leaks (LeakSanitizer is on by
  default on Linux; enable it on macOS with `ASAN_OPTIONS=detect_leaks=1`). Typical slowdown 2x.
- UBSan: signed overflow, misaligned access and more. For most checks it prints and continues, so
  tests stay green unless you pass `-fno-sanitize-recover=...`.
- TSan (`-fsanitize=thread`) in a **separate** build.
- MSVC: `/fsanitize=address`. Hardened libc++/libstdc++ modes
  (`_GLIBCXX_ASSERTIONS`, libc++ hardening) add bounds and precondition checks.
- clang-tidy checks: `cppcoreguidelines-owning-memory`, `modernize-make-unique`,
  `bugprone-use-after-move`.

## Gotchas
- `shared_ptr` cycles (parent ↔ child) never free — make the back-edge `weak_ptr`.
- The `shared_ptr` constructor taking a `weak_ptr` throws `bad_weak_ptr` when the object is gone.
- Never build two `shared_ptr`s from the same raw pointer; use `make_shared` or copy the first.
- Destructors must never fail (Core Guidelines E.16).
- Dangling views: `std::string_view`/`std::span` of a temporary compile fine and are
  RAII-invisible.

## Verify
- [ ] No naked `new`/`delete` outside low-level containers (grep and clang-tidy clean).
- [ ] Classes follow rule of zero, or define/delete all five with `noexcept` moves.
- [ ] Polymorphic bases have virtual or protected destructors.
- [ ] CI has an ASan+UBSan job with `halt_on_error=1`, and a separate TSan job for threaded code.
- [ ] Any `shared_ptr` back-references are `weak_ptr`.
- [ ] Tests pass under sanitizers with zero reports.

Related: computing-software.software-engineering.rust.ownership-and-borrowing

## Checked

Date: 2026-10-25. Documentation: C++ Core Guidelines (isocpp/CppCoreGuidelines R.21, R.32-R.36, C.21, C.35, C.66, E.6, E.16), Clang AddressSanitizer and UndefinedBehaviorSanitizer pages (llvm/llvm-project, head 2026-10-25), C++ working draft (cplusplus/draft, head 2026-10-24: make_shared allocation note, bad_weak_ptr), Microsoft C++ docs for /fsanitize.

Confirmed: the rules cited above; ASan 2x slowdown, LeakSanitizer default on Linux and `detect_leaks` on macOS; `UBSAN_OPTIONS=print_stacktrace=1`; UBSan continues after most checks unless `-fno-sanitize-recover`; `/fsanitize=address` in MSVC; clang-tidy `cppcoreguidelines-owning-memory`, `modernize-make-unique`, `bugprone-use-after-move`.
Removed as unconfirmed: pointer cost column, pimpl destructor note, `abort_on_error`, `halt_on_error`, memory-overhead figure, the TSan/ASan combination rule, shared_from_this and make_shared lifetime notes, and the thread-safety note on refcounts. `sources` now lists fetched pages.

Method: documentation only; no commands were run.
