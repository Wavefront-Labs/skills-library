---
id: computing-software.software-engineering.objective-c.libobjc2-runtime
name: libobjc2-runtime
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-ops, libobjc2-runtime]
level: sme
status: docs-checked
description: "Select the GNUstep runtime ABI with clang -fobjc-runtime flags, link libobjc2 and know feature differences from Apple's runtime."
sources:
  - https://raw.githubusercontent.com/gnustep/libobjc2/master/README.md
  - https://clang.llvm.org/docs/ClangCommandLineReference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# libobjc2
**Goal:** use modern Objective-C features off Apple platforms.

```bash
clang -fobjc-runtime=gnustep-2.0 -fobjc-arc main.m -o hello   # plus libobjc2 and your GNUstep libraries at link time
```
- libobjc2 is the GNUstep Objective-C runtime, designed as a drop-in replacement for the GCC runtime. It supports three ABIs, chosen with `-fobjc-runtime=`: `gcc` (old GCC ABI, Objective-C 1.0 features; also by compiling with GCC), `gnustep-1.9` (initial non-fragile ABI) and `gnustep-2.0` (modern v2 ABI with richer reflection metadata, smaller binaries and lower memory use; needs Clang 7.0 or later). `-fobjc-runtime=<arg>` is documented by clang as "Specify the target Objective-C runtime kind and version".
- Match the ABI to the runtime installed: the runtime can be built without older-ABI support (CMake `OLDABI_COMPAT=OFF`), and the result will not link against code built for the older ABIs.
- All ABIs add, beyond the GCC runtime: the modern runtime APIs introduced with OS X 10.5, blocks, synthesised property accessors, efficient `@synchronized()`, type-dependent dispatch (when compiled in), the associated reference APIs from Mac OS X 10.6 and the ARC APIs from Mac OS X 10.7.
- Type-dependent dispatch: when enabled, a message sent with a typed selector only invokes a method with the same types, avoiding stack corruption from mismatched signatures; an untyped selector matches by name. A mismatch calls a handler that by default prints a message and exits.
- The runtime is MIT licensed.
- The library supports Linux, Windows and FreeBSD (CI badges on the README).
- Check the installed version against the README and the headers it ships; the exact ABI the toolchain targets must be the one libobjc2 was built for.

## Gotchas
- Mixing code built for different ABIs in one program can fail at link or load time.
- Do not assume every Cocoa class or Apple framework is available on GNUstep; check its documentation before depending on one.

## Self-check
Compile the same wrapper on macOS and under GNUstep CI and compare test results.

## Checked

2026-11-08. Confirmed against the libobjc2 README (ABIs, flags, Clang 7.0, OLDABI_COMPAT, feature list, type-dependent dispatch, MIT licence, CI platforms) and the Clang command line reference (`-fobjc-runtime=`). Removed the `gnustep-1.8` value, `gnustep-config` flags, claims about weak references and tagged pointers, Swift on Linux, `NSURLSession` and `os_log` availability, and the `#if GNUSTEP` idiom, which no readable page states.
Method: documentation only; no commands were run.
