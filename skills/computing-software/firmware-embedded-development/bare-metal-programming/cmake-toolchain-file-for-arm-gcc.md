---
id: computing-software.firmware-embedded-development.bare-metal-programming.cmake-toolchain-file-for-arm-gcc
name: cmake-toolchain-file-for-arm-gcc
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [cmake-toolchain-file, cmake, cross-compiling, arm-none-eabi-gcc, try-compile, cmake-presets, bare-metal-build, ninja, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write a CMake toolchain file for arm-none-eabi bare-metal builds: CMAKE_SYSTEM_NAME Generic, STATIC_LIBRARY try_compile, find-root modes, and CPU flags shared by compile and link."
sources:
  - https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html
  - https://cmake.org/cmake/help/latest/variable/CMAKE_TRY_COMPILE_TARGET_TYPE.html
  - https://cmake.org/cmake/help/latest/command/target_link_options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CMake toolchain file for bare-metal

**Goal:** configure CMake with a toolchain file so an `arm-none-eabi-` GCC builds a Cortex-M
image from any host.

## arm-gcc-toolchain.cmake
```cmake
set(CMAKE_SYSTEM_NAME Generic)          # bare metal: must be set to enable cross compiling
set(CMAKE_SYSTEM_PROCESSOR arm)
set(TOOLCHAIN_PREFIX arm-none-eabi-)
set(CMAKE_C_COMPILER   ${TOOLCHAIN_PREFIX}gcc)
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PREFIX}g++)
set(CMAKE_ASM_COMPILER ${TOOLCHAIN_PREFIX}gcc)

# compiler checks cannot link without a linker script / startup code
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
```
Points the CMake toolchains manual states:
- `CMAKE_SYSTEM_NAME` set to `Generic` is how an embedded target without an OS is declared, and
  setting it enables cross compiling.
- For toolchains that cannot link a binary without custom flags or scripts, set
  `CMAKE_TRY_COMPILE_TARGET_TYPE` to `STATIC_LIBRARY` so the compiler checks only compile and archive.
- By default `find_*` commands also search the host system; the `CMAKE_FIND_ROOT_PATH_MODE_*`
  settings above restrict libraries, includes and packages to the target root while still
  running host programs.
- Avoid `CMAKE_SOURCE_DIR` and `CMAKE_BINARY_DIR` inside a toolchain file: it is used in contexts
  (such as try_compile projects) where they have different values.

## CPU flags in both compile and link
Cortex-M multilib selection needs the same `-mcpu`, `-mthumb`, `-mfpu` and `-mfloat-abi` flags on
the link line as on compile lines. In the project:
```cmake
set(CPU_FLAGS -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard)
target_compile_options(fw PRIVATE ${CPU_FLAGS})
target_link_options(fw PRIVATE ${CPU_FLAGS})
```
`target_link_options` does not apply to static library targets, because they do not use a linker.
Add a linker script with `target_link_options` as well (for example `-T<path to .ld>`), and pass
`-Wl,-Map=...` for a map file.

## Gotchas
- CMake caches the results of its toolchain tests, so after changing the toolchain file
  reconfigure from an empty build directory.
- A bare-metal compiler check that fails to link a test program is the symptom the
  `STATIC_LIBRARY` setting avoids.

## Verify
- [ ] A fresh configure with `-DCMAKE_TOOLCHAIN_FILE=<path>` selects the cross compiler.
- [ ] Compile and link command lines carry the same CPU flags.

## Checked
Date: 2026-10-31.
Confirmed in the CMake toolchains manual, the `CMAKE_TRY_COMPILE_TARGET_TYPE` page and the
`target_link_options` page: `CMAKE_SYSTEM_NAME Generic`, `CMAKE_SYSTEM_PROCESSOR`, the
`STATIC_LIBRARY` advice, `CMAKE_FIND_ROOT_PATH_MODE_*` values, the `CMAKE_SOURCE_DIR` caution,
and that `target_link_options` does not apply to static libraries.
Removed as unconfirmed: the `*_INIT` flag advice, `CMAKE_OBJCOPY`/`CMAKE_SIZE`, the CMakePresets
JSON and its version, `LINK_DEPENDS`, hex post-build rules, a board-specific startup and linker script, `-Og` advice,
and the toolchain-file read-count claim.
Method: documentation only; no commands were run.
