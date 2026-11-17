---
id: computing-software.software-engineering.compiler-construction.antlr-and-bison
name: antlr-and-bison
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, antlr4-grammar, bison-yacc, tree-listener, antlr, peg-parser, parser-combinators, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Generated parsers"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ANTLR and bison/yacc

Goal: use a generator.
- ANTLR4: `grammar X; expr: expr '*' expr | INT;` supports direct left recursion; visitor/listener APIs.
- Bison: `%union`, actions `$$ = $1 + $3;`, `yyerror`.
- Lexer modes and error strategies matter for usable errors.
Verify: generated parser handles test inputs and reports line/column errors.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
