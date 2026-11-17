---
id: computing-software.software-engineering.objective-c.address-sanitizer
name: address-sanitizer
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-memory-tools, address-sanitizer]
level: practitioner
status: docs-checked
description: "Build with -fsanitize=address, thread and undefined to catch memory errors, data races and UB in Objective-C code."
sources:
  - https://clang.llvm.org/docs/
  - https://developer.apple.com/documentation/xcode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# AddressSanitizer
**Goal:** detect memory bugs at test time.

```bash
clang -fsanitize=address -g -O1 -fno-omit-frame-pointer main.m -o app_asan
ASAN_OPTIONS=detect_leaks=1 ./app_asan
```
- Build and link with `-fsanitize=address`; add `-g` for symbols and `-fno-omit-frame-pointer` for readable stacks.
- LeakSanitizer is enabled with `ASAN_OPTIONS=detect_leaks=1` on macOS.
- Suppressions and ignore lists are covered on the page; read it before relying on a flag.

## Self-check
Write an out-of-bounds read on a malloc'd buffer and confirm AddressSanitizer reports it.

## Checked
2026-11-02. Confirmed against the Clang AddressSanitizer page: `-fsanitize=address`, recommended `-fno-omit-frame-pointer`, `ASAN_OPTIONS=detect_leaks=1` on macOS. Removed: ThreadSanitizer/UBSan/Main Thread Checker claims and combinations, Xcode scheme paths, slowdown ratios, `-fsanitize-ignorelist` spelling and the Linux leak claim (not stated for those pages read).
Method: documentation only; no commands were run.
