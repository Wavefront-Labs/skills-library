---
id: computing-software.software-engineering.compiler-construction.instruction-selection
name: instruction-selection
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, tree-pattern-matching, burs, isel-dag, instruction-selection, calling-convention, assembly-emission, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Mapping IR to machine ops"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Instruction selection

Goal: map IR to instructions.
- Tree/DAG pattern matching with cost (BURG), or macro expansion with peephole cleanup.
- Use addressing modes and fused instructions (LEA, FMA).
- LLVM uses SelectionDAG/GlobalISel.
Verify: generated assembly for sample expressions is compact and correct.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
