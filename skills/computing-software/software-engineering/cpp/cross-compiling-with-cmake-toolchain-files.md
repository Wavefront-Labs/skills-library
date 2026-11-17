---
id: computing-software.software-engineering.cpp.cross-compiling-with-cmake-toolchain-files
name: cross-compiling-with-cmake-toolchain-files
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cmake, cpp-build, toolchain-file, cpp-cross-compiling, sysroot, embedded, cpp-toolchains]
level: practitioner
status: docs-checked
description: "Cross-compile C++ with CMake toolchain files: compilers, sysroot and find root path modes, running tests via emulators, and vcpkg/Conan integration."
sources:
  - https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html
  - https://cmake.org/cmake/help/latest/variable/CMAKE_FIND_ROOT_PATH_MODE_PROGRAM.html
  - https://cmake.org/cmake/help/latest/variable/CMAKE_CROSSCOMPILING_EMULATOR.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cross-compiling with CMake toolchain files

**Goal:** build for another architecture or OS (ARM Linux boards, embedded, Windows from Linux) with libraries found in the target sysroot, not the host.

## 1. A toolchain file
```cmake
# cmake/toolchains/aarch64-linux-gnu.cmake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

set(CMAKE_C_COMPILER   aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)

set(CMAKE_SYSROOT /opt/sysroots/aarch64)
set(CMAKE_FIND_ROOT_PATH ${CMAKE_SYSROOT})
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)    # build tools come from the host
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)     # libraries only from the target
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

set(CMAKE_CROSSCOMPILING_EMULATOR qemu-aarch64;-L;${CMAKE_SYSROOT})   # lets ctest run target binaries
```
```bash
cmake -S . -B build-arm64 -G Ninja --toolchain cmake/toolchains/aarch64-linux-gnu.cmake
cmake --build build-arm64 && ctest --test-dir build-arm64
```
Setting `CMAKE_SYSTEM_NAME` in the toolchain file is what enables cross-compiling; CMake then sets `CMAKE_CROSSCOMPILING` (the emulator variable is only used when it is on).

## 2. Clang as a cross compiler
```cmake
set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_COMPILER clang++)
set(CMAKE_C_COMPILER_TARGET aarch64-linux-gnu)
set(CMAKE_CXX_COMPILER_TARGET aarch64-linux-gnu)
set(CMAKE_LINKER_TYPE LLD)    # CMake 3.29+
```
One clang install targets many architectures; you still need the target sysroot (headers/libs).

## 3. Bare-metal / embedded
```cmake
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)
set(CMAKE_C_COMPILER arm-none-eabi-gcc)
set(CMAKE_CXX_COMPILER arm-none-eabi-g++)
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)   # compiler checks cannot link without startup files
set(CMAKE_CXX_FLAGS_INIT "-mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16")
```

## 4. Host tools during a cross build
Code generators built and run during the build must be compiled for the host: build them in a separate host build and import them (`find_program`/an exported targets file), or use `ExternalProject` for a host sub-build.

## 5. With package managers
- vcpkg: pick a triplet for the target and chain your own toolchain file through the vcpkg triplet's chainload setting (see the vcpkg triplet documentation).
- Conan: use a host profile and a build profile (`conan install . -pr:h=<host-profile> -pr:b=<build-profile>`).

## Gotchas
- Mixing host and target libraries produces "file in wrong format" link errors; check `FIND_ROOT_PATH_MODE` and sysroot.
- Set toolchain variables in the toolchain file, not in CMakeLists.txt; CMake loads the file early to set the compilers.

## Verify
- `file build-arm64/app` reports the target architecture, the binary runs under QEMU or on the device, and `ctest` passes via the emulator.

## Checked

Date: 2026-10-25. Documentation: CMake cmake-toolchains(7) and variable pages (Kitware/CMake, head 2026-10-25).

Confirmed: `--toolchain` and `CMAKE_TOOLCHAIN_FILE` load the file early; `CMAKE_SYSTEM_NAME` enables cross-compiling and `Generic` is for bare metal; `CMAKE_CROSSCOMPILING_EMULATOR` (3.3, list form 3.15, used only when cross-compiling); `CMAKE_<LANG>_COMPILER_TARGET`; `CMAKE_LINKER_TYPE` (3.29); `CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY` for bare-metal; the `CMAKE_FIND_ROOT_PATH_MODE_*` variables.
Removed as unconfirmed: the vcpkg triplet and chainload variable names, the exact Conan profile example, and the try_run note.

Method: documentation only; no commands were run.
