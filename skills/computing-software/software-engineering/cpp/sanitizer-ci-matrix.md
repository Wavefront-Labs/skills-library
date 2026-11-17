---
id: computing-software.software-engineering.cpp.sanitizer-ci-matrix
name: sanitizer-ci-matrix
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-tooling, cpp-tl-sanitizer-ci, sanitizer-ci-matrix, github-actions, cmake-presets, asan, tsan, ubsan, msan]
level: practitioner
status: docs-checked
description: "Set up a CI matrix running C++ tests under ASan, UBSan, TSan and MSan with Clang flags, runtime options and limits, CMake presets and GitHub matrix jobs."
sources: ["https://clang.llvm.org/docs/AddressSanitizer.html", "https://clang.llvm.org/docs/ThreadSanitizer.html", "https://clang.llvm.org/docs/MemorySanitizer.html", "https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html", "https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html", "https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sanitizer CI matrix

One job per sanitizer family plus a plain build. Build flags (from each Clang page):

| Job | Compile and link | Runtime options |
|---|---|---|
| asan | `-fsanitize=address -O1 -g -fno-omit-frame-pointer` | `ASAN_OPTIONS` (colon-separated, e.g. `detect_stack_use_after_return=1`, `detect_leaks=1`, `suppressions=MyASan.supp`) |
| ubsan | `-fsanitize=undefined` | `UBSAN_OPTIONS` |
| tsan | `-fsanitize=thread -g -O1` | `TSAN_OPTIONS` (e.g. `halt_on_error=1`, `suppressions=...`) |
| msan (Clang) | `-fsanitize=memory -fno-omit-frame-pointer -g`, optional `-fsanitize-memory-track-origins` | `MSAN_OPTIONS` |
| plain | release flags | none |

Facts that shape the matrix:
- ASan: `-O1` or higher for reasonable performance and `-fno-omit-frame-pointer` for nicer stack traces. Use-after-return detection is on by default on Linux (`-fsanitize-address-use-after-return=runtime`). Runtime flags in `ASAN_OPTIONS` take precedence over compiled-in defaults. LSan and UBSan flags belong in `LSAN_OPTIONS`/`UBSAN_OPTIONS` rather than `ASAN_OPTIONS`. LeakSanitizer is enabled by default in ASan on Linux and via `ASAN_OPTIONS=detect_leaks=1` on macOS.
- UBSan: by default it prints a diagnostic and continues. `-fno-sanitize-recover=...` prints a verbose report and exits; `-fsanitize-trap=...` executes a trap instruction instead (no runtime needed). `-fno-sanitize=alignment` turns off an individual check.
- TSan: `-fsanitize=thread` makes Clang act as though `-fPIE`/`-pie` were given if you do not use `-fPIC`. Static linking of libc/libstdc++ is not supported. All code should be compiled with the flag, otherwise races may be missed or false positives reported. Deadlock detection is on by default (`detect_deadlocks`); `halt_on_error` defaults to false. On Linux, disabling ASLR can make TSan fail with `FATAL: ThreadSanitizer can not mmap the shadow memory`; GDB disables ASLR by default, so debug with `gdb -ex 'set disable-randomization off' --args ./a.out`. The page lists C++11 threading as supported with libc++ and calls TSan beta.
- MSan: all program code including libraries (even libc) must be instrumented or false reports may result; the runtime has 70+ interceptors for common libc functions, and the authors bootstrapped Clang with a self-built instrumented libc++. Supported on Linux, NetBSD and FreeBSD. Uses 2x real memory (3x with origin tracking); static linking is not supported.
- None of these runtimes are meant to be linked into production executables.

## CMake presets
`CMakePresets.json` has `configurePresets`, `buildPresets` and `testPresets`; each preset has a `name` used by `cmake --preset`, optional `cacheVariables`, and may `inherit` from a `hidden` base preset (hidden presets cannot be selected with `--preset`). Define one configure preset per sanitizer so developers and CI run the same thing locally and remotely.

## GitHub Actions matrix
`jobs.<job_id>.strategy.matrix` defines variables with arrays of values and creates one job per combination; `include` adds or extends combinations, `exclude` removes them. Control failure handling with `strategy.fail-fast` (if a job fails, in-progress and queued jobs are cancelled when true) and `continue-on-error`.
```yaml
jobs:
  sanitize:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        preset: [asan, ubsan, tsan]
    steps:
      - uses: actions/checkout@v4
      - run: cmake --preset ${{ matrix.preset }}
      - run: cmake --build --preset ${{ matrix.preset }}
      - run: ctest --preset ${{ matrix.preset }} --output-on-failure
```

## Verify
- Seeded bugs (heap overflow, data race, uninitialised read) each turn exactly the matching job red.

## Checked
Read the Clang AddressSanitizer, ThreadSanitizer, MemorySanitizer and UndefinedBehaviorSanitizer pages, the CMake presets manual and the GitHub Actions matrix page. Removed as unconfirmed: that ASan and UBSan can be combined while TSan and MSan cannot, `second_deadlock_stack`, the `vm.mmap_rnd_bits` sysctl workaround, `ctest --repeat until-fail`, pinned action and compiler versions, vcpkg/Conan sanitizer triplets, sanitizer slowdown factors and the CMake option snippet.
Method: docs-checked 2026-11-09 against the Clang ASan, TSan, MSan and UBSan pages, the CMake presets manual and the GitHub Actions matrix docs.
