---
id: computing-software.software-engineering.cpp.cmake-install-export-and-package-config
name: cmake-install-export-and-package-config
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, cmake, cmake-install, cmake-package-config, find-package, export-targets, gnuinstalldirs, library-packaging]
level: advanced
status: docs-checked
description: "Make a CMake library consumable with find_package: install() rules, exported targets with namespaces, generated Config and ConfigVersion files, and relocatable include paths."
sources: ["https://cmake.org/cmake/help/latest/guide/importing-exporting/index.html", "https://cmake.org/cmake/help/latest/command/install.html", "https://cmake.org/cmake/help/latest/module/CMakePackageConfigHelpers.html", "https://cmake.org/cmake/help/latest/module/GNUInstallDirs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# install(), export and package config files

**Goal:** after `cmake --install`, consumers write `find_package(MyLib 1.2 REQUIRED)` and
`target_link_libraries(app PRIVATE MyLib::mylib)` and get includes, defines and transitive
dependencies automatically.

## Library target with relocatable includes
```cmake
cmake_minimum_required(VERSION 3.23)
project(MyLib VERSION 1.4.0 LANGUAGES CXX)
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

add_library(mylib src/mylib.cpp)
add_library(MyLib::mylib ALIAS mylib)          # same name in-tree and installed
target_compile_features(mylib PUBLIC cxx_std_20)
target_include_directories(mylib PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)
find_package(fmt 10 REQUIRED)
target_link_libraries(mylib PUBLIC fmt::fmt)
set_target_properties(mylib PROPERTIES VERSION ${PROJECT_VERSION} SOVERSION ${PROJECT_VERSION_MAJOR})
```
Wrap build-tree include paths in `$<BUILD_INTERFACE:...>` and installed paths in `$<INSTALL_INTERFACE:...>` so
the exported package does not point back into your source tree. CMake 3.23+ `FILE_SET HEADERS` handles this neatly:
`target_sources(mylib PUBLIC FILE_SET HEADERS BASE_DIRS include FILES include/mylib/mylib.h)`.

## Install rules
```cmake
install(TARGETS mylib EXPORT MyLibTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}      # DLLs on Windows
    FILE_SET HEADERS)                                # or install(DIRECTORY include/ DESTINATION ...)

install(EXPORT MyLibTargets
    FILE MyLibTargets.cmake
    NAMESPACE MyLib::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib)
```

## Config and version files
cmake/MyLibConfig.cmake.in:
```cmake
@PACKAGE_INIT@
include(CMakeFindDependencyMacro)
find_dependency(fmt 10)                 # re-find PUBLIC dependencies for consumers
include("${CMAKE_CURRENT_LIST_DIR}/MyLibTargets.cmake")
check_required_components(MyLib)
```
```cmake
configure_package_config_file(cmake/MyLibConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib)
write_basic_package_version_file(${CMAKE_CURRENT_BINARY_DIR}/MyLibConfigVersion.cmake
    VERSION ${PROJECT_VERSION} COMPATIBILITY SameMajorVersion)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfig.cmake
              ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfigVersion.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib)
```
- `find_dependency` for every dependency in the exported link interface, or consumers fail with
  "target fmt::fmt not found".
- COMPATIBILITY: `SameMajorVersion` for semver libraries, `ExactVersion` for unstable ABI,
  `AnyNewerVersion` rarely.
- Header-only libraries: `ARCH_INDEPENDENT` in `write_basic_package_version_file`.

## Build tree export (optional)
`export(EXPORT MyLibTargets NAMESPACE MyLib:: FILE ${CMAKE_CURRENT_BINARY_DIR}/MyLibTargets.cmake)`
lets others use the build directory without installing.

## Test it like a consumer
```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build && cmake --install build --prefix stage
cmake -S tests/consumer -B build-consumer -DCMAKE_PREFIX_PATH="$PWD/stage" && cmake --build build-consumer
```
A tiny `tests/consumer` project with `find_package(MyLib REQUIRED)` run in CI catches broken
exports. Package managers (vcpkg ports, Conan recipes) build on exactly these install rules.

## Gotchas
- Multi-config generators install per configuration: `cmake --install build --config Release`.
- Set `CMAKE_DEBUG_POSTFIX d` to install Debug and Release side by side.
- Windows DLLs: export symbols (`GenerateExportHeader`) and install RUNTIME to bin.

## Verify
- [ ] Consumer project builds against the staged install using only `find_package`.
- [ ] Installed `MyLibTargets.cmake` contains no absolute source/build paths.
- [ ] A version mismatch (`find_package(MyLib 2.0)` against 1.4.0 with `SameMajorVersion`) is rejected.

## Checked

Date: 2026-10-25. Documentation: CMake reference (Kitware/CMake Help sources, head 2026-10-25).

Confirmed: `install(TARGETS ... FILE_SET HEADERS)` and `FILE_SET` added in 3.23 with default destination `include`; the importing and exporting guide for `find_dependency` and `check_required_components`; `write_basic_package_version_file` COMPATIBILITY values (AnyNewerVersion, SameMajorVersion, SameMinorVersion, ExactVersion) and `ARCH_INDEPENDENT`; `BUILD_INTERFACE` and `INSTALL_INTERFACE` usage in cmake-buildsystem; `cmake --install --prefix` and `--config`.
Removed as unconfirmed: that install(EXPORT) rejects absolute source paths, and the static-library PRIVATE dependency note.

Method: documentation only; no commands were run.
