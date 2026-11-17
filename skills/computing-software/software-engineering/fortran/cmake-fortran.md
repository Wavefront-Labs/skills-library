---
id: computing-software.software-engineering.fortran.cmake-fortran
name: cmake-fortran
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, cmake-fortran, fortran-build-systems]
level: practitioner
status: draft
description: "Configure CMake with enable Fortran, module directory, and linking libraries, and let CMake compute module dependencies."
sources:
  - https://www.gnu.org/software/make/manual/
  - https://cmake.org/cmake/help/latest/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CMake for Fortran projects
**Goal:** use CMake to build Fortran.
```cmake
cmake_minimum_required(VERSION 3.20)
project(demo LANGUAGES Fortran)
set(CMAKE_Fortran_MODULE_DIRECTORY ${CMAKE_BINARY_DIR}/mod)
add_library(geom src/geometry.f90)
add_executable(app src/main.f90)
target_link_libraries(app PRIVATE geom)
find_package(LAPACK REQUIRED)
target_link_libraries(app PRIVATE LAPACK::LAPACK)
```
- CMake scans Fortran sources and orders module builds automatically (Makefile and Ninja generators).
- Per-target module dir: `set_target_properties(geom PROPERTIES Fortran_MODULE_DIRECTORY ...)`.
- `find_package(BLAS)`, `find_package(OpenMP)`, `find_package(MPI)` provide imported targets.
- Mixed C/Fortran: `FortranCInterface` module checks mangling.
## Gotchas
- Modules from a different target must be in an include path; target-based linking handles it when module dir is set per target.
- Use `-DCMAKE_BUILD_TYPE=Release` so flags apply; set `CMAKE_Fortran_FLAGS` with care.
## Self-check
Configure and build in a fresh build directory; confirm the order is correct with `cmake --build build -j`.
