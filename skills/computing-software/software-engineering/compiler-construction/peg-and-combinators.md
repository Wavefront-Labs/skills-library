---
id: computing-software.software-engineering.compiler-construction.peg-and-combinators
name: peg-and-combinators
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, peg-packrat, parser-combinators, nom-parsec, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Alternative parsing styles"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PEG and parser combinators

Goal: choose PEG/combinators.
- PEG ordered choice `/` removes ambiguity; packrat memoisation gives linear time but memory.
- Combinators (parsec, nom, megaparsec, chumsky) build parsers as functions.
- Left recursion needs special handling in PEG.
Verify: parses the same corpus as the reference parser.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
