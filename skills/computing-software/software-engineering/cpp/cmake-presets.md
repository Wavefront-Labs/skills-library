---
id: computing-software.software-engineering.cpp.cmake-presets
name: cmake-presets
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cmake, cpp-build, cmake-presets, ci, build-configurations]
level: practitioner
status: docs-checked
description: "Standardise CMake configure, build and test settings with CMakePresets.json and CMakeUserPresets.json, shared by developers, IDEs and CI."
sources: ["https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html", "https://learn.microsoft.com/en-us/vcpkg/users/buildsystems/cmake-integration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CMakePresets.json

**Goal:** `cmake --preset ci-release` means the same generator, cache variables, toolchain and test options on every machine and in CI.

## 1. A presets file
```json
{
  "version": 6,
  "cmakeMinimumRequired": { "major": 3, "minor": 25 },
  "configurePresets": [
    {
      "name": "base", "hidden": true,
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/${presetName}",
      "cacheVariables": { "CMAKE_EXPORT_COMPILE_COMMANDS": "ON", "CMAKE_CXX_STANDARD": "20" }
    },
    { "name": "debug",   "inherits": "base", "cacheVariables": { "CMAKE_BUILD_TYPE": "Debug" } },
    { "name": "release", "inherits": "base", "cacheVariables": { "CMAKE_BUILD_TYPE": "Release" } },
    {
      "name": "asan", "inherits": "debug",
      "cacheVariables": { "CMAKE_CXX_FLAGS": "-fsanitize=address,undefined -fno-omit-frame-pointer" }
    },
    {
      "name": "vcpkg", "hidden": true,
      "toolchainFile": "$env{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake"
    },
    {
      "name": "windows-msvc", "inherits": ["base", "vcpkg"],
      "condition": { "type": "equals", "lhs": "${hostSystemName}", "rhs": "Windows" },
      "architecture": { "value": "x64", "strategy": "external" }
    }
  ],
  "buildPresets": [
    { "name": "debug", "configurePreset": "debug" },
    { "name": "release", "configurePreset": "release", "jobs": 0 }
  ],
  "testPresets": [
    { "name": "debug", "configurePreset": "debug",
      "output": { "outputOnFailure": true }, "execution": { "jobs": 8, "noTestsAction": "error" } }
  ],
  "workflowPresets": [
    { "name": "ci", "steps": [
      { "type": "configure", "name": "release" },
      { "type": "build", "name": "release" },
      { "type": "test", "name": "debug" } ] }
  ]
}
```

## 2. Commands
```bash
cmake --list-presets
cmake --preset debug
cmake --build --preset debug
ctest --preset debug
cmake --workflow --preset ci        # configure + build + test in one (schema v6, CMake 3.25+)
```

## 3. User presets
`CMakeUserPresets.json` (git-ignored) for personal tweaks: local compiler paths, extra flags, `inherits` from the shared presets. Never commit machine-specific paths into `CMakePresets.json`; use `$env{VAR}` and `$penv{VAR}` macros.

## 4. IDE integration
Editors and IDEs that support presets read the same file, so the IDE and CI can build the same way (check your IDE's documentation for the preset schema version it supports). `CMAKE_EXPORT_COMPILE_COMMANDS` is honoured only by the Makefile and Ninja generators and feeds clangd/clang-tidy.

## Gotchas
- Schema `version` must be supported by the oldest CMake you use; the file errors on older CMake.
- Hidden presets cannot be selected directly; they exist only to be inherited.
- To discard an existing `CMakeCache.txt` and reconfigure cleanly, run `cmake --fresh --preset x`.
- `condition` lets one file serve Windows/Linux/macOS without broken presets showing on the wrong host.

## Verify
- CI runs only `cmake --workflow --preset ci`, and a new developer builds with `cmake --preset debug && cmake --build --preset debug` with no other instructions.

## Checked

Date: 2026-10-25. Documentation: CMake cmake-presets(7) and its preset property pages (Kitware/CMake Help sources, head 2026-10-25) and cmake(1); vcpkg-docs (microsoft/vcpkg-docs, head 2026-10-20).

Confirmed: schema version 6 added workflow and package presets in CMake 3.25 (`cmake --workflow`), `toolchainFile` needs schema 3, `architecture.strategy` accepts `external`, `jobs: 0` equals `--parallel` with no number, `testPresets.execution.noTestsAction` has an `error` value, `--list-presets` and `--fresh`; the vcpkg toolchain path `<vcpkg-root>/scripts/buildsystems/vcpkg.cmake` with a `VCPKG_ROOT` preset example.
Removed as unconfirmed: the claim about which IDEs read presets and the claim about cacheVariables only applying on first configure. `sources` now lists only the CMake presets manual.

Method: documentation only; no commands were run.
