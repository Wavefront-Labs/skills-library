---
id: computing-software.software-engineering.d.d-betterc-subset-and-switch
name: d-betterc-subset-and-switch
category: computing-software
field: software-engineering
product: d
tags: [d-betterc-subset-and-switch, betterc, -betterc, d_betterc, no-runtime, freestanding, extern-c-main, subset, d]
level: advanced
status: docs-checked
description: "Compile D as a runtime-free C-like subset with -betterC (D_BetterC): supported features, missing ones (GC, classes, exceptions, TypeInfo), and extern(C) main."
sources:
  - https://dlang.org/spec/betterc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# -betterC: what is available and unavailable

Goal: use D without druntime.

- `dmd -betterC app.d` (dub: `dflags "-betterC"` or the `"betterC"` build option); `version (D_BetterC)` is defined. Entry: a C `main()`, e.g. `extern(C) void main()` as in the spec.
- Available: compile-time features and full metaprogramming, nested functions, delegates and lambdas, member functions, constructors, destructors, operator overloading, array slicing with bounds checking, RAII, `scope(exit)`, memory safety protections, COM and C++ classes, `switch` with strings, `final switch`, and `unittest` (run via `__traits(getUnitTests, ...)`). `assert` failures go to the C runtime.
- Unavailable: garbage collection, `TypeInfo` and `ModuleInfo`, classes, built-in threading (`core.thread`), dynamic arrays (slices of static arrays and pointers work), associative arrays, exceptions, `synchronized` and `core.sync`, static module constructors/destructors.
- Use C library calls: `import core.stdc.stdio; printf("%d\n", x);` or link libc.
- Druntime and Phobos were not written for BetterC: determine which symbols you may use and expect cryptic compiler or linker errors.

Gotchas:
- Linking D into C programs works when only the C runtime library is required, which is what BetterC restricts you to.

Verify: `dmd -betterC hello.d && ./hello` prints the greeting.

## Checked

Date 2026-11-02. Confirmed the Better C spec page: the -betterC switch, D_BetterC version, available and unavailable feature lists. Errors fixed: entry is extern(C) void main() in the spec; classes, dynamic arrays, AAs and exceptions are unavailable; unittest and string switch are available. Removed -nodefaultlibs and nm claims.

Method: documentation only; no commands were run.
