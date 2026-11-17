---
id: computing-software.software-engineering.cpp.faster-builds-with-ccache-unity-builds-and-pch
name: faster-builds-with-ccache-unity-builds-and-pch
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cmake, cpp-build, ccache, precompiled-headers, unity-builds, build-performance, include-hygiene]
level: practitioner
status: docs-checked
description: "Cut C++ build times with ccache/sccache, precompiled headers, unity builds, Ninja, faster linkers and include hygiene, and measure where build time goes."
sources:
  - https://ccache.dev/manual/latest.html
  - https://cmake.org/cmake/help/latest/command/target_precompile_headers.html
  - https://cmake.org/cmake/help/latest/prop_tgt/UNITY_BUILD.html
  - https://github.com/aras-p/ClangBuildAnalyzer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Faster C++ builds: ccache, unity builds and PCH

**Goal:** shorter edit-compile cycles and CI times, guided by measurement.

## 1. Measure first
- Clang: `-ftime-trace` per TU, aggregate with ClangBuildAnalyzer to find expensive headers and templates.
- GCC: `-ftime-report`. Other compilers and Ninja have their own timing tools; measure wall time at minimum.

## 2. Compiler cache
```cmake
find_program(CCACHE ccache)
if(CCACHE)
  set(CMAKE_CXX_COMPILER_LAUNCHER ${CCACHE})
  set(CMAKE_C_COMPILER_LAUNCHER ${CCACHE})
endif()
```
```bash
ccache -s                # statistics (--show-stats)
ccache --max-size=20G    # -M
```
CI: persist the cache directory between runs. Hits require identical command lines and paths: set `base_dir` (`CCACHE_BASEDIR`) to the workspace root so absolute paths are rewritten as relative ones.

## 3. Precompiled headers
```cmake
target_precompile_headers(core PRIVATE <vector> <string> <unordered_map> <fmt/format.h> "include/core/common.h")
target_precompile_headers(app REUSE_FROM core)     # share one PCH across targets with identical flags
```
Put stable, heavy, widely used headers in the PCH; never frequently edited project headers (every edit rebuilds everything). Do not rely on PCH for correctness: each file must still include what it uses.

## 4. Unity (jumbo) builds
```cmake
set_target_properties(core PROPERTIES UNITY_BUILD ON UNITY_BUILD_BATCH_SIZE 16)
# or globally: cmake -DCMAKE_UNITY_BUILD=ON
```
Combines several .cpp files into one TU: fewer header re-parses. Breaks on file-local name clashes (`static` functions, anonymous namespaces with the same names, `using namespace` leaks); fix them or exclude files (`SKIP_UNITY_BUILD_INCLUSION`). Good for CI full builds; less helpful for incremental edits.

## 5. Other big levers
- Ninja instead of Make; Ninja already runs jobs in parallel by CPU count (watch RAM for heavy templates).
- Faster linkers: `lld` or `mold` (`-DCMAKE_LINKER_TYPE=MOLD`, CMake 3.29+); split DWARF (`-gsplit-dwarf`) separates debug information from the objects.
- Include hygiene: forward declarations, pimpl for heavy dependencies, avoid including `<iostream>`/`<regex>`/big template libraries in headers; include-what-you-use to prune.
- Explicit template instantiation (`extern template`) for heavy templates used everywhere.
- C++20 modules / `import std;` where your toolchain supports them reliably.

## Gotchas
- ccache treats code using `__DATE__`/`__TIME__` specially and absolute paths in command lines cause misses; the `sloppiness` setting (`CCACHE_SLOPPINESS`) can relax some checks.
- PCH with differing compile flags across targets cannot be reused; REUSE_FROM fails.
- Unity builds can hide missing includes (another file in the batch included it); keep a non-unity CI job.

## Verify
- Record clean and incremental build times before and after each change, and check the ccache hit rate on a second CI run.

## Checked

Date: 2026-10-25. Documentation: ccache manual (ccache/ccache doc/manual.adoc), CMake reference pages for UNITY_BUILD, UNITY_BUILD_BATCH_SIZE, SKIP_UNITY_BUILD_INCLUSION, target_precompile_headers and CMAKE_LINKER_TYPE (Kitware/CMake, head 2026-10-25), GCC manual.

Confirmed: ccache `-s/--show-stats`, `-M/--max-size`, `base_dir`/CCACHE_BASEDIR, `sloppiness`/CCACHE_SLOPPINESS and `__DATE__`/`__TIME__` handling; `UNITY_BUILD_BATCH_SIZE` (initialised from CMAKE_UNITY_BUILD_BATCH_SIZE), `SKIP_UNITY_BUILD_INCLUSION` (3.16); `REUSE_FROM`; `CMAKE_LINKER_TYPE` (3.29) with `MOLD` and `LLD` values; GCC `-ftime-report`, `-gsplit-dwarf`; Ninja's default parallelism.
Removed as unconfirmed: the ccache MSVC/`/Z7` version claim, sccache backends, the 2-4x speed-up and 90 percent hit-rate figures, MSVC timing flags and ninjatracing.

Method: documentation only; no commands were run.
