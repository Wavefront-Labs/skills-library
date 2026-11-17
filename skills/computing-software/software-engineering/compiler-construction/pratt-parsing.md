---
id: computing-software.software-engineering.compiler-construction.pratt-parsing
name: pratt-parsing
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, pratt-parser, precedence-climbing, binding-power, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Expression parsing"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pratt (precedence climbing) parsing

Goal: parse operators compactly.
- Each token has prefix/infix handlers and a binding power; `parse_expr(min_bp)` loops while next operator binds tighter.
- Right associativity: recurse with `bp` instead of `bp+1`.
- Handles ternary, postfix and mixfix operators cleanly.
Verify: `1+2*3^2^2` parses with correct associativity.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
