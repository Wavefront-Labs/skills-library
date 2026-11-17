---
id: computing-software.software-engineering.cpp.cpp20-modules
name: cpp20-modules
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, cpp-modules, c++20, import-std, cmake, module-interface-units, build-times, cpp-modern]
level: advanced
status: docs-checked
description: "Adopt C++20 modules: interface and implementation units, partitions, import std (C++23), CMake FILE_SET CXX_MODULES with Ninja, compiler support and migration traps."
sources: ["https://cmake.org/cmake/help/latest/manual/cmake-cxxmodules.7.html", "https://gcc.gnu.org/onlinedocs/gcc/C_002b_002b-Modules.html", "https://learn.microsoft.com/en-us/cpp/cpp/modules-cpp", "https://clang.llvm.org/docs/StandardCPlusPlusModules.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# C++20 modules

**Goal:** replace textual header inclusion with compiled module interfaces for isolation (no macro
leakage) and faster builds, where your toolchain supports it.

## Units
```cpp
// math.cppm  (primary module interface unit; MSVC prefers .ixx)
module;                        // global module fragment: legacy #includes go here
#include <cmath>
export module math;            // module declaration
export namespace math {
    double hypot(double a, double b);
    template <class T> T square(T x) { return x * x; }   // templates stay in the interface
}
int helper();                  // not exported: invisible to importers

// math.cpp  (module implementation unit)
module math;
double math::hypot(double a, double b) { return std::sqrt(square(a) + square(b)); }

// main.cpp
import math;
import std;                    // C++23 standard library module
int main() { std::println("{}", math::hypot(3, 4)); }
```
- Partitions: `export module math:geometry;` in one file, `export import :geometry;` in the primary
  interface.
- Macros do not cross `import` boundaries (a feature). Configuration macros must be passed as
  compiler definitions or replaced by constexpr variables.
- `import <vector>;` header units exist, but CMake's modules manual does not describe support for them; prefer `import std;`
  or `#include` in the global module fragment.

## Build system: CMake 3.28+ with Ninja
```cmake
cmake_minimum_required(VERSION 3.28)
project(app CXX)
set(CMAKE_CXX_STANDARD 23)
add_library(math)
target_sources(math PUBLIC FILE_SET CXX_MODULES FILES math.cppm PRIVATE math.cpp)
add_executable(app main.cpp)
target_link_libraries(app PRIVATE math)
```
- Modules require dependency scanning (the build must compile interfaces before importers): CMake lists the
  Ninja, Ninja Multi-Config, Visual Studio 17 2022 and Visual Studio 18 2026 generators (ninja 1.11 or newer);
  Unix Makefiles is not on the list.
- `import std;` is documented in CMake's modules manual from CMake 4.5, for the Ninja generators only, with
  Clang 18.1.2+ (libc++ or libstdc++), MSVC toolset 14.36+ or GCC 15+ (GCC 16+ on macOS); earlier CMake
  releases gated it behind experimental settings, so read the manual for your CMake version.
- Compiled module interfaces (BMIs) are compiler- and flag-specific build artefacts; ship the module interface
  sources, not the BMIs.

## Compiler status (check your versions)
CMake can scan sources for modules with MSVC toolset 14.34+ (VS 17.4+), LLVM/Clang 16.0+ and GCC 14+. GCC enables
modules with `-fmodules`. Editor and clangd support varies - verify code completion before migrating a large
codebase.

## Migration approach
1. Turn on `import std;` in new leaf code first (biggest compile-time win per effort).
2. Wrap a self-contained library: create a module interface that `#include`s its headers in the
   global module fragment and `export using ns::Thing;` - existing headers keep working.
4. Cyclic module dependencies are errors; restructure into partitions or a lower-level module.

## Verify
- [ ] Clean build with Ninja succeeds from scratch and after touching an interface.
- [ ] Measured compile-time improvement (wall time or your build profiler).
- [ ] Editor tooling (clangd/IntelliSense) still navigates the code.

## Checked

Date: 2026-10-25. Documentation: CMake cmake-cxxmodules(7) (Kitware/CMake Help sources, head 2026-10-25) and the GCC manual (gcc-mirror/gcc doc/invoke.texi).

Confirmed: modules support added in CMake 3.28 with `FILE_SET` type `CXX_MODULES`; supported-generator list and ninja 1.11 requirement; scanning compiler list (MSVC 14.34+, Clang 16+, GCC 14+); `import std` toolchain list (CMake 4.5); GCC `-fmodules`.
Removed as unconfirmed: header-unit tooling claims, the `CMAKE_CXX_MODULE_STD` gate and 3.30 figure (not in the current manual), BMI file extensions, the mixed include/import note.

Method: documentation only; no commands were run.
