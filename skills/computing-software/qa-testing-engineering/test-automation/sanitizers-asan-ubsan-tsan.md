---
id: computing-software.qa-testing-engineering.test-automation.sanitizers-asan-ubsan-tsan
name: sanitizers-asan-ubsan-tsan
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [addresssanitizer, sanitizers, dynamic-analysis, ubsan, threadsanitizer, leaksanitizer, wild-pointers, clang, gcc]
level: practitioner
status: docs-checked
description: "Run unit and integration tests under AddressSanitizer, UBSan and ThreadSanitizer to catch buffer overflows, use-after-free, undefined behaviour and data races."
sources:
  - https://clang.llvm.org/docs/AddressSanitizer.html
  - https://clang.llvm.org/docs/ThreadSanitizer.html
  - https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sanitizers in test runs (ASan, UBSan, TSan)

**Goal:** turn silent memory and concurrency bugs (wild pointers, races) into loud test failures.

## Build flags (Clang)
```bash
# AddressSanitizer: add -O1 or higher for reasonable speed, frame pointers for good stacks
CFLAGS="-fsanitize=address -fno-omit-frame-pointer -g -O1"
# UndefinedBehaviorSanitizer (link with clang++ for C++ so the runtime is present)
CFLAGS="-fsanitize=undefined"
# ThreadSanitizer: its own build
CFLAGS="-fsanitize=thread -g -O1"
```
Put each in a dedicated CI build or preset. Check the compiler docs for combining sanitizers and for GCC,
Rust and Go equivalents; this skill does not cover them.

## Runtime options
Set per-sanitizer environment variables: `ASAN_OPTIONS` (for example `detect_leaks=1`; LeakSanitizer is
supported on some platforms only, so check the ASan page for yours), `UBSAN_OPTIONS` (for example
`print_stacktrace=1`) and `TSAN_OPTIONS` (for example `halt_on_error=1`, default false, exits after the first
reported error). Separate options with a colon or space as the docs show.

## What each catches
- **ASan**: heap, stack and global buffer overflow, use-after-free, double-free and invalid free,
  use-after-return (runtime mode by default; `ASAN_OPTIONS=detect_stack_use_after_return=0` disables it), and
  leaks via LeakSanitizer.
- **UBSan** (`-fsanitize=undefined`): signed integer overflow, null or misaligned pointer use, out-of-bounds
  shifts, bounds checks where the array bound is statically known (`-fsanitize=bounds`). Not in the
  `undefined` group: float-divide-by-zero, unsigned-integer-overflow, vptr and `local-bounds`; enable those
  explicitly. Unsigned overflow is not undefined behaviour but often unintentional.
- **TSan**: data races; deadlock detection is on by default (`detect_deadlocks`).

## CI
Separate jobs for ASan/UBSan and for TSan; run unit, integration and fuzz targets. Documented cost: ASan
typical slowdown 2x; TSan typical slowdown about 5x-15x and memory overhead about 5x-10x.

## Gotchas
- Code not built with the sanitizer is not instrumented; use suppression files sparingly and comment each entry.
- TSan only sees races that the tests actually execute concurrently; stress the concurrent paths.

## Verify
Seed a known off-by-one in a branch: the ASan job fails with a heap-buffer-overflow report pointing to the line.

## Checked
2026-11-01. Confirmed in the Clang AddressSanitizer, ThreadSanitizer and UndefinedBehaviorSanitizer pages:
flags, option variables, what each tool detects, UBSan group membership, slowdown and memory figures, TSan
`halt_on_error` and `detect_deadlocks`. Removed: the CTAL-TTA syllabus reference, the combined
`address,undefined` flag line and ASan/TSan incompatibility statement, CMake/Rust/Go/GCC recipes,
`abort_on_error` and `second_deadlock_stack`, and the false-positive/negative remark on third-party libraries,
none of which those pages state.
Method: documentation only; no commands were run.
