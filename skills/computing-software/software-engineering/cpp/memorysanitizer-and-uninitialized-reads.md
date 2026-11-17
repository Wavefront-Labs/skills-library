---
id: computing-software.software-engineering.cpp.memorysanitizer-and-uninitialized-reads
name: memorysanitizer-and-uninitialized-reads
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, msan, memorysanitizer, uninitialized-memory, clang, instrumented-libcxx, valgrind, trivial-auto-var-init]
level: advanced
status: docs-checked
description: "Find uninitialised memory reads in C/C++ with MemorySanitizer: Clang flags, origin tracking, the instrumented-libc++ requirement, false positives, and -ftrivial-auto-var-init."
sources: ["https://clang.llvm.org/docs/MemorySanitizer.html", "https://clang.llvm.org/docs/SanitizerSpecialCaseList.html", "https://clang.llvm.org/docs/UsersManual.html", "https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html", "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MemorySanitizer and uninitialised reads

**Goal:** detect branches, syscalls and outputs that depend on uninitialised memory - a class of
bug ASan does not catch and that causes heisenbugs and information leaks.

## What MSan reports
Use of uninitialised values when they **matter**: conditional branches, pointer dereferences,
syscall arguments, returning to uninstrumented code. Merely copying uninitialised bytes is not
reported (it tracks "shadow" bits through copies and arithmetic).

## Build (Clang; Linux, NetBSD and FreeBSD)
```bash
clang++ -fsanitize=memory -fsanitize-memory-track-origins=2 -fno-omit-frame-pointer \
        -g -O1 app.cpp -o app
./app
```
```
WARNING: MemorySanitizer: use-of-uninitialized-value
    #0 in parse_header src/parse.cpp:42
  Uninitialized value was created by an allocation of 'hdr' in the stack frame of function 'read_packet'
```
- `-fsanitize-memory-track-origins=2` tells you where the uninitialised memory came from (it adds roughly
  1.5x-2x on top of MSan's usual 3x slowdown; `=1` records only allocation points and is a little faster).
- Use a separate build and CI job for MSan (it is its own sanitizer runtime).
- CMake: add a `msan` preset with `CMAKE_CXX_FLAGS="-fsanitize=memory -fsanitize-memory-track-origins=2 -fno-omit-frame-pointer"` and matching linker flags.

## The big requirement: instrument everything
MSan needs **all** code that touches memory to be instrumented, including the C++ standard library
and third-party libraries. Uninstrumented code writes memory MSan cannot see, producing false
positives. libc is intercepted, but libstdc++ is not instrumented:
- Replace libstdc++ with a self-built, MSan-instrumented libc++ (see "Handling external code" in the Clang
  MemorySanitizer page for the steps).
- Build dependencies from source with the same flags.
- Replace inline assembly that writes memory, or code MSan cannot see, as the same page describes.

## Suppressing and controlling
- `__attribute__((no_sanitize("memory")))` on a function (MSan may still instrument it to avoid false positives);
  `-fsanitize-ignorelist=<file>` for a special case list.
- Use-after-destruction detection is on by default; disable it with `-fno-sanitize-memory-use-after-dtor` or
  `MSAN_OPTIONS=poison_in_dtor=0`.

## Alternatives and mitigations
- **Prevention**: `-ftrivial-auto-var-init=zero` (GCC and Clang) zero-initialises automatic variables to
  prevent uninitialised memory disclosure; `=pattern` fills them with a recognisable pattern. GCC still
  reports `-Wuninitialized` for such variables. Initialising memory hides bugs from MSan, so keep it out of MSan builds.
- Compiler warnings: `-Wuninitialized` and `-Wmaybe-uninitialized` (GCC); always initialise at declaration (Core Guidelines ES.20).

## Verify
- [ ] MSan job builds with an instrumented libc++ and runs the test suite cleanly.
- [ ] Each report fixed by initialising at the source the origin trace identifies.
- [ ] Release builds use `-ftrivial-auto-var-init=zero` if policy allows.

## Checked

Date: 2026-10-25. Documentation: Clang MemorySanitizer page (llvm/llvm-project clang/docs/MemorySanitizer.md, head 2026-10-25), Clang UsersManual and SanitizerSpecialCaseList, GCC manual invoke.texi, C++ Core Guidelines (isocpp/CppCoreGuidelines).

Confirmed: supported OS list (Linux, NetBSD, FreeBSD); `-fsanitize=memory`, `-fsanitize-memory-track-origins` (=1, =2) and its cost; 3x typical slowdown; all code including libraries must be instrumented and libc++ is the recommended replacement for libstdc++; `no_sanitize("memory")`; `-fsanitize-ignorelist`; use-after-destruction default and its switches; `-ftrivial-auto-var-init` zero and pattern; GCC `-Wuninitialized` and `-Wmaybe-uninitialized`; Core Guidelines ES.20.
Removed as unconfirmed: architecture list, the ASan/TSan combination rule, the `LLVM_USE_SANITIZER` recipe and linker flags, MSan interface function names, `halt_on_error`, Valgrind slowdown figures, GCC 12 gate, the Clang `-Wconditional-uninitialized` warning, the clang-tidy init check and the OSS-Fuzz MSan remark.

Method: documentation only; no commands were run.
