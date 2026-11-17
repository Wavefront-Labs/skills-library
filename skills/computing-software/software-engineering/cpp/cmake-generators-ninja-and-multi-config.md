---
id: computing-software.software-engineering.cpp.cmake-generators-ninja-and-multi-config
name: cmake-generators-ninja-and-multi-config
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, cmake, ninja, cmake-generators, ninja-multi-config, visual-studio-generator, xcode, build-types]
level: practitioner
status: docs-checked
description: "Choose CMake generators: Ninja for speed, Ninja Multi-Config, Visual Studio and Xcode; single vs multi-config build types, generator expressions, and switching safely."
sources: ["https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html", "https://cmake.org/cmake/help/latest/generator/Ninja%20Multi-Config.html", "https://cmake.org/cmake/help/latest/variable/CMAKE_BUILD_TYPE.html", "https://ninja-build.org/manual.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CMake generators (Ninja / Visual Studio / multi-config)

**Goal:** fast, correct builds on every platform and a mental model of single- vs multi-config
that stops "my Release build is actually Debug" bugs.

## Picking a generator
```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake -S . -B build -G "Ninja Multi-Config"
cmake -S . -B build -G "Visual Studio 17 2022" -A x64
cmake -S . -B build -G Xcode
cmake --help               # lists generators available on this machine
```
| Generator | Use |
|---|---|
| Ninja | common choice for CI and command line on all OSes; the Ninja generators (with Visual Studio 17 2022 and 18 2026) are the ones that can scan for C++20 modules, and need ninja 1.11 or newer |
| Ninja Multi-Config | one build dir with Debug/Release/RelWithDebInfo side by side |
| Unix Makefiles | default on many Unix hosts; not in CMake's list of generators that support C++ modules |
| Visual Studio 17 2022 (also Visual Studio 18 2026) | IDE solution files, MSBuild; multi-config |
| Xcode | Apple platforms, signing, IDE |
The generator is fixed per build directory: switching needs a fresh directory (or delete
CMakeCache.txt and CMakeFiles/). Set it once in `CMakePresets.json` (`"generator": "Ninja"`) or via
the `CMAKE_GENERATOR` environment variable.

## Single-config vs multi-config
- **Single-config** (Ninja, Makefiles): build type chosen at configure time with
  `CMAKE_BUILD_TYPE`. If unset the value is often an empty string (CMake's docs say this is usually not
  desirable), so no build-type flags are applied. Default it in your project:
```cmake
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING "" FORCE)
endif()
```
- **Multi-config** (VS, Xcode, Ninja Multi-Config): `CMAKE_BUILD_TYPE` is **ignored**; choose at
  build time: `cmake --build build --config Release`, `ctest -C Release`,
  `cmake --install build --config Release`. Forgetting `--config` builds Debug.
- Therefore never write `if(CMAKE_BUILD_TYPE STREQUAL "Debug")` in project logic; use generator
  expressions, which work for both:
```cmake
target_compile_definitions(app PRIVATE $<$<CONFIG:Debug>:APP_DEBUG_CHECKS>)
target_compile_options(app PRIVATE $<$<AND:$<CXX_COMPILER_ID:GNU,Clang>,$<CONFIG:Release>>:-O3>)
```
- Output paths differ: multi-config adds a per-config subdirectory (`build/Release/app.exe`). Use
  `$<TARGET_FILE:app>` instead of hard-coded paths.

## Ninja tips
```bash
cmake --build build -j 16            # ninja already parallelises by default, based on the CPU count
cmake --build build --target app -- -v   # show full command lines
ninja -C build -t targets all
ninja -C build -t compdb > compile_commands.json
```
- Job pools to limit memory-hungry link steps:
  `set_property(GLOBAL PROPERTY JOB_POOLS link=2)` + `set(CMAKE_JOB_POOL_LINK link)`.
- On Windows run Ninja from a VS Developer Prompt (or `vcvarsall.bat x64`) so `cl.exe` is found;
  CMake presets can do this via the toolset and `"architecture": {"strategy": "external"}`.

## Ninja Multi-Config specifics
`cmake --build build --config Debug`. `CMAKE_CONFIGURATION_TYPES` defaults to `Debug;Release;RelWithDebInfo`,
`CMAKE_DEFAULT_BUILD_TYPE` picks the configuration used by the plain `build.ninja`, and
`CMAKE_CROSS_CONFIGS` lists configurations that can be built from every `build-<Config>.ninja` file
(for example building a tool in Release while building Debug targets).

## Verify
- [ ] Presets define generator and build type; CI uses them.
- [ ] No `CMAKE_BUILD_TYPE` comparisons in CMakeLists (grep).
- [ ] `--config` passed on every multi-config build/test/install command in scripts.

## Checked

Date: 2026-10-25. Documentation: CMake reference (Kitware/CMake Help sources, head 2026-10-25) and the Ninja manual (ninja-build/ninja doc/manual.asciidoc).

Confirmed: CMAKE_BUILD_TYPE applies to single-config generators and its default is often an empty string; Ninja Multi-Config variables (CMAKE_CONFIGURATION_TYPES default, CMAKE_CROSS_CONFIGS, CMAKE_DEFAULT_BUILD_TYPE); the C++ modules generator list (Ninja, Ninja Multi-Config, Visual Studio 17 2022, Visual Studio 18 2026, ninja 1.11+); GLOBAL JOB_POOLS and CMAKE_JOB_POOL_LINK; ninja default parallelism by CPU count, `-t targets all` and `-t compdb`.
Removed as unconfirmed: the "cores + 2" figure and the `-d explain` tip.

Method: documentation only; no commands were run.
