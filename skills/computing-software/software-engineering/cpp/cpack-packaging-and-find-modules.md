---
id: computing-software.software-engineering.cpp.cpack-packaging-and-find-modules
name: cpack-packaging-and-find-modules
category: computing-software
field: software-engineering
product: cpp
tags: [cmake, cmake-testing, cmake-ts-cpack, cmake-compile, cmake-cp-findmod, cmake-cp-features, cpack, find-module, compile-features, cxx-std, cpack-packaging, find-module-authoring, compile-features-standards]
level: practitioner
status: docs-checked
description: "Package with CPack, write FindXxx.cmake modules with imported targets, and request language standards via compile features."
sources:
  - https://cmake.org/cmake/help/latest/module/CPack.html
  - https://cmake.org/cmake/help/latest/manual/cmake-developer.7.html
  - https://cmake.org/cmake/help/latest/manual/cmake-compile-features.7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPack, find modules and compile features

## CPack
```cmake
include(GNUInstallDirs)
install(TARGETS app RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
set(CPACK_PACKAGE_NAME "myapp")
set(CPACK_PACKAGE_VENDOR "Example Org")
set(CPACK_GENERATOR "TGZ;ZIP")
include(CPack)    # after the CPACK_ variables are set
```
- `include(CPack)` writes `CPackConfig.cmake` and `CPackSourceConfig.cmake`, which a later `cpack` run uses.
- Binary installers contain what `install()` installed. The `DESTINATION` must be a relative path or CPack ignores the files.
- In `CMakeLists.txt`, `CPACK_GENERATOR` is a list: `cpack` with no arguments makes one package per entry. `-G` overrides the list. Per-generator overrides go in a file named by `CPACK_PROJECT_CONFIG_FILE`, where `CPACK_GENERATOR` is a single generator.
- With Makefile, Ninja or Xcode generators `include(CPack)` adds a `package` target (`PACKAGE` for Visual Studio); Makefile and Ninja also get `package_source`.
- `CPACK_PACKAGE_NAME` defaults to the project name; `CPACK_PACKAGE_VENDOR` defaults to "Humanity". Source packages include everything in the project directory except `CPACK_SOURCE_IGNORE_FILES`.
- Generator-specific settings are documented per generator in `cpack-generators(7)`; check there before setting any.

## Find modules for dependencies without a config package
```cmake
# cmake/FindFoo.cmake
find_path(Foo_INCLUDE_DIR foo/foo.h)
find_library(Foo_LIBRARY NAMES foo)
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Foo REQUIRED_VARS Foo_LIBRARY Foo_INCLUDE_DIR)
if(Foo_FOUND AND NOT TARGET Foo::Foo)
  add_library(Foo::Foo UNKNOWN IMPORTED)
  set_target_properties(Foo::Foo PROPERTIES
    IMPORTED_LOCATION "${Foo_LIBRARY}"
    INTERFACE_INCLUDE_DIRECTORIES "${Foo_INCLUDE_DIR}")
endif()
mark_as_advanced(Foo_INCLUDE_DIR Foo_LIBRARY)
```
- A find module is for packages whose upstream provides no config file. Its job is to set `<PackageName>_FOUND` and provide variables and imported targets.
- The modern approach is imported targets, which propagate usage requirements to consumers. Namespace them (`Foo::Foo`); names containing `::` get a diagnostic if the target does not exist.
- `find_package_handle_standard_args` checks the `REQUIRED_VARS` hold values not ending in `-NOTFOUND`, sets `Foo_FOUND`, checks `VERSION_VAR` against a requested version, and prints a message.
- Honour `Foo_FIND_QUIETLY` and `Foo_FIND_REQUIRED` (the latter means `FATAL_ERROR` when not found); the standard-args helper does this for you.
- `UNKNOWN` as the imported library type lets CMake inspect the file, which suits static or shared results.
- Target properties like `INTERFACE_INCLUDE_DIRECTORIES` describe the target itself only; express its dependencies as other targets.
- Mark most cache variables advanced. For debug and release binaries, `Foo_LIBRARY_RELEASE` and `Foo_LIBRARY_DEBUG` with `IMPORTED_CONFIGURATIONS` is the documented pattern, release listed first.

## Compile features and standards
```cmake
target_compile_features(lib PUBLIC cxx_std_20)
set_target_properties(lib PROPERTIES CXX_EXTENSIONS OFF)
```
- A `cxx_std_NN` meta-feature requires a compiler mode of at least that standard, possibly greater. CMake adds a flag like `-std=gnu++11` only if needed; with `PUBLIC` it applies to dependents too.
- It does not guarantee any particular language feature exists; unsupported use is diagnosed at compile time.
- The `-std=` flag may be omitted if the compiler default is already enough, but is still added if the default extensions mode differs from the `CXX_EXTENSIONS` property, or if `CXX_STANDARD` is set.
- `CXX_EXTENSIONS` defaults to the compiler's default (`CMAKE_CXX_EXTENSIONS_DEFAULT`); most compilers enable extensions, which can hide portability bugs. See policy `CMP0128`.
- `CMAKE_CXX_COMPILE_FEATURES` lists the features the compiler supports.

## Verify
- [ ] `cmake --build build --target package`, then list the archive contents and confirm only intended files are present.
- [ ] `find_package(Foo REQUIRED)` fails with a clear message when the library is absent.

## Checked
Method: docs-checked 2026-11-09 against the CPack module, cmake-developer(7) and cmake-compile-features(7) pages on cmake.org (latest). Dropped DEB/RPM-specific variables, cpack command-line flags, CMP0074 and per-version cxx_std claims, which the pages read do not confirm.
