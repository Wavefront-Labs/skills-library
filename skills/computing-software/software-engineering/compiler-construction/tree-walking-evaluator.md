---
id: computing-software.software-engineering.compiler-construction.tree-walking-evaluator
name: tree-walking-evaluator
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, eval-loop, runtime-values, runtime-errors, tree-walking-interpreter, environments, closures, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Simple interpreters"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tree-walking evaluation

Goal: execute an AST.
- `eval(node, env)` with a tagged runtime value type; environments chain for scope.
- Short-circuit `and/or`; truthiness rules; runtime errors with line numbers.
- Slow but easy; good for prototypes and DSLs.
Verify: factorial and fib programs produce correct output.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
