---
id: computing-software.game-programming.game-engine-architecture.data-race-detection-with-threadsanitizer
name: data-race-detection-with-threadsanitizer
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, thread-sanitizer, data-race, multithreading, game-programming]
level: practitioner
status: draft
description: "Find data races in engine code with ThreadSanitizer: build flags, reading reports, annotating lock-free code and job systems, suppressions and CI use."
sources: ["https://clang.llvm.org/docs/ThreadSanitizer.html", "https://github.com/google/sanitizers/wiki/ThreadSanitizerCppManual"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data race detection with ThreadSanitizer

**Goal:** catch races in job systems, streaming and render threads before they become one-in-a-
thousand crashes.

## Build
```bash
clang++ -fsanitize=thread -g -O1 -fno-omit-frame-pointer ...     # also link with -fsanitize=thread
TSAN_OPTIONS="halt_on_error=0 history_size=7 second_deadlock_stack=1" ./game --headless --bench
```
- Supported with Clang/GCC on Linux and macOS (x86-64, ARM64); MSVC has no TSan, so run a Linux
  headless build of engine/game code in CI.
- 5-15x slowdown and 5-10x memory; use headless tests and small scenes.
- Every linked library ideally built with TSan; uninstrumented code can hide races or cause false
  positives.

## Reading reports
`WARNING: ThreadSanitizer: data race` lists two accesses (write/read) with stacks and the threads'
creation stacks. Fix by making the shared access atomic, protecting it with a mutex, or restructuring
so ownership is exclusive (double buffering, per-thread copies).

## Custom synchronisation
TSan understands `std::atomic`, `std::mutex`, pthreads. Custom primitives (spinlocks with inline asm,
fiber switches, lock-free queues with fences) need annotations:
- Fibers: `__tsan_create_fiber`, `__tsan_switch_to_fiber`, `__tsan_destroy_fiber`.
- Happens-before: `__tsan_acquire(addr)` / `__tsan_release(addr)` around custom handoffs.
- Job systems built on std atomics with acquire/release generally work unmodified.

## Suppressions
`TSAN_OPTIONS=suppressions=tsan.supp` with lines like `race:ThirdPartyLib::*` for known benign
races in code you can't fix. Never suppress your own "benign" races; they are undefined behaviour.

## CI
Nightly TSan run of the job system tests, streaming tests and a bot match. Track new reports as bugs.

## Verify
- Seed a known race (unsynchronised counter in a parallel-for) and confirm TSan reports it.
