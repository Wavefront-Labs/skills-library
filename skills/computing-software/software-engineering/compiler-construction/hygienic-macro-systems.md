---
id: computing-software.software-engineering.compiler-construction.hygienic-macro-systems
name: hygienic-macro-systems
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, hygiene, syntax-rules, procedural-macros, hygienic-macros, macro-expansion, compile-time-evaluation, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Metaprogramming"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Macro expansion and hygiene

Goal: implement or reason about macros.
- Textual macros (C preprocessor) vs syntactic macros (Lisp, Rust `macro_rules!`); hygiene avoids accidental capture via renaming/scopes.
- Procedural macros operate on token streams.
- Expansion happens before name resolution/type checking.
Verify: a macro that introduces a temporary does not capture user variables.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
