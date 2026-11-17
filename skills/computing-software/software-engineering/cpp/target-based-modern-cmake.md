---
id: computing-software.software-engineering.cpp.target-based-modern-cmake
name: target-based-modern-cmake
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cmake, cpp-build, cmake-targets, modern-cmake, target-link-libraries, usage-requirements]
level: practitioner
status: docs-checked
description: "Write target-based modern CMake: add_library/add_executable, PUBLIC/PRIVATE/INTERFACE usage requirements, generator expressions, and installing exportable targets."
sources:
  - https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html
  - https://cmake.org/cmake/help/latest/command/target_link_libraries.html
  - https://cmake.org/cmake/help/latest/guide/importing-exporting/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Target-based modern CMake

**Goal:** each target declares its own sources, include paths, flags and dependencies, and those requirements propagate correctly to consumers.

## 1. Skeleton
```cmake
cmake_minimum_required(VERSION 3.24)
project(acme VERSION 1.4.0 LANGUAGES CXX)

add_library(money src/money.cpp src/currency.cpp)
add_library(acme::money ALIAS money)                 # namespaced name, same as after install
target_compile_features(money PUBLIC cxx_std_20)    # not CMAKE_CXX_FLAGS -std=...
target_include_directories(money
    PUBLIC  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
            $<INSTALL_INTERFACE:include>
    PRIVATE src)
target_link_libraries(money PRIVATE fmt::fmt PUBLIC acme::core)
target_compile_options(money PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra -Wpedantic>
    $<$<CXX_COMPILER_ID:MSVC>:/W4>)

add_executable(app src/main.cpp)
target_link_libraries(app PRIVATE acme::money)
```

## 2. PUBLIC / PRIVATE / INTERFACE
| Keyword | Used to build this target | Propagated to consumers |
|---|---|---|
| PRIVATE | yes | no |
| PUBLIC | yes | yes |
| INTERFACE | no | yes (header-only libs, usage-only flags) |
Rule: a dependency is PUBLIC only if it appears in your **public headers**. Over-using PUBLIC leaks include paths and slows builds; under-using causes "header not found" in consumers.
Header-only library: `add_library(span_lite INTERFACE)` + `target_include_directories(span_lite INTERFACE include)`.

## 3. Avoid directory-scoped commands
`include_directories()`, `link_libraries()`, `add_definitions()`, and editing `CMAKE_CXX_FLAGS` apply to everything in the directory and below, invisibly. Use `target_*` equivalents. Link with target names (`fmt::fmt`), never raw paths or `-lfoo`.

## 4. Install and export
```cmake
include(GNUInstallDirs)
install(TARGETS money EXPORT acmeTargets)
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(EXPORT acmeTargets NAMESPACE acme:: DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/acme)
include(CMakePackageConfigHelpers)
write_basic_package_version_file(acmeConfigVersion.cmake COMPATIBILITY SameMajorVersion)
configure_package_config_file(cmake/acmeConfig.cmake.in acmeConfig.cmake INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/acme)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/acmeConfig.cmake ${CMAKE_CURRENT_BINARY_DIR}/acmeConfigVersion.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/acme)
```
The config template must `find_dependency()` every PUBLIC dependency. Consumers then `find_package(acme 1.4 REQUIRED)` and link `acme::money`.

## 5. Build commands
```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
ctest --test-dir build --output-on-failure
cmake --install build --prefix /opt/acme
```
Always out-of-source builds.

## Gotchas
- `file(GLOB ...)` for sources does not notice new files without re-running CMake (`CONFIGURE_DEPENDS` helps, with a cost); list sources explicitly.
- Multi-config generators (Visual Studio, Ninja Multi-Config) ignore `CMAKE_BUILD_TYPE`; use `--config Release` and `$<CONFIG>` expressions.
- `BUILD_SHARED_LIBS` toggles `add_library` without a type; be explicit when it matters.

## Verify
- A separate consumer project finds the installed package with `find_package` and builds using only `acme::money`, and `cmake --build build --target help` lists the expected targets.

## Checked

Date: 2026-10-25. Documentation: CMake cmake-buildsystem(7), target_link_libraries, install and importing-exporting guide (Kitware/CMake Help sources, head 2026-10-25).

Confirmed: usage requirements via PRIVATE, PUBLIC and INTERFACE keywords; `BUILD_INTERFACE`/`INSTALL_INTERFACE`; `$<CXX_COMPILER_ID:GNU,Clang>` style (`$<LANG_COMPILER_ID:compiler_ids>`) expressions accept a list of compiler ids; `install(TARGETS ... EXPORT ...)` default destinations; `write_basic_package_version_file` COMPATIBILITY SameMajorVersion; `FILE_SET` requires 3.23.

Method: documentation only; no commands were run.
