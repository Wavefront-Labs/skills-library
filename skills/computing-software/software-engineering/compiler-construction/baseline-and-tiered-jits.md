---
id: computing-software.software-engineering.compiler-construction.baseline-and-tiered-jits
name: baseline-and-tiered-jits
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, baseline-jit, tiering, on-stack-replacement, jit-compiler, tiered-compilation, tracing-jit, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Staged compilation"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Baseline and tiered JITs

Goal: design a JIT pipeline.
- Tier 0 interpreter collects profile; tier 1 baseline JIT; tier 2 optimising JIT with speculation; deoptimise when guards fail; OSR moves running loops between tiers.
- Hot thresholds counters at function/loop heads.
- Keep deopt metadata.
Verify: benchmark warm-up curve shows tier transitions.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
