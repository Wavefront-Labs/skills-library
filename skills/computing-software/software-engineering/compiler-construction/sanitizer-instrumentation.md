---
id: computing-software.software-engineering.compiler-construction.sanitizer-instrumentation
name: sanitizer-instrumentation
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, addresssanitizer, undefined-behaviour-sanitizer, shadow-memory, compilers, interpreters, language-implementation]
level: practitioner
status: docs-checked
description: "Runtime checking"
sources:
  - https://clang.llvm.org/docs/AddressSanitizer.html
  - https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html
  - https://clang.llvm.org/docs/ThreadSanitizer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sanitizer instrumentation

Goal: understand compiler-inserted checks.
- ASan (`-fsanitize=address`) is a compiler instrumentation module plus a run-time library; it detects out-of-bounds accesses to heap, stack and globals, use-after-free, use-after-scope, double-free and invalid free. Typical slowdown is 2x.
- UBSan (`-fsanitize=undefined`) inserts checks such as `signed-integer-overflow`, `null` and `alignment`; most checks print a report and continue, and `-fno-sanitize-recover` or `-fsanitize-trap` change that. The `undefined` group excludes `unsigned-integer-overflow` and `vptr`.
- TSan (`-fsanitize=thread`) detects data races with instrumentation plus a run-time library; typical slowdown is about 5x-15x and memory overhead about 5x-10x. Build with `-O1` or higher and `-g`.
Verify: a seeded bug is caught with a readable report.

## Checked
2026-11-08. Confirmed in the Clang AddressSanitizer, UndefinedBehaviorSanitizer and ThreadSanitizer pages: bug classes, slowdown and memory figures, check names, group membership, recover and trap options, TSan build advice. Removed: the shadow-memory and happens-before descriptions, the generic 2-10x slowdown, and the run-in-CI advice.
Method: documentation only; no commands were run.
