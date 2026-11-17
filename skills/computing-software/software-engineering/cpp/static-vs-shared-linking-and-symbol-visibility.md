---
id: computing-software.software-engineering.cpp.static-vs-shared-linking-and-symbol-visibility
name: static-vs-shared-linking-and-symbol-visibility
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cmake, cpp-build, shared-libraries, symbol-visibility, abi, rpath, static-linking, cpp-linking]
level: practitioner
status: docs-checked
description: "Choose static vs shared libraries in C++: symbol visibility and export macros, ABI stability, SONAME versioning, RPATH, and diagnosing undefined symbol and ODR problems."
sources: ["https://cmake.org/cmake/help/latest/module/GenerateExportHeader.html", "https://cmake.org/cmake/help/latest/prop_tgt/SOVERSION.html", "https://cmake.org/cmake/help/latest/prop_tgt/LANG_VISIBILITY_PRESET.html", "https://gcc.gnu.org/onlinedocs/gcc/C_002b_002b-Dialect-Options.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Static vs shared linking and symbol visibility

**Goal:** libraries that link predictably, export only their public API, and can be updated without breaking dependants when ABI promises are made.

## 1. Trade-offs
| | Static (.a/.lib) | Shared (.so/.dylib/.dll) |
|---|---|---|
| Deployment | single binary | ship and locate the library |
| Updates | rebuild dependants | replace library (if ABI-compatible) |
| Size/memory | duplicated per binary | shared pages |
| Link-time optimisation | whole program | across the boundary only with care |
| Globals/singletons | one copy per linked binary (duplicates if linked into several .so) | one copy |

## 2. Visibility: hide by default
```cmake
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN ON)
add_library(acme SHARED src/acme.cpp)
include(GenerateExportHeader)
generate_export_header(acme)          # acme_export.h with ACME_EXPORT
target_include_directories(acme PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>)
```
```cpp
#include "acme_export.h"
class ACME_EXPORT Client { public: void send(); };
ACME_EXPORT int acme_version();
```
On Windows, DLLs export nothing unless marked (`__declspec(dllexport)`); hidden-by-default on GCC/Clang matches that model and prevents accidental ABI surface. Inspect the dynamic symbol table with your platform's tools (for example `nm -D` on Linux).

## 3. ABI stability rules (if you promise it)
Breaking: changing class layout (adding/removing/reordering members, base classes), changing virtual function order or adding virtuals, changing inline functions' behaviour, changing function signatures, templates in the API, changing enum underlying values. Techniques: pimpl (`std::unique_ptr<Impl>`), C API boundary (`extern "C"`), versioned inline namespaces. Compare releases with an ABI checking tool such as libabigail.

## 4. Versioning and lookup (Linux)
```cmake
set_target_properties(acme PROPERTIES VERSION 1.4.2 SOVERSION 1)   # libacme.so.1.4.2, SONAME libacme.so.1
set(CMAKE_INSTALL_RPATH "$ORIGIN/../lib")                          # find libs relative to the executable
```
Runtime search: RPATH/RUNPATH, `LD_LIBRARY_PATH`, system dirs (`ldconfig`). macOS uses install names and `@rpath`; Windows searches the exe directory and PATH. `ldd app` / `otool -L app` show what resolves.

## 5. Common errors
- `undefined reference to X`: library missing from the link line, wrong order with static libs (GNU ld resolves left to right: dependants before dependencies), or symbol hidden.
- `multiple definition` / ODR violations: the same static library linked into two shared libraries plus the exe gives duplicate globals and two singletons; link static libs into exactly one shared object or make them shared.
- Mixed C++ standard libraries or `_GLIBCXX_USE_CXX11_ABI` values across binaries: crashes at boundaries passing `std::string`.

## Gotchas
- Exceptions and RTTI across shared library boundaries require the type info to be exported (default visibility for exception classes).
- `-fPIC` is required for code going into shared libraries (`POSITION_INDEPENDENT_CODE ON` for static libs linked into them).
- Windows: do not free memory across DLLs that use different C runtimes.

## Verify
- `nm -DC` lists only intended exports, `ldd`/`otool -L` resolve from the install location, and an ABI checker reports no changes between patch releases.

## Checked

Date: 2026-10-25. Documentation: CMake property and variable pages (Kitware/CMake Help sources, head 2026-10-25) and the GCC manual (gcc-mirror/gcc doc/invoke.texi).

Confirmed: `CMAKE_<LANG>_VISIBILITY_PRESET` initialises the `<LANG>_VISIBILITY_PRESET` property that sets `-fvisibility=`; `VERSION` and `SOVERSION` define the build and ABI versions and create so-name symlinks; `-fvisibility-inlines-hidden` is a GCC option; GenerateExportHeader and POSITION_INDEPENDENT_CODE exist.
Removed as unconfirmed: the glibc static-NSS note, the symbol-table speed claim, tool command lines (`dumpbin`, `abidiff`) that no fetched page covers.

Method: documentation only; no commands were run.
