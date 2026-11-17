---
id: computing-software.software-engineering.cpp.threadsanitizer-and-ubsan-checks
name: threadsanitizer-and-ubsan-checks
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-tooling, cpp-tl-tsan-ubsan, threadsanitizer, ubsan, sanitizers, data-race, undefined-behavior, clang]
level: practitioner
status: docs-checked
description: "Run ThreadSanitizer and UBSan on C++ code with Clang: flags, which checks are in the undefined group, trap and recover modes, suppressions and TSan limits."
sources: ["https://clang.llvm.org/docs/ThreadSanitizer.html", "https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ThreadSanitizer and UBSan

## ThreadSanitizer (TSan): data races
```
clang++ -g -fsanitize=thread test.cpp -o test_tsan
TSAN_OPTIONS="halt_on_error=1" ./test_tsan
```
TSan is a compiler instrumentation module plus a run-time library. Fix a reported race by adding a mutex, making the variable `std::atomic`, or restructuring ownership.
- Typical slowdown is about 5x-15x and typical memory overhead about 5x-10x (at default settings 5x plus 1 MB per thread), so run it as its own CI job.
- It generally requires all code compiled with `-fsanitize=thread`. Code that is not (such as pre-compiled dynamic libraries) may hide races or give false positives; see the `ignore_interceptors_accesses` and `ignore_noninstrumented_modules` run-time options.
- `halt_on_error` defaults to false (keep going after the first report). Other options go in `TSAN_OPTIONS` (run an instrumented binary with `help=1` for the list) or in a compiled-in `__tsan_default_options()`.
- Suppress known races you cannot fix (for example in a third-party library) with `TSAN_OPTIONS="suppressions=/path/to/suppressions.supp"`. Each line is `suppression_type:suppression_pattern`; types include `race`, `race_top`, `mutex`, `thread`, `signal`, `deadlock` and `called_from_lib`.
- `no_sanitize("thread")` on a function stops instrumentation of plain loads and stores while still instrumenting to avoid false positives. Ignoring a function through a special case list (`src`, `fun`) leaves it uninstrumented and can cause false positives.
- 64-bit targets are supported; 32-bit support is problematic and not planned. On Linux, disabling ASLR can make TSan fail to map shadow memory (`FATAL: ThreadSanitizer can not mmap the shadow memory`), and GDB disables ASLR by default, so configure GDB to preserve ASLR when debugging a TSan binary.

## UndefinedBehaviorSanitizer (UBSan)
```
clang++ -g -fsanitize=undefined test.cpp                      # link with clang++, not ld
clang++ -fsanitize=undefined -fno-sanitize-recover=undefined test.cpp   # print a report and exit on first hit
clang++ -fsanitize=undefined,float-divide-by-zero,implicit-conversion,vptr ...
UBSAN_OPTIONS=print_stacktrace=1 ./a.out
```
- `-fsanitize=undefined` is every check except `float-divide-by-zero`, `unsigned-integer-overflow`, `implicit-conversion`, `local-bounds`, `vptr` and the `nullability-*` group: enable those by name when you want them.
- Individual checks include `signed-integer-overflow`, `shift`, `null`, `alignment`, `bounds` (indexing where the array bound is statically known), `return` (C++: reaching the end of a value-returning function), `unreachable`, `bool`, `enum` and `float-cast-overflow`.
- `-fno-sanitize-recover=...` prints a verbose report and exits; `-fsanitize-trap=...` executes a trap instruction and needs no UBSan run-time library (the program typically ends with SIGILL or SIGTRAP). `-fsanitize-trap=all` puts every check in trap mode.
- The UBSan run-time is meant for testing; for security-sensitive builds the page suggests the minimal runtime (`-fsanitize-minimal-runtime`) or trap mode.

## Gotchas
- `-fsanitize=vptr` is incompatible with `-fno-rtti`, must be linked by `clang++`, and does not support `-fsanitize-trap=vptr`.
- `-fsanitize=float-divide-by-zero` is excluded from `undefined` because Clang defines the result (infinity or NaN).
- `-fno-sanitize=alignment` after `-fsanitize=undefined` removes one check from the group.

## Verify
- [ ] A seeded race (two threads incrementing a plain int) is reported by the TSan job.
- [ ] A seeded signed overflow and a missing return are reported by the UBSan job, which fails on any report.

## Checked
2026-11-09. Confirmed on the Clang ThreadSanitizer page (slowdown and memory figures, all-code-instrumented requirement and the two run-time options, halt_on_error default, suppressions file format and types, no_sanitize("thread"), special case list, 64-bit and 32-bit support, ASLR shadow-memory failure and GDB note) and the Clang UndefinedBehaviorSanitizer page (contents of the undefined group, check descriptions, no-sanitize-recover and trap flags, print_stacktrace, test-only runtime and minimal runtime advice, vptr and float-divide-by-zero notes). Removed as not on those pages: second_deadlock_stack, lock-order inversion claim, the claim that TSan cannot combine with ASan/MSan, __tsan_acquire/release, the setarch and vm.mmap_rnd_bits advice (the page says disabling ASLR is what breaks TSan), GCC invocation, the 20-50% UBSan cost, standard library hardening macros and the claim that vptr is part of -fsanitize=undefined (it is not).
Method: documentation only; no commands were run.
