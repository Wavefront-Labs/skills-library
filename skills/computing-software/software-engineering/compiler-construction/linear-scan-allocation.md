---
id: computing-software.software-engineering.compiler-construction.linear-scan-allocation
name: linear-scan-allocation
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, linear-scan-register, live-intervals, second-chance-binpacking, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Fast allocator"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Linear scan allocation

Goal: allocate quickly.
- Compute live intervals, scan in order, assign free register or spill the interval ending last.
- Used in JITs; SSA-based variants (Wimmer) improve quality.
- Handle holes in intervals.
Verify: compare spill counts against graph colouring on benchmarks.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
