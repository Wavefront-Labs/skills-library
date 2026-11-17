---
id: computing-software.software-engineering.cpp.compiler-warnings-as-errors
name: compiler-warnings-as-errors
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, undefined-behavior, compiler-warnings, wall-wextra, werror, msvc-w4, gcc, clang, hardening-flags, fortify-source]
level: practitioner
status: docs-checked
description: "Set a strong C/C++ warning and hardening baseline for GCC, Clang and MSVC, make it -Werror in CI without blocking upgrades, and handle third-party headers."
sources: ["https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html", "https://clang.llvm.org/docs/DiagnosticsReference.html", "https://learn.microsoft.com/en-us/cpp/build/reference/compiler-option-warning-level", "https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compiler warnings as errors

**Goal:** let the compiler find bugs for free (uninitialised values, sign mix-ups,
fallthrough, shadowing), and keep the build warning-free so new warnings are noticed.

## Baseline flags
GCC / Clang:
```
-Wall -Wextra -Wpedantic -Wshadow -Wconversion -Wsign-conversion -Wnull-dereference
-Wdouble-promotion -Wformat=2 -Wimplicit-fallthrough -Wnon-virtual-dtor -Wold-style-cast
-Woverloaded-virtual -Wcast-align -Wuseless-cast(GCC) -Wduplicated-cond(GCC) -Wlogical-op(GCC)
```
MSVC: `/W4 /permissive-`; `/wNxxxx` options (for example `/w14242`) raise individual warnings to a chosen level.
`-Wall` is NOT all warnings; `-Weverything` (Clang) is too noisy for daily use but good
for an occasional audit.

## Hardening (release builds; OpenSSF guide)
```
-O2 -D_FORTIFY_SOURCE=3 -D_GLIBCXX_ASSERTIONS -fstack-protector-strong
-fstack-clash-protection -fcf-protection=full -ftrivial-auto-var-init=zero
-Wl,-z,relro,-z,now -pie -fPIE
```
The OpenSSF guide's baseline combines these with `-O2`; `-fcf-protection=full` is the x86_64 setting there.

## CMake
```cmake
add_library(project_warnings INTERFACE)
target_compile_options(project_warnings INTERFACE
  $<$<CXX_COMPILER_ID:GNU,Clang,AppleClang>:-Wall -Wextra -Wpedantic -Wshadow -Wconversion>
  $<$<CXX_COMPILER_ID:MSVC>:/W4 /permissive->)
target_link_libraries(myapp PRIVATE project_warnings)
set(CMAKE_COMPILE_WARNING_AS_ERROR ON)   # CMake 3.24+, overridable with --compile-no-warning-as-error
```
Apply warnings per target, not via global `CMAKE_CXX_FLAGS`, so third-party targets are unaffected.

## -Werror strategy
- Turn on `-Werror` in CI, but let developers and distro packagers disable it
  (`--compile-no-warning-as-error`): new compiler versions add warnings, and a library
  that hard-codes -Werror breaks downstream builds.
- Legacy code: enable flags, fix or baseline with targeted `-Wno-...` per target, then
  remove suppressions gradually. Never blanket `-w`.
- Third-party headers: include them as SYSTEM (`target_include_directories(x SYSTEM ...)`,
  `/external:I` + `/external:W0` on MSVC) so their warnings don't count.
- Local suppression with a reason: `#pragma GCC diagnostic push/ignored/pop` around the line.

## Verify
- [ ] CI builds with both GCC and Clang (they catch different things) at -Werror.
- [ ] Release binaries show RELRO, stack protector, NX and PIE when inspected with your platform's tools.

## Checked

Date: 2026-10-25. Documentation: GCC manual (gcc-mirror/gcc doc/invoke.texi), OpenSSF Compiler Options Hardening Guide (ossf/wg-best-practices-os-developers), CMake cmake(1) and CMAKE_COMPILE_WARNING_AS_ERROR (Kitware/CMake, head 2026-10-25), Microsoft C++ docs (MicrosoftDocs/cpp-docs).

Confirmed: each GCC warning in the baseline list exists (-Wuseless-cast, -Wduplicated-cond, -Wlogical-op, -Wnon-virtual-dtor, -Wold-style-cast, -Woverloaded-virtual, -Wcast-align, -Wnull-dereference, -Wdouble-promotion, -Wsign-conversion, -Wshadow); the hardening flags (-D_FORTIFY_SOURCE=3, -D_GLIBCXX_ASSERTIONS, -fstack-protector-strong, -fstack-clash-protection, -fcf-protection=full, -ftrivial-auto-var-init=zero, -Wl,-z,relro,-z,now, -fPIE -pie) appear in the OpenSSF guide; `CMAKE_COMPILE_WARNING_AS_ERROR` and `--compile-no-warning-as-error` are 3.24; MSVC `/W4`, `/permissive-`, `/external:I` and `/external:W0` are documented.
Removed as unconfirmed: the list of specific MSVC warning numbers and the checksec step.

Method: documentation only; no commands were run.
