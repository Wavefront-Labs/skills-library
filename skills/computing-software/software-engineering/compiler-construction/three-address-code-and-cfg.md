---
id: computing-software.software-engineering.compiler-construction.three-address-code-and-cfg
name: three-address-code-and-cfg
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, basic-blocks, three-address-code-gen, cfg-construction, three-address-code, ssa-form, control-flow-graph, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Lowering"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Three-address code and CFGs

Goal: lower an AST to IR.
- Emit instructions like `t1 = a + b`; split into basic blocks (leaders at jumps/targets), build the CFG.
- Short-circuit and loops become conditional branches.
- Keep an IR printer for debugging.
Verify: CFG dump for a loop looks as expected.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
