---
id: computing-software.devops-ci-cd.build-systems.ninja-and-cmake-incremental-builds
name: ninja-and-cmake-incremental-builds
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, ninja, cmake-incremental, cmake, depfiles, ninja-explain, unity-builds]
level: practitioner
status: docs-checked
description: "Get fast, correct incremental C/C++ builds with CMake and Ninja: generator choice, depfiles, diagnosing unnecessary rebuilds with ninja -d explain, and avoiding reconfigure churn."
sources: ["https://ninja-build.org/manual.html", "https://cmake.org/cmake/help/latest/generator/Ninja.html", "https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html", "https://cmake.org/cmake/help/latest/prop_tgt/UNITY_BUILD_BATCH_SIZE.html", "https://cmake.org/cmake/help/latest/variable/CMAKE_LINKER_TYPE.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ninja and CMake incremental builds

## Use Ninja
```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo   # or "Ninja Multi-Config"
cmake --build build                      # Ninja runs in parallel by default
cmake --build build --target app -j 16
```
Ninja chooses its default parallelism from the CPU count (processors + 2 on machines with more than two CPUs), starts quickly on no-op builds, and records header dependencies from compiler depfiles (`/showIncludes` is handled for MSVC) so only what changed is rebuilt.

## Presets for consistency
```json
{ "version": 6,
  "configurePresets": [{ "name": "dev", "generator": "Ninja", "binaryDir": "build/dev",
    "cacheVariables": { "CMAKE_BUILD_TYPE": "Debug", "CMAKE_EXPORT_COMPILE_COMMANDS": "ON",
                        "CMAKE_CXX_COMPILER_LAUNCHER": "ccache" } }],
  "buildPresets": [{ "name": "dev", "configurePreset": "dev" }] }
```
`cmake --preset dev && cmake --build --preset dev`. The `version` field selects the preset schema version; check the cmake-presets manual for the CMake release each version requires.

## Why did it rebuild?
```bash
ninja -C build -d explain                      # explains what caused each command to run
ninja -C build -n                              # dry run: list what would run
ninja -C build -t deps src/foo.o               # dependencies stored in the .ninja_deps log
ninja -C build -t query app                    # inputs and outputs of a target
ninja -C build -t compdb > compile_commands.json
```
A build that has nothing to do prints `ninja: no work to do.`
Common causes of over-rebuilding:
- Generated headers rewritten on every build (a version header with a timestamp or git hash): write only if the content changed (`configure_file` only rewrites when content changes; custom commands can use `cmake -E copy_if_different`).
- A header included everywhere (config.h, precompiled header) that changes often.
- `file(GLOB ... CONFIGURE_DEPENDS)` re-checks the file list at build time and can re-run CMake.
- Timestamps reset by checkout or cache restore in CI (all files newer than outputs).
- Different absolute paths between builds invalidate ccache unless `base_dir` is set; moving the build directory rebuilds everything.

## Making incremental builds faster
- `target_precompile_headers()` for heavy stable headers (STL, Qt, Boost).
- `UNITY_BUILD ON` (with `UNITY_BUILD_BATCH_SIZE`, default 8 from `CMAKE_UNITY_BUILD_BATCH_SIZE`) speeds full builds but makes incremental rebuilds of one file coarser - enable in CI, not for developers.
- Split monolithic libraries; reduce header includes (forward declarations, `include-what-you-use`).
- Link time dominates big C++ incremental builds: choose a faster linker with `CMAKE_LINKER_TYPE` (CMake 3.29+; predefined types include `LLD`, `MOLD`, `GOLD`, `BFD`).
- `ninja -t graph | dot` shows the build graph.

## Verify
- [ ] A second `cmake --build` with no changes does no work (`ninja: no work to do.`).
- [ ] Touching one .cpp rebuilds one object plus relink; `-d explain` shows no unexpected inputs.

## Checked
Date: 2026-10-25. Documentation: Ninja manual and `src/ninja.cc` / `src/build.cc` (ninja-build/ninja), CMake help sources (Kitware/CMake: cmake-presets manual, `UNITY_BUILD_BATCH_SIZE`, `CMAKE_LINKER_TYPE`, `file()`, Ninja generator).
Confirmed: default parallelism (processors + 2 above two CPUs); `ninja: no work to do.`; `-d explain`; `-t deps`, `-t query`, `-t compdb`, `-t graph`; `/showIncludes` handling; `UNITY_BUILD_BATCH_SIZE` (default 8 when the variable is unset); `CMAKE_LINKER_TYPE` since 3.29 and its predefined types (including `MOLD`); `file(GLOB ... CONFIGURE_DEPENDS)`; preset `generator`, `binaryDir`, `cacheVariables`, `buildPresets` fields.
Removed: the `-MD` flag detail, the statement that Make with recursive Makefiles is "slower and less precise", `-gsplit-dwarf` and `ninjatracing` advice, and `head`/`wc` pipelines.
Method: documentation only; no commands were run.
