---
id: computing-software.software-engineering.cpp.lto-and-pgo-optimization
name: lto-and-pgo-optimization
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-toolchains, cpp-tc-lto, lto-pgo, link-time-optimization, profile-guided-optimization, thinlto, fprofile-use]
level: advanced
status: docs-checked
description: "Enable link-time and profile-guided optimisation for C++ with Clang (ThinLTO, instrumented PGO, llvm-profdata) and CMake IPO."
sources:
  - https://clang.llvm.org/docs/UsersManual.html
  - https://clang.llvm.org/docs/ThinLTO.html
  - https://cmake.org/cmake/help/latest/module/CheckIPOSupported.html
  - https://cmake.org/cmake/help/latest/prop_tgt/INTERPROCEDURAL_OPTIMIZATION.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LTO and PGO (Clang and CMake)

## LTO
Interprocedural optimisation works across translation units; at link time it is called LTO, enabling more inlining and dead-code elimination.
```
clang -flto=thin -O2 file1.c file2.c -c
clang -flto=thin -O2 file1.o file2.o -o a.out
```
- `-flto` alone is full LTO. ThinLTO (`-flto=thin`) is scalable and incremental: it avoids merging all inputs into one module and runs optimisation in parallel backends.
- With `lld-link`, `-flto=thin` is needed only at compile time.
- ThinLTO supports incremental builds through a cache (linker option, for example `/lldltocache:` for lld-link).
- Parallelism of the backend is a linker option (for example `/opt:lldltojobs=N` for lld-link); the default uses the hardware thread count.

CMake:
```cmake
include(CheckIPOSupported)
check_ipo_supported(RESULT ok OUTPUT why)
if(ok)
  set_property(TARGET app PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
else()
  message(WARNING "IPO is not supported: ${why}")
endif()
```
- `check_ipo_supported` (3.9+) needs policy `CMP0069` set to `NEW`, or it is a fatal error. Without `RESULT` it is a fatal error when IPO is unsupported.
- `INTERPROCEDURAL_OPTIMIZATION` is initialised from `CMAKE_INTERPROCEDURAL_OPTIMIZATION`; a per-config `INTERPROCEDURAL_OPTIMIZATION_<CONFIG>` overrides it when set. Enabling it on an unsupported compiler is reported or ignored depending on `CMP0069`.

## PGO with instrumentation (Clang)
```
clang++ -O2 -fprofile-generate code.cc -o code           # IR-based; -fprofile-instr-generate is frontend-based
LLVM_PROFILE_FILE="code-%p.profraw" ./code               # run with typical inputs
llvm-profdata merge -output=code.profdata code-*.profraw
clang++ -O2 -fprofile-use=code.profdata code.cc -o code
```
- The docs recommend IR-based instrumentation (`-fprofile-generate`) for best PGO performance: lower overhead and smaller profiles. Frontend-based has better source correlation, for coverage.
- Raw profiles go to `default.profraw` unless `LLVM_PROFILE_FILE` (which wins over the command-line option) or `-fprofile-instr-generate=` says otherwise. `%p` expands to the process ID; `%h` to the hostname; `%m` merges raw profiles from processes automatically and cuts storage.
- Merging with `llvm-profdata merge` is required even for one raw profile, because it also converts the format.
- Code changes can make a profile unusable; clang warns when that happens.
- Instrument and profile with inputs that reflect typical usage.

## Verify
- [ ] Benchmark the optimised build against a plain `-O2` build on a realistic workload.
- [ ] The test suite passes on the LTO/PGO binary.

## Checked
Method: docs-checked 2026-11-09 against the Clang Users Manual (PGO section), Clang ThinLTO page and the CMake CheckIPOSupported and INTERPROCEDURAL_OPTIMIZATION pages. Dropped GCC and MSVC flags (GCC manual not read), speed-up percentages, AutoFDO and ODR-warning advice as unconfirmed.
