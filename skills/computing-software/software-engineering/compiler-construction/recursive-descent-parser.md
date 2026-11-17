---
id: computing-software.software-engineering.compiler-construction.recursive-descent-parser
name: recursive-descent-parser
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, recursive-descent-parser, expression-grammar, left-recursion-elimination, recursive-descent, ll1, predictive-parsing, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Hand-written parsers"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recursive descent

Goal: write a parser from a grammar.
- One function per nonterminal; eliminate left recursion with loops (`while match(PLUS)`).
- Precedence by layering rules: expression -> term -> factor -> unary -> primary.
- Synchronise after errors on statement boundaries (panic mode).
Verify: parses and pretty-prints test programs round-trip.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
