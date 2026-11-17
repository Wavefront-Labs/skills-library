---
id: computing-software.software-engineering.compiler-construction.hand-written-scanner
name: hand-written-scanner
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, scanner-loop, lookahead-char, maximal-munch, lexer, tokenizer, scanner, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Writing a scanner"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hand-written scanners

Goal: build a robust tokenizer.
- Loop over characters with one-character lookahead; produce tokens with type, lexeme, literal and position (line/column).
- Maximal munch: take the longest match (`>=` over `>`); keywords by looking up identifier text in a table.
- Handle strings with escapes, nested/unterminated comments, and report errors with positions, then keep scanning to find more errors.
Verify: unit tests for edge tokens and unterminated constructs.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
