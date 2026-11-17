---
id: computing-software.software-engineering.compiler-construction.regex-to-dfa-lexers
name: regex-to-dfa-lexers
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, regex-to-nfa, subset-construction, lexer-generator, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Automata theory for lexers"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Regular expressions, NFA and DFA lexers

Goal: understand generated lexers.
- Thompson construction regex -> NFA; subset construction NFA -> DFA; Hopcroft minimisation.
- Tools: flex/re2c/logos/ocamllex generate table- or code-driven DFAs.
- Longest-match with priority by rule order.
Verify: generated lexer tokenises a corpus identically to the hand-written one.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
