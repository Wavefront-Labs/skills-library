---
id: computing-software.software-engineering.cpp.coverage-with-gcov-and-llvm-cov
name: coverage-with-gcov-and-llvm-cov
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, gcov, llvm-cov, gcovr, lcov, code-coverage, source-based-coverage, cmake]
level: practitioner
status: docs-checked
description: "Measure C/C++ test coverage with GCC gcov (gcovr, lcov) or Clang source-based coverage (llvm-profdata, llvm-cov), wire it into CMake/CTest, and report in CI."
sources: ["https://gcc.gnu.org/onlinedocs/gcc/Gcov.html", "https://clang.llvm.org/docs/SourceBasedCodeCoverage.html", "https://gcovr.com/en/stable/", "https://llvm.org/docs/CommandGuide/llvm-cov.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coverage with gcov / llvm-cov

**Goal:** know which lines and branches the C/C++ test suite exercises, with reports in CI.

## Option A: GCC + gcov + gcovr
```bash
cmake -S . -B build-cov -G Ninja -DCMAKE_BUILD_TYPE=Debug \
      -DCMAKE_CXX_FLAGS="--coverage -O0 -fno-inline" -DCMAKE_EXE_LINKER_FLAGS="--coverage"
cmake --build build-cov
ctest --test-dir build-cov
gcovr -r . build-cov --exclude 'tests/' --exclude 'build-cov/_deps/' \
      --html-details coverage.html --xml coverage.xml --txt
```
- `--coverage` = `-fprofile-arcs -ftest-coverage`: compile emits `.gcno`, running emits `.gcda`.
- Build without optimisation (`-O0`) so line counts map cleanly to source.
- `.gcda` files accumulate across runs; delete them (`find build-cov -name '*.gcda' -delete` or
  `gcovr --delete`) for a fresh measurement.
- Branch coverage: gcovr `--txt-metric branch`; expect noise from exception paths
  (gcovr `--exclude-throw-branches`, `--exclude-unreachable-branches`).
- For multithreaded programs, `-fprofile-update=atomic` (one of `single`, `atomic`, `prefer-atomic`) makes the counter updates atomic.

## Option B: Clang source-based coverage (more precise)
```bash
clang++ -fprofile-instr-generate -fcoverage-mapping -O0 ... -o tests
LLVM_PROFILE_FILE="cov-%p-%m.profraw" ./tests           # %p pid, %m binary signature
llvm-profdata merge -sparse cov-*.profraw -o cov.profdata
llvm-cov report ./tests -instr-profile=cov.profdata -ignore-filename-regex='(tests|_deps)/'
llvm-cov show   ./tests -instr-profile=cov.profdata -format=html -output-dir=cov-html \
                -show-line-counts-or-regions -show-branches=count
llvm-cov export ./tests -instr-profile=cov.profdata -format=lcov > cov.lcov
```
- Region-level accuracy: sub-line regions, macro expansions and template instantiations can be shown (`-show-line-counts-or-regions`, `--show-expansions`).
- Several test binaries: pass each with `-object=` to report/show.
- MC/DC coverage: add `-fcoverage-mcdc` (and `--show-mcdc` in `llvm-cov show`).

## CMake integration
Add a preset or option:
```cmake
option(ENABLE_COVERAGE "Instrument for coverage" OFF)
if(ENABLE_COVERAGE)
  if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-fprofile-instr-generate -fcoverage-mapping)
    add_link_options(-fprofile-instr-generate)
  else()
    add_compile_options(--coverage -fprofile-update=atomic)
    add_link_options(--coverage)
  endif()
endif()
```
Never ship coverage-instrumented binaries.

## CI
Upload `coverage.xml` (Cobertura, written by gcovr's `--xml`) or an lcov file to your coverage service and gate on patch coverage. Exclude third-party and generated code; mark intentionally untestable lines
with `// GCOVR_EXCL_LINE` (gcovr) sparingly.

## Gotchas
- Use gcov/gcovr for GCC-instrumented builds and llvm-profdata/llvm-cov for Clang source-based builds.
- Header-only templates appear only if instantiated in tests.
- Processes that never exit normally do not write profile data; call `__gcov_dump()` (gcc) or
  `__llvm_profile_write_file()` (clang) at a safe point if needed.

## Verify
- [ ] Coverage report matches expectations for a file with a known untested branch.
- [ ] Third-party code excluded; numbers stable across reruns.
- [ ] CI uploads reports and shows patch coverage on PRs.

## Checked

Date: 2026-10-25. Documentation: Clang Source-based Code Coverage and llvm-cov command guide (llvm/llvm-project, head 2026-10-25), GCC manual gcov.texi and invoke.texi (gcc-mirror/gcc), gcovr source and docs (gcovr/gcovr).

Confirmed: `--coverage` and `.gcno`/`.gcda` files; `-fprofile-update` methods; `__gcov_dump`; `LLVM_PROFILE_FILE` patterns `%p` and `%m`; `llvm-profdata merge -sparse`; llvm-cov `report`/`show`/`export` (lcov or JSON), `-ignore-filename-regex`, `-show-branches=count`, `-show-line-counts-or-regions`, `-output-dir`, repeated `-object`; `-fcoverage-mcdc`; `__llvm_profile_write_file`; gcovr `--html-details`, `--xml`, `--txt-metric`, `--exclude`, `--delete`, `--exclude-throw-branches`, `--exclude-unreachable-branches`, `GCOVR_EXCL_LINE`.
Removed as unconfirmed: lcov command line and `LCOV_EXCL_LINE`, the macOS `xcrun` note, the Clang 18 version gate, the claim that parallel `.gcda` writes merge safely, and statements about optimised builds.

Method: documentation only; no commands were run.
